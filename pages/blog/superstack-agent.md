---
title: "Superstack AI Agent"
parent: IoT Solutions Blog
description: TODO
image: /assets/images/blog/share-image.png
nav_order: 4
---

# **Superstack Agent**

Raj Nakarja, CEO and Chief Engineer \| 15 August 2025
{: .float-left .fs-2 }

---

Modern LLMs are not databases or number‑crunchers—and if you naively dump raw timeseries into them, they’ll hallucinate, drop edge cases, and miss units. To make LLMs useful for data analysis, you must wrap them in a proper system: one that retrieves the right data, computes deterministically, and asks the model only to reason, plan, and explain.

In our experience, LLMs excel at three things:
- **Text compression**: distilling long specs, schemas, and prior chats into concise working context. We use this to build compact analysis plans and keep prompts focused on what matters.
- **Fuzzy search within text**: semantically locating relevant devices, fields, and time ranges across messy metadata, logs, and schemas. We use this to select the exact slice of data that should be analyzed.
- **Cross‑domain comparison**: linking concepts, units, and heuristics across domains (e.g., “solar yield per m²” vs “kWh counters” vs “irradiance”). We use this to frame results, choose reasonable defaults, and translate findings for the end user.

Superstack’s Agent is designed around those strengths. It never lets the model “touch” your raw rows directly. Instead, it orchestrates three steps:
1) Filter: identify precisely which data is relevant,
2) Analyse: run deterministic code on that data in a secure runtime,
3) Explain: turn results into clear, contextual answers—along with the model’s reasoning.

In this article, we’ll show how the Superstack Agent works end‑to‑end and share what changes with GPT‑5: better instruction‑following and robustness, but with notable latency trade‑offs. You’ll see where GPT‑5 helps, where it can slow things down, and how we’re optimizing prompts and execution to get the best of both.

## How does the agent work? 

The Superstack agent works through a series of orchestrated steps that transform natural language queries into precise data analysis. Each step leverages the LLM's strengths while maintaining strict separation between the AI models and your raw IoT data.

![block diagram showing the agent pipeline](/assets/images/blog/superstack-agent-pipeline.drawio.png)

---

Let's examine these steps in detail with a simple example query for a deployment of plant health monitors - consider the user asks `What's the average temperature in my greenhouse?`

### 1. Filter

The Filter step analyzes your deployment's metadata and data structure to determine what information is relevant to the query. The LLM examines device names, groups, locations, and sensor types to understand which devices are relevant to the user's question. In our example asking about "my greenhouse," the system identifies that only devices belonging to the "greenhouse" group should be included in the analysis.

![Superstack devices tab showing greenhouse and outside groups](/assets/images/blog/superstack-agent-devices.png)

As shown above, the system would select devices like "Tomatoes," "Rosemary & basil," and "Marjoram" from the greenhouse group, while excluding "Kale" and "Lettuce" from the outside group. The system also inspects the JSON data structure from these devices to understand reporting frequency, available sensor fields, and data patterns.

Since no specific time range was provided in the query, the Filter tool assumes a reasonable default timeframe to ensure current and relevant data. It will look for the most recent temperature reading from each greenhouse device within the last few hours, ensuring that the analysis reflects the current state rather than stale data. If a device's last reported temperature is too old (for example, more than 6-12 hours depending on the expected reporting frequency), that device will be excluded from the calculation to maintain data quality and relevance.

The output is a precise filter specification that will select only the relevant, recent temperature readings from active greenhouse devices—no raw data is shared with the AI provider.

### 2. Analyze

Using the data structure understanding from Step 1, this step generates a deterministic algorithm tailored to answer the specific query. The LLM creates executable code that will perform the exact calculation needed—in our temperature average example, it generates code to compute the mean of temperature values while properly handling missing data points, different units of measurement, and varying reporting frequencies across devices.

The algorithm might include statistical validation, outlier detection, or temporal aggregation depending on the complexity of the query. Importantly, the LLM only generates the analysis code—it never sees or processes your actual data. This generated algorithm then executes in Superstack's secure runtime environment, processing only the filtered data to produce a precise numerical result.

### 3. Explain

The final step takes the computed results along with the detailed reasoning from both previous steps and synthesizes them into a clear, contextual answer. It draws upon the user's domain context (such as device roles and deployment settings), chat history for conversational continuity, and the specific reasoning used in filtering and analysis to craft an appropriate response.

In our greenhouse temperature example, it would present the calculated average along with relevant context such as which devices contributed to the calculation, the time period analyzed, any data quality considerations encountered, and suggestions for follow-up questions. The response is formatted appropriately whether accessed through the web interface or API, maintaining both human readability and programmatic usability.

### Key Benefits

This orchestrated approach delivers several critical advantages:

- **Model agnostic**: Each step can use the optimal model for its specific task—whether that's GPT-5 for complex reasoning or a smaller model for simple filtering. This flexibility allows us to quickly adopt new models and optimize for both performance and cost.

- **Data sovereignty**: Your IoT data never leaves Superstack's infrastructure. AI providers only see metadata, data structures, and generated algorithms—never your actual sensor readings or device information.

- **Contextual precision**: The complete system context—including chat history, deployment-specific roles, and device metadata—is available at each step. This enables fine-tuned prompting that produces more accurate and relevant results than generic data analysis tools.

The conversational interface is accessible both through our web application and programmatically via REST API, making it easy to integrate natural language data analysis into your own applications or workflows.

---

## GPT5 vs GPT4.1
While investigating the effectiveness of different models for the superstack agent we noticed some interesting behaviour.

The example deployment here consists of a number of devices in 2 groups - 'greenhouse' and 'outside'. Each device reports the temperature, soil moisture and light level in varying intervals.
One of the queries we tried was the following: `What was the temperature range in the greenhouse over the last 3 days?`, using GPT4.1 and then GPT5.
Both models were able to calculate the right answer, but with significantly different timelines. GPT4.1 took a total of 17.1 seconds, whereas GPT5 took 57.22 seconds! Comparing the intermediate steps and between runs, we noted that the code generated by GPT5 followed the instructions more closely, and was more meticulous, however the latency impact is tremendous. This tracks with openAI's docs other developer's experience, but our expectation was the internal model router mechanism of GPT5 would reroute simpler queries resulting in faster processing times.

Next we tried a much more complex query on a solar farm deployment consisting of 2 different panels 'farmhouse' and 'barn', which face different directions, and have simulated power output using real world solar incidence data. The query we ran was: `I am planning on installing another panel, which location is better? What percentage difference can I expect with a 15m^2 panel per day?`. We made sure the sampling times did not exactly match in the two sites, to keep it realistic - and this caused both models to struggle. GPT4.1 failed to give an answer, the filter agent was not able to infer a reasonable time range since it is not explicitly mentioned in the query. GPT5 correctly tried to fetch a year's worth of data, and came up with following plan:
```
- Aggregate each device’s measurements by day. 
- For every day and device, try to compute total daily energy in kWh using this priority: 
    (1) use explicit energy/yield counters (daily counter value or end-start difference with reset handling and unit detection for kWh/Wh), 
    (2) if no energy counters, integrate power over time within the day via trapezoidal approximation, 
    (3) as a last resort, integrate irradiance to Wh/m² and convert to electrical energy by assuming a typical module efficiency, then treat that as kWh per m². 
- Average daily energy across available days for each device, normalize by the device’s panel area to get kWh per m² per day, and compare locations. 
- Identify the better site as the one with higher per‑m² yield. Estimate the expected daily energy for a 15 m² panel at both sites and compute the percentage difference between them.
```