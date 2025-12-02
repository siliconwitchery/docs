---
title: API Reference
parent: Superstack Platform
description: 
image: /assets/images/superstack-annotated-masthead.png
nav_order: 2
---


### Authentication

For accessing the APIs. Both the `Deployment-ID` and `API-Key` are required in order to make requests. They can be obtained from within the **Settings Tab** within Superstack.

![Superstack deployment ID](/assets/images/superstack-deployment-id.png)

The **API Key** is created using the **Create Key** button and can be then copied to use within the authentication header.

**Remember that API Keys are secrets.** Do not share it with others or expose it in any client-side code. API Keys should be securely loaded from an environment variable or key management service on the server.

![Superstack API Keys](/assets/images/superstack-api-key.png)

The `API-Key` should be specified within the `X-Api-Key` header, and the `Deployment-ID` should be passed to the `deploymentId` field within the request body.

```sh
curl https://super.siliconwitchery.com/api/data \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "<Deployment-ID>"
    }'
```

---

### Data API

### `POST https://super.siliconwitchery.com/api/data`
{: .no_toc }

Retrieves Data from the Deployment.

**Example request**

```sh
curl https://super.siliconwitchery.com/api/data \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "00000000-0000-0000-0000-000000000000",
        "devices": ["Tomatoes", "Kale", "Marjoram"],
        "groups": ["greenhouse"],
        "time": {
            "start": "2025-06-17T13:30:00+02:00",
            "end": "2025-06-17T13:45:00+02:00"
        }
    }'
```

**Response**

```json
[
    {
        "device_name": "Marjoram",
        "device_group": "greenhouse",
        "timestamp": "2025-06-17T13:44:05.424264+02:00",
        "data_uuid": "ad59ea27-c507-46a2-a3fa-2c185d0425d6",
        "data": {
            "light_lux_level": 943.86,
            "temperature_celsius": 19.4,
            "soil_moisture_percent": 50
        }
    },
    {
        "device_name": "Tomatoes",
        "device_group": "greenhouse",
        "timestamp": "2025-06-17T13:44:34.160881+02:00",
        "data_uuid": "fed0532a-99e3-413e-a683-7ecda5179f54",
        "data": {
            "light_lux_level": 1204.56,
            "temperature_celsius": 25.1,
            "soil_moisture_percent": 71
        }
    }
]
```

<table>
    <tr>
        <th>Request parameter</th>
        <th>Scope</th>
        <th>Details</th>
    </tr>
    <tr>
        <td><code>deploymentId</code></td>
        <td>Required</td>
        <td><strong>string</strong> - The deployment ID as found on the Settings Tab</td>
    </tr>
    <tr>
        <td><code>devices</code></td>
        <td>Optional</td>
        <td><strong>list of strings</strong> - A list of Device Names or IMEIs to retrieve Data for. If not provided, all Devices will be included</td>
    </tr>
    <tr>
        <td><code>groups</code></td>
        <td>Optional</td>
        <td><strong>list of strings</strong> - A list of Device Groups to retrieve Data for. If not provided, all Groups will be included</td>
    </tr>
    <tr>
        <td><code>time.start</code></td>
        <td>Optional</td>
        <td><strong>string</strong> - An RFC 3339 formatted time string. If not provided, this value defaults to 24 hours before the current time</td>
    </tr>
    <tr>
        <td><code>time.end</code></td>
        <td>Optional</td>
        <td><strong>string</strong> - An RFC 3339 formatted time string. If not provided, this value defaults to the current time</td>
    </tr>
</table>

<table>
    <tr>
        <th>Returns</th>
        <th>Details</th>
    </tr>
    <tr>
        <td><code>device_name</code></td>
        <td><strong>string</strong> - The Device that generated the Data</td>
    </tr>
    <tr>
        <td><code>device_group</code></td>
        <td><strong>string</strong> - The Group that the Device belongs to</td>
    </tr>
    <tr>
        <td><code>timestamp</code></td>
        <td><strong>string</strong> - The time at which the Data was generated. Formatted as an RFC 3339 time string</td>
    </tr>
    <tr>
        <td><code>uuid</code></td>
        <td><strong>string</strong> - A unique ID for the row of Data. Can be used to delete the Data</td>
    </tr>
    <tr>
        <td><code>data</code></td>
        <td><strong>object</strong> - The Data</td>
    </tr>
</table>

---

### `DELETE https://super.siliconwitchery.com/api/data`
{: .no_toc }

Deletes Data from the Deployment.

