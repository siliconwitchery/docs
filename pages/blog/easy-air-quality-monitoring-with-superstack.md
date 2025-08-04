---
title: "Easy Air Quality Monitoring with Superstack"
parent: IoT Business Solutions Blog
nav_order: 2
---

# **Easy Air Quality Monitoring with Superstack**

Rohit Nareshkumar, Embedded Engineer \| 24 July 2025
{: .float-left	.fs-2 }
---
Air quality is a key factor in our health and well-being. Poor air quality can cause respiratory issues, allergies, and long-term health problems, especially for children, the elderly, and those with pre-existing conditions. Monitoring air quality is important not only for comfort and safety in homes and offices, but also for regulatory compliance and worker safety in factories, and for optimizing HVAC systems in commercial buildings. By tracking air quality metrics, we can make informed decisions to create healthier, more productive environments. This article demonstrates a straightforward indoor air quality monitoring system using S2-Superstack.

---

## Setup

### Hardware
For this project, we use a Sparkfun ENS160 air quality sensor, which measures the air quality index (AQI), equivalent carbon dioxide (eCO2), and total volatile organic compounds (TVOC). The sensor board features a Qwiic interface and can be connected via I2C to any 4-pin port on the S2 module.

[TODO image: hardware setup]

### Platform

Start by creating a new deployment and adding your device to it. For detailed steps, see [Getting Started with S2-Superstack](/pages/blog/getting-started-with-s2-superstack.md). Once your device is set up, your deployment should look like this:

![Devices tab showing the air quality monitoring device](/assets/images/blog/easy-air-quality-monitoring-devices-tab.png)

---

## Implementation
The following code initializes the ENS160 air quality sensor, reads air quality data (AQI, TVOC, and eCO2) at regular intervals, and sends the measurements to the Superstack platform. The sensor is configured for typical indoor conditions, and the device sleeps between readings to conserve power.

```lua
local ENS160_I2C_ADDRESS = 0x53

function init_sensor()
    local resp = device.i2c.write(ENS160_I2C_ADDRESS, 0x10, "\x02")
    if not resp.success then
        error("I2C bus error")
    end
    device.sleep(0.2)

    -- 25C
    resp = device.i2c.write(ENS160_I2C_ADDRESS, 0x13, "\x80\x4A")
    if not resp.success then
        error("I2C bus error")
    end
    device.sleep(0.2)

    -- 50% RH
    resp = device.i2c.write(ENS160_I2C_ADDRESS, 0x15, "\x00\x64")
    if not resp.success then
        error("I2C bus error")
    end
    device.sleep(0.2)
end

function read_sensor()
    local sensor_data = {}
    local resp = device.i2c.read(ENS160_I2C_ADDRESS, 0x21, 1)
    if resp.success then
        sensor_data.aqi = resp.value & 0x07
    else
        error("I2C bus error")
    end
    resp = device.i2c.read(ENS160_I2C_ADDRESS, 0x22, 2)
    if resp.success then
        sensor_data.tvoc = string.byte(resp.data, 1) | string.byte(resp.data, 2) << 8;
    else
        error("I2C bus error")
    end
    resp = device.i2c.read(ENS160_I2C_ADDRESS, 0x24, 2)
    if resp.success then
        sensor_data.eco2 = string.byte(resp.data, 1) | string.byte(resp.data, 2) << 8;
    else
        error("I2C bus error")
    end
    return sensor_data
end

-- main
device.power.set_vout(1.8)
init_sensor()
while true
do
    sensor_data = read_sensor()
    -- print(string.format("AQI: %d, TVOC: %d ppb, eCO2: %d ppm", sensor_data.aqi, sensor_data.tvoc, sensor_data.eco2))
    network.send_data {
        air_quality_index = sensor_data.aqi,
        total_volatile_compounds = { value = sensor_data.tvoc, unit = "ppb" },
        equivalent_CO2 = { value = sensor_data.eco2, unit = "ppm" }
    }
    -- sleep for 30 mins
    device.sleep(60*30)
end
```

![Code tab showing some debug print statements](/assets/images/blog/easy-air-quality-monitoring-code-tab.png)

---

## Data Access and Analysis

The data logged by the device is available in the `Data` tab. The Lua table sent with `network.send_data()` is converted to a JSON object under the `data` field. Metadata such as device IMEI and timestamp are added automatically. Nested fields are supported, allowing you to provide additional context.

![Data tab showing the logged air quality data](/assets/images/blog/easy-air-quality-monitoring-data-tab.png)

### Using the Agent Interface

In the Agent tab, you can enter queries in the chat box. The agent retrieves, filters, and analyzes data, returning concise summaries. For example, you can ask about air quality on a specific date or location. The agent uses device names and date ranges to filter relevant entries and analyze the data. See the [documentation](/pages/superstack/#ai-agent) for technical details.

![Agent tab showing a query about indoor air quality](/assets/images/blog/easy-air-quality-monitoring-agent-tab.png)

### Data API Integration

Generate an API key in the Settings tab to access the data API. 
![Settings tab showing the new api key button](/assets/images/blog/easy-air-quality-monitoring-api-key.png)

The API allows you to read and delete device data, and to make programmatic agent queries. See the [documentation](/pages/superstack/#data-api) for usage examples.

**Data request**
```sh
curl https://super.siliconwitchery.com/api/data \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "7b311c01-0b8c-4e81-902e-5c5a8e916662",
        "time": {
            "start": "2025-07-21T10:30:00+00:00",
            "end": "2025-07-21T11:30:00+00:00"
        }
    }'
```

**Response**
```json
[
    {
        "data": {
            "air_quality_index": 1,
            "equivalent_CO2": {
                "unit": "ppm",
                "value": 400
            },
            "total_volatile_compounds": {
                "unit": "ppb",
                "value": 0
            }
        },
        "device": "359404230274418",
        "time": "2025-07-21 - 11:08:37"
    }
]
```

**Agent request**
```sh
curl https://super.siliconwitchery.com/api/chat \
    -H 'Content-Type: application/json'         \
    -H 'X-Api-Key: <API-Key>'                   \
    -d '{
        "deploymentId": "7b311c01-0b8c-4e81-902e-5c5a8e916662",
        "messages": [
            {
                "role": "user",
                "content": "what is the level of CO2 now?"
            }
        ]
    }'
```

**Response**
```json
[
    {
        "role": "user",
        "content": "what is the level of CO2 now?",
        "reasoning": {
            "filter": "",
            "analysis": ""
        }
    },
    {
        "role": "assistant",
        "content": "The latest equivalent CO2 level is 408 ppm.",
        "reasoning": {
            "filter": "To determine the current CO2 level, we want the most recent data point from the device in the office on the 3rd floor that monitors indoor air quality. Sampling from the past several hours ensures relevance, and selecting just the latest measurement from each device provides the most up-to-date reading.",
            "analysis": "To answer the question, I look for the most recent value of the equivalent CO2 level reported by any device, using the 'equivalent_CO2' sensor value in the data. I select the entry with the latest timestamp containing this value. If such data is not available, I return a message indicating its absence."
        }
    }
]
```

---

## Learn More

- [Product page](https://www.siliconwitchery.com/s2-superstack)
- [Documentation](/pages/superstack/)

## Need Assistance?

For support or questions, [email our engineering team](mailto:projects@siliconwitchery.com?subject=IoT Project Support - Superstack&amp;body=Hi Silicon Witchery team,%0D%0A%0D%0AI'm interested in implementation support for:%0D%0A%0D%0A- Project type:%0D%0A- Timeline:%0D%0A- Company:%0D%0A%0D%0ABest regards,) for a free consultation.