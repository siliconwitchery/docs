---
title: "Build a 5G Air Quality Monitor in Minutes"
parent: IoT Solutions Blog
description: "Learn how to build a production-ready 5G air quality monitoring system using the S2 module and Superstack platform. This step-by-step project shows how to connect ENS160 and SHT45 sensors, automate fan control, and access real-time data and AI insights—all in under 70 lines of code."
image: /assets/images/blog/share-image.png
nav_order: 5
---

# **Build a 5G Air Quality Monitor in Minutes**
Raj Nakarja, CEO and Chief Engineer \| 22 October 2025
{: .float-left .fs-2 }

---

<div style="position: relative; width: 100%; overflow: hidden; padding-top: 56.25%;">
    <iframe style="position: absolute; top: 0; left: 0; right: 0; width: 100%; height: 100%; border: none;"
        src="https://www.youtube.com/embed/hRCY-5qgxd4" title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
    </iframe>
</div>

### Ready to build a smart, production-ready 5G connected air quality monitoring system?
\
This project demonstrates how you can deploy a powerful IoT device in minutes using the **S2 module** and the **Superstack platform**. The entire build relies on readily available, off-the-shelf components, including a clear mounting box, the S2 module (the heart of the system), an **ENS160 air quality sensor**, and an **SHT45 temperature and humidity sensor**. Assembly is streamlined using the straightforward **qwiic / Stemma QT** interface, minimising complexity. 

All the remote management happens on **Superstack**, your central hub for viewing logs, editing the Lua code, and accessing device data. The result is a robust monitoring solution under 70 lines of code that tracks air quality index (AQI), carbond dioxide (CO2), and volatile organic compound (VOC) levels. It also automates a  relay to turn on a fan if CO2 or VOC levels exceed safe thresholds. Finally, Superstack makes the collected data instantly usable via **REST APIs** for dashboard integration and features an embedded **AI agent** capable of generating valuable, contextual insights about your deployment data.

Here's the complete Lua script for reference:

```lua

local SHT45_I2C_ADDRESS = 0x44
local ENS160_I2C_ADDRESS = 0x53

-- Enable gas sensing mode on the air quality monitor
device.i2c.write(ENS160_I2C_ADDRESS, "\x10\x02", { port = "PORTF" })

print("Reading temperature, humidity, AIQ, eCO2 and TVOC periodically")

-- Read the sensor periodically
while true do
    -- Measure the temperature and humidity
    device.i2c.write(SHT45_I2C_ADDRESS, "\xFD", { port = "PORTE" })
    device.sleep(0.01)
    response = device.i2c.read(SHT45_I2C_ADDRESS, 6, { port = "PORTE" })

    local raw_temperature = (string.byte(response.data, 1) << 8) | string.byte(response.data, 2)
    local raw_humidity = (string.byte(response.data, 4) << 8) | string.byte(response.data, 5)

    local temperature = -45 + (175 * (raw_temperature / 65535));
    local humidity = -6 + (125 * (raw_humidity / 65535));

    -- Provide calibration to the air quality sensor
    temperature_calibration = math.floor(temperature) + 273
    humidity_calibration = math.floor(humidity) << 9

    device.i2c.write(ENS160_I2C_ADDRESS, string.char(
            0x13,
            (temperature_calibration & 0x02) << 6,
            temperature_calibration >> 2),
        { port = "PORTF" })
    device.i2c.write(ENS160_I2C_ADDRESS, string.char(
            0x15,
            humidity_calibration & 0xff,
            humidity_calibration >> 8),
        { port = "PORTF" })

    -- Read the air quality sensor
    response = device.i2c.write_read(ENS160_I2C_ADDRESS, "\x21", 1, { port = "PORTF" })
    local aqi = response.value & 0x07

    response = device.i2c.write_read(ENS160_I2C_ADDRESS, "\x22", 2, { port = "PORTF" })
    local tvoc = string.byte(response.data, 1) | string.byte(response.data, 2) << 8

    response = device.i2c.write_read(ENS160_I2C_ADDRESS, "\x24", 2, { port = "PORTF" })
    local eco2 = string.byte(response.data, 1) | string.byte(response.data, 2) << 8

    -- Turn the fan on or off based on CO2 and TVOC levels
    if eco2 > 800 or tvoc > 2200 then
        device.digital.set_output("A0", true)
    else
        device.digital.set_output("A0", false)
    end

    -- Send the values to Superstack
    network.send_data {
        air_quality_index = aqi,
        carbon_dioxide = eco2,
        volatile_compounds = tvoc,
        humidity = humidity
    }

    -- Sleep for a few seconds
    device.sleep(3)
end

```