{: .warning }
This action is irreversible


**Example request**

```sh
curl https://super.siliconwitchery.com/api/data \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "00000000-0000-0000-0000-000000000000",
        "ids": ["ad59ea27-c507-46a2-a3fa-2c185d0425d6", "fed0532a-99e3-413e-a683-7ecda5179f54"],
        "confirm": true
    }'
```

<table>
    <tr>
        <th>Request parameter</th>
        <th>Scope</th>
        <th>Details</th>
    </tr>
    <tr>
        <td><code>deploymentId</code></td>
        <td>Required</td>
        <td><strong>string</strong> - The deployment ID as found on the Settings Tab</td>
    </tr>
    <tr>
        <td><code>ids</code></td>
        <td>Required</td>
        <td><strong>list of strings</strong> - A list UUIDs representing each row of data that should be deleted</td>
    </tr>
    <tr>
        <td><code>confirm</code></td>
        <td>Required</td>
        <td><strong>boolean</strong> - Confirms that the data should be deleted. This value can be set to `false` in order to test the API without actually deleting the data</td>
    </tr>
</table>

---

### Natural language API

### `POST https://super.siliconwitchery.com/api/chat`
{: .no_toc }

Runs a chat query with the AI Agent.

**Example request**

```sh
curl https://super.siliconwitchery.com/api/chat \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "00000000-0000-0000-0000-000000000000",
        "messages": [
            {
                "role": "user",
                "content": "What is the average temperature in my greenhouse?"
            }
        ]
    }'
```

**Response**

```json
[
    {
        "role": "user",
        "content": "What's the average temperature in my greenhouse?",
        "answer": "",
        "reasoning": {
            "filter": "",
            "analysis": ""
        }
    },
    {
        "role": "assistant",
        "content": "The average temperature in your greenhouse over the past 6 hours is approximately 26.7°C. If you need a breakdown by specific sensor or details for a different time frame, let me know!",
        "answer": "26.7",
        "reasoning": {
            "filter": "To answer your question accurately, I need to filter data to only include the latest measurements from devices located in the greenhouse within the past 6 hours. This ensures recent and relevant information from all greenhouse devices is used for your analysis.",
            "analysis": "The logic is to identify all devices in the greenhouse group, extract their reported temperature values, and compute the average. If no temperature data is found for any greenhouse device, return an appropriate error message."
        }
    }
]
```

<table>
    <tr>
        <th>Request parameter</th>
        <th>Scope</th>
        <th>Details</th>
    </tr>
    <tr>
        <td><code>deploymentId</code></td>
        <td>Required</td>
        <td><strong>string</strong> - The deployment ID as found on the Settings Tab</td>
    </tr>
    <tr>
        <td><code>messages</code></td>
        <td>Required</td>
        <td><strong>list of objects</strong> - A list of message to send to the chat agent. The response from the API may be fed back into this field if you wish the AI Agent to keep the chat history within context. Note that the tokens used relate directly to the length of this field. As the message history gets longer and longer, more tokens will be used for each query</td>
    </tr>
    <tr>
        <td><code>messages[].role</code></td>
        <td>Required</td>
        <td><strong>string</strong> - The role of a given message. Can be either <code>"user"</code> or <code>"assistant"</code></td>
    </tr>
    <tr>
        <td><code>messages[].content</code></td>
        <td>Required</td>
        <td><strong>string</strong> - The content of the message query</td>
    </tr>
</table>

<table>
    <tr>
        <th>Returns</th>
        <th>Details</th>
    </tr>
    <tr>
        <td><code>role</code></td>
        <td><strong>string</strong> - The role of a given message. Can be either <code>"user"</code> or <code>"assistant"</code></td>
    </tr>
    <tr>
        <td><code>content</code></td>
        <td><strong>string</strong> - The content of the message query</td>
    </tr>
    <tr>
        <td><code>answer</code></td>
        <td><strong>string</strong> - The computed answer related to the query</td>
    </tr>
    <tr>
        <td><code>reasoning</code></td>
        <td><strong>object</strong> - The reasoning steps that the AI Agent took while generating the response. Only relevant for the <code>"assistant"</code> role</td>
    </tr>
    <tr>
        <td><code>reasoning.filter</code></td>
        <td><strong>string</strong> - The reasoning behind the filter step</td>
    </tr>
    <tr>
        <td><code>reasoning.analysis</code></td>
        <td><strong>string</strong> - The reasoning behind the analysis step</td>
    </tr>
</table>

---