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

> 1. **Filter**: identify precisely which data is relevant,
> 
> 1. **Analyze**: run deterministic code on that data in a secure runtime,
> 
> 1. **Explain**: turn results into clear, contextual answers—along with the model’s reasoning.

---

In this article, we’ll show how the Superstack Agent works end‑to‑end and share what changes with GPT‑5: better instruction‑following and robustness, but with notable latency trade‑offs. You’ll see where GPT‑5 helps, where it can slow things down, and how we’re optimizing prompts and execution to get the best of both.

---

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

This orchestrated approach delivers several critical advantages over traditional data analysis tools and naive LLM implementations:

- **Model agnostic**: Each step can use the optimal model for its specific task—whether that's GPT-5 for complex reasoning or a smaller, faster model for simple filtering. This flexibility allows us to quickly adopt new models and optimize for both performance and cost as the AI landscape evolves.

- **Data sovereignty**: Your IoT data never leaves Superstack's infrastructure. AI providers only see metadata, data structures, and generated algorithms—never your actual sensor readings or device information. This ensures compliance with data privacy regulations and eliminates concerns about sensitive operational data being used to train external models.

- **Deterministic accuracy**: Unlike direct LLM analysis which can hallucinate or make calculation errors, our approach generates verifiable code that produces mathematically correct results. The separation between reasoning (LLM) and computation (deterministic algorithms) eliminates the reliability issues that plague other AI data analysis tools.

- **Contextual precision**: The complete system context—including chat history, deployment-specific roles, and device metadata—is available at each step. This enables fine-tuned prompting that produces more accurate and relevant results than generic data analysis tools, while understanding domain-specific terminology and relationships.

- **Scalable complexity**: The system handles everything from simple averages to sophisticated statistical analysis, automatically generating appropriate algorithms based on query complexity. As your data needs grow, the agent adapts without requiring manual reconfiguration.

The conversational interface is accessible both through our web application and programmatically via REST API, making it easy to integrate natural language data analysis into your own applications or workflows.

---

## GPT5 vs GPT4.1

To evaluate the practical differences between GPT-4.1 and GPT-5 in our agent pipeline, we conducted a series of tests using real solar panel data from a ranch deployment in Boulder, Colorado. The setup consists of two 20-square-meter solar arrays—one mounted on a house roof and another on a barn—with panels reporting power output every 15 minutes throughout the year. This high-frequency data creates a substantial dataset perfect for testing the models' analytical capabilities.

![](/assets/images/blog/superstack-agent-solar-data.png)

This solar deployment exemplifies why Superstack's filtered approach is essential for real IoT analytics. With readings every 15 minutes from multiple panels across a full year, the dataset contains over 70,000 individual data points. Naively sending this raw data to an AI provider would cost hundreds of dollars per query due to token pricing, and would frequently exceed context limits entirely—GPT-4's 128k token limit could only accommodate a fraction of the year's data. More critically, LLMs perform poorly on large numerical datasets, often hallucinating patterns or dropping precision in calculations. Superstack's architecture solves this by using the LLM only for reasoning about *which* data to analyze and *how* to analyze it, while keeping the actual number-crunching deterministic and local.

### Test Setup

We designed three progressively complex queries to stress-test both models:

1. **"What was the average power output in May?"** - A straightforward aggregation requiring temporal filtering and basic statistics
2. **"What day in May had the best power output?"** - Requires grouping by date, calculating daily totals, and identifying the maximum
3. **"How many watt hours were generated in May?"** - The most complex query, requiring unit conversion from instantaneous power readings to cumulative energy over time

Each query was tested multiple times across both model versions to assess consistency and reliability.

### Results and Analysis

| Query | GPT4.1 result | GPT5 result |
|-------|:------:|:----:|
| "What was the average power output in May?"  | Filter passed: **10/10**<br>Analysis passed: **10/10** | Filter passed: **10/10**<br>Analysis passed: **10/10** |
| "What day in May had the best power output?" | Filter passed: **5/10**<br>Analysis passed: **10/10**  | Filter passed: **10/10**<br>Analysis passed: **10/10** |
| "How many watt hours were generated in May?" | Filter passed: **10/10**<br>Analysis passed: **4/10**  | Filter passed: **10/10**<br>Analysis passed: **10/10** |

**Query 1: Average Power Output**
Both GPT-4.1 and GPT-5 handled this query reliably. The filtering step correctly identified May data from both arrays, and the analysis step generated appropriate code to compute the mean across all 15-minute intervals. Response times were comparable, with both models consistently producing accurate results.

**Query 2: Best Day Identification**  
Here we began to see differences. GPT-4.1 occasionally struggled with the temporal grouping logic, sometimes generating code that would aggregate across hours rather than days, or failing to properly handle timezone considerations for the Boulder location. GPT-5 showed more robust instruction-following, consistently generating correct daily aggregation algorithms and properly accounting for the Mountain Time zone.

**Query 3: Energy Calculation (Watt Hours)**
This query revealed the most significant gap between models. GPT-4.1 frequently failed to generate correct integration logic, often treating instantaneous power readings as if they were already energy measurements, or miscalculating the time intervals for numerical integration. 

GPT-5, by contrast, consistently understood that converting from 15-minute power samples to total energy requires proper temporal integration. It reliably generated code that would sum `(power_reading * 0.25 hours)` across all intervals, correctly handling the units conversion from watts to watt-hours.

### Performance Implications

| Query | GPT4.1 avg time taken | GPT5 avg time taken |
|-------|:------:|:----:|
| "What was the average power output in May?"  | Filter: **11.5s**<br>Analysis: **13.4s** | Filter: **31.1s**<br>Analysis: **69.7s** |
| "What day in May had the best power output?" | Filter: **10.5s**<br>Analysis: **16.1s** | Filter: **28.3s**<br>Analysis: **63.7s** |
| "How many watt hours were generated in May?" | Filter: **10.5s**<br>Analysis: **22.1s** | Filter: **33.7s**<br>Analysis: **78.9s** |

While GPT-5 demonstrated superior reasoning and instruction-following, this came with notable latency trade-offs. GPT-5 queries averaged 2-3 seconds longer than GPT-4.1, primarily in the Analysis step where more complex reasoning occurs. For applications requiring real-time responsiveness, this difference may influence model selection.

However, the reliability gains often offset the latency cost. Failed queries require retry logic and user interaction to clarify intent, ultimately taking longer than a single successful GPT-5 response. For complex analytical workloads like energy calculations, GPT-5's improved accuracy significantly reduces the need for manual verification and correction.

*[A graph showing the complete year of solar generation data will be inserted here, demonstrating how summer months generate significantly more energy than winter months - this seasonal pattern was correctly identified and explained by both models when analyzing the May data in context.]*

### Optimization Strategies

Based on these findings, we've implemented a hybrid approach in production:

- **Simple aggregations** (averages, counts, basic filtering) default to GPT-4.1 for faster response times
- **Complex analytical queries** (unit conversions, temporal calculations, multi-step reasoning) automatically use GPT-5
- **Query complexity scoring** in the Filter step helps determine optimal model selection

This strategy delivers the best balance of accuracy and performance, ensuring users get fast responses for simple questions while maintaining reliability for sophisticated analysis.

---

