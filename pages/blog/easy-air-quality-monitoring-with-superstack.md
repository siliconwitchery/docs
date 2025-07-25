---
title: "Easy Air Quality Monitoring with Superstack"
parent: Blog
nav_order: 2
---

Air quality plays a crucial role in our everyday health and well-being. Poor air quality can lead to respiratory issues, allergies, and long-term health complications, especially for vulnerable groups such as children and the elderly. Applications range from improving comfort and safety in homes and offices, to ensuring compliance and worker safety in factories, and optimizing HVAC systems in commercial buildings. By keeping track of air quality metrics, we can make informed decisions to create healthier and more productive environments. In this article, we explore an easy indoor air quality monitoring system powered by S2-Superstack

## Setup

### Hardware
For this project, we used a Sparkfun ENS160 air quality sensor, which measures the air quality index (AQI), equivalent carbon dioxide (eCO2), and total volatile organic compounds (TVOC). The sensor board comes with an easy to use Qwiic interface, and can be easily configured to work with I2C on any of the 4-pin ports of the S2 module.

[image: hardware setup]

### Platform

Begin by setting up a new deployment and adding the device to that deployment. Refer to [Getting Started with S2-Superstack](/pages/blog/getting-started-with-s2-superstack.md) for a step-by-step guide.

## Implementation
TODO: what details go here other than code?

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

## Data Access and Analysis

### Using the Agent Interface

- In the Agent tab, enter queries in the chat box. The agent retrieves, filters, and analyzes data, returning concise summaries.
- See the [documentation](/pages/superstack/#ai-agent) for technical details.

### Data API Integration

- Generate an API key in the Settings tab to access the data API.
- The API supports reading, deleting device data, and programmatic agent queries. Refer to the [documentation](/pages/superstack/#data-api) for usage examples.

---