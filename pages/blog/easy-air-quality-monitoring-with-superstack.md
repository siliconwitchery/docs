---
title: "Easy Air Quality Monitoring with Superstack"
parent: IoT Solutions Blog
nav_order: 2
---

# **Easy Air Quality Monitoring with Superstack**

Rohit Nareshkumar, Solutions Architect and Embedded Applications Engineer \| 28 July 2025
{: .float-left .fs-2 }

---

Air quality is a key factor in our health and well-being. Poor air quality can cause respiratory issues, allergies, and long-term health problems, especially for children, the elderly, and those with pre-existing conditions. Monitoring air quality is important not only for comfort and safety in homes and offices, but also for regulatory compliance in the workplace and for optimizing HVAC systems in commercial buildings. 

By tracking air quality metrics, we can make informed decisions to create healthier, more productive environments. This article demonstrates a straightforward indoor air quality monitoring system using the S2 Module and a low-cost air quality sensing module available from popular distributors.

---

## Setup

### Hardware

For this project, we will use a [ScioSence ENS160](https://www.sciosense.com/wp-content/uploads/2023/12/ENS160-Datasheet.pdf) air quality sensor from [Sparkfun Electronics](https://www.sparkfun.com/sparkfun-indoor-air-quality-sensor-ens160-qwiic.html). It's capable of measuring Air Quality Index (AQI), Equivalent Carbon Dioxide (eCO2), as well as Total Volatile Organic Compounds (TVOC). The sensor module from Sparkfun features a Qwiic I<sup>2</sup>C interface and can be connected to any of the 4-pin ports on the S2 module.

![S2 Module connected to the ENS160 air quality sensor](/assets/images/blog/easy-air-quality-monitoring-hardware.png)

### Platform

Start by creating a new deployment and adding your device to it:

> For detailed steps, see the blog post on [Getting Started with the S2 Module and Superstack](/pages/blog/getting-started-with-s2-superstack).

![Devices tab showing the air quality monitoring device](/assets/images/blog/easy-air-quality-monitoring-devices-tab.png)

---

## Implementation

The following code initializes the ENS160 air quality sensor, reads AQI, TVOC, and eCO2, and sends the measurements to Superstack at regular intervals:

```lua
local ENS160_I2C_ADDRESS = 0x53

-- Set the IO to 3.3V
device.power.set_vout(3.3)

-- Check if the device is connected by reading the part ID
local response = device.i2c.read(ENS160_I2C_ADDRESS, 0x00, 2)

if not response.success then
    error("Device not found")
end

if string.byte(response.data, 1) ~= 0x60 or string.byte(response.data, 2) ~= 0x01 then
    error("Incorrect device ID")
end

-- Enable gas sensing mode
device.i2c.write(ENS160_I2C_ADDRESS, 0x10, "\x02")

-- Provide temperature calibration to the sensor (assume 25°C)
device.i2c.write(ENS160_I2C_ADDRESS, 0x13, "\x80\x4A")

-- Provide relative humidity calibration to the sensor (assume 50%)
device.i2c.write(ENS160_I2C_ADDRESS, 0x15, "\x00\x64")

print("Sensor configured")

-- Read the sensor periodically
while true do
    print("Reading AIQ, TVOC and eCO2")

    response = device.i2c.read(ENS160_I2C_ADDRESS, 0x21, 1)
    local aqi = response.value & 0x07

    response = device.i2c.read(ENS160_I2C_ADDRESS, 0x22, 2)
    local tvoc = string.byte(response.data, 1) | string.byte(response.data, 2) << 8

    response = device.i2c.read(ENS160_I2C_ADDRESS, 0x24, 2)
    local eco2 = string.byte(response.data, 1) | string.byte(response.data, 2) << 8

    -- Send the values to Superstack
    network.send_data {
        air_quality_index = aqi,
        total_volatile_compounds = { value = tvoc, unit = "ppb" },
        equivalent_CO2 = { value = eco2, unit = "ppm" }
    }

    -- Sleep for 30 minutes
    device.sleep(30 * 60)
end
```

![Air quality sensor code running on the S2 Module](/assets/images/blog/easy-air-quality-monitoring-code-tab.png)

---

## Data Access and Analysis

The **Data** tab shows all the measurements received from the device. The Lua table provided to `network.send_data()` is converted to a JSON object. The key names match those provided in Lua. Nested fields are supported, allowing you to provide additional context or neatly separate fields when multiple sensors are used. Metadata such as device IMEI and timestamp are added automatically:

> Using complete names for the keys in `network.send_data()` is helpful for the AI agent to understand the context of what the data represents. Avoid using acronyms or shorthand variable names.
>
> Additionally, the **Device Role** field within the individual device details from the **Devices** tab can be used to provide more capabilities about the specific sensor and units of measurement that can help the AI agent analyze the data returned.

![Data tab showing the logged air quality data](/assets/images/blog/easy-air-quality-monitoring-data-tab.png)

### Using the Agent Interface

From within the **Agent** tab, you can then ask questions about the overall air quality. For example, query averages, trends, or peaks. By populating the **Agent Role** field with specifics regarding expected ranges or maximum healthy limits, the AI agent can better analyze the data against these limits and provide recommendations on how to improve air quality if needed.

> To better understand how the AI agent works, see the [detailed documentation](/pages/superstack/#ai-agent) of Superstack.

![Agent tab showing a query about indoor air quality](/assets/images/blog/easy-air-quality-monitoring-agent-tab.png)

### External API Integration

Both the data and AI agent are programmatically accessible via REST APIs, allowing for easy integration of Superstack's data logging and agentic capabilities into your own applications.

Begin by generating an API key from the **Settings** tab:

![Settings tab showing the new API key button](/assets/images/blog/easy-air-quality-monitoring-api-key.png)

The following example demonstrates how to use `curl` from a WSL, Linux, or macOS terminal to view data recorded between 10am and 11am UTC on the 21st of July 2025:

> For more detailed examples, check the [complete API reference](/pages/superstack/#apis) within the Superstack documentation.

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

A `chat` endpoint is also available for interacting with the AI agent:

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
                "content": "What is the level of CO2 now?"
            }
        ]
    }'
```

**Response**
```json
[
    {
        "role": "user",
        "content": "What is the level of CO2 now?",
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

## Conclusion

This air quality monitoring system demonstrates how easily you can deploy IoT solutions using the S2 Module and Superstack platform. The combination of reliable hardware, simple code, and powerful AI-driven analysis makes it straightforward to monitor and improve indoor air quality in any environment.

---

## Learn More

- [Product page](https://www.siliconwitchery.com/s2-superstack)
- [Superstack API reference and documentation](/pages/superstack/)
- [S2 Module hardware manual](/pages/s2-module)

## Need Assistance?

For support or questions, [email our engineering team](mailto:projects@siliconwitchery.com?subject= Superstack IoT Consultation&amp;body=Hello Silicon Witchery team,%0D%0A%0D%0AI'm interested in support for my project.%0D%0A%0D%0A- Brief description:%0D%0A- Timeline:%0D%0A- Company:%0D%0A%0D%0ABest regards,) for a free consultation.
