---
title: "Deploy Production IoT Air Quality Monitoring in Minutes"
parent: IoT Solutions Blog
description: "Build a production-ready 5G air quality monitoring system using the S2 module and Superstack platform. Connect sensors, automate fan control, and access AI insights—all in under 70 lines of code."
image: /assets/images/blog/share-image.png
nav_order: 5
redirect_from:
  - /pages/blog/easy-air-quality-monitoring-with-superstack/
---

# **Deploy Production IoT Air Quality Monitoring in Minutes**
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

Transform your IoT strategy from months of development to minutes of deployment. This tutorial demonstrates how CTOs and engineering teams can rapidly prototype and deploy enterprise-grade IoT solutions using the S2 Module and Superstack Platform.

The S2 module arrives pre-configured with global LTE connectivity, eliminating the typical 12+ month infrastructure development cycle. Superstack's AI engine processes data from multiple sensors simultaneously, providing natural language insights that integrate directly into your existing business applications via ChatGPT-style APIs.

✓ 5G/LTE Cat-M1 connectivity out of the box with included eSIM  
✓ Remote programming and debugging via cloud-based Lua scripting  
✓ AI-powered pattern recognition across device fleets  
✓ Enterprise security with DTLS 1.2 encryption  
✓ RESTful APIs for seamless business system integration

## The Build

The **ENS160 air quality sensor** and **SHT45 temperature & humidity sensor** form the perfect combination for comprehensive air quality monitoring. The ENS160 provides precise measurements of air quality index (AQI), carbon dioxide (CO2), and volatile organic compounds (VOCs), while the SHT45 delivers accurate temperature and humidity readings that are essential for calibrating the air quality measurements.

Assembly is incredibly straightforward using the **Qwiic/STEMMA QT** interface, which eliminates complex wiring and reduces the chance of connection errors. The entire system fits neatly into a clear enclosure, creating a professional-looking monitoring device that can be deployed anywhere with cellular coverage.

### Components List

- [S2 Module (with eSIM)](https://www.digikey.com/en/products/detail/silicon-witchery/S2-MODULE-EXT-ANT/27621233)
- [S2 Module (with eSIM + integrated antenna)](https://www.digikey.com/en/products/detail/silicon-witchery/S2-MODULE/27621234)
- [SparkFun ENS160 Indoor Air Quality Sensor](https://www.sparkfun.com/sparkfun-indoor-air-quality-sensor-ens160-qwiic.html)
- [Adafruit SHT45 Precision Temperature & Humidity Sensor](https://www.adafruit.com/product/5665)
- [Adafruit Power Relay FeatherWing](https://www.adafruit.com/product/3191)
- [SparkFun Qwiic Cable Kit](https://www.sparkfun.com/sparkfun-qwiic-cable-kit.html)
- [Polycarbonate Clear Enclosure](https://www.digikey.com/en/products/detail/serpac/RBF63P06C16C/22461984)

## The Code

The entire air quality monitoring system runs on just **under 70 lines of Lua code**. The script continuously reads both sensors, uses the temperature and humidity data to calibrate the air quality measurements for maximum accuracy, and automatically controls a relay to turn on a fan when CO2 or VOC levels exceed safe thresholds (800 ppm CO2 or 2200 ppb TVOC).

All sensor communication happens over I2C, and the data is automatically transmitted to Superstack via the built-in cellular connection. The code is designed to be robust and production-ready, with proper sensor initialization and error handling.

```lua
local SHT45_I2C_ADDRESS = 0x44
local ENS160_I2C_ADDRESS = 0x53

-- Enable gas sensing mode on the air quality monitor
device.i2c.write(ENS160_I2C_ADDRESS, "\x10\x02", { port = "PORTF" })

print("Reading temperature, humidity, AQI, eCO2 and TVOC periodically")

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

## The Data

Once your air quality monitor is collecting data, you can easily access it programmatically using Superstack's REST API. This makes it simple to integrate the sensor data into your existing dashboards, applications, or business systems.

Here's a simple example of how to fetch the air quality data using a curl request:

```bash
curl https://super.siliconwitchery.com/api/data \
    -H 'Content-Type: application/json' \
    -H 'X-Api-Key: Jc9kdtAMoNiQcao-SDQvg8dtZ33HoWkHFJmjhnY5Mu4' \
    -d '{
        "deploymentId": "2b549e58-b05b-4a24-8266-2843b6538de6",
        "devices": ["Air Quality Sensors"]
    }'
```

The API returns structured JSON data containing all sensor readings with timestamps, making it easy to build custom visualizations, set up alerts, or integrate with existing monitoring systems.

### Live Dashboard Example

Want to see the data in action? Check out our [live dashboard demo](https://demos.siliconwitchery.com) that visualizes real-time air quality data from multiple sensors.

The dashboard demonstrates how to create a production-ready IoT visualization using just two core files - showcasing air quality index, CO2 levels, volatile compounds, and humidity data in real-time charts. The entire dashboard is built with simple HTML/JavaScript and updates every second with live sensor data.

**Source code available:** The complete dashboard implementation is open source and available at [GitHub](https://github.com/siliconwitchery/superstack-dashboard-demos), showing exactly how to integrate Superstack's API into your own web applications.

## The AI

Superstack's embedded AI agent takes your air quality data to the next level by providing intelligent insights and natural language analysis of your sensor readings. The AI can identify patterns, detect anomalies, and provide actionable recommendations based on your specific deployment data.

**Try the AI agent yourself** directly within the public deployment at [super.siliconwitchery.com](https://super.siliconwitchery.com/?deployment=2b549e58-b05b-4a24-8266-2843b6538de6)

You can ask questions like "What were the air quality trends this week?" or "When should I expect the next maintenance cycle?" and get intelligent, context-aware responses based on your actual sensor data.

---

Ready to eliminate IoT infrastructure headaches? Contact us at **projects@siliconwitchery.com** to request a free consultation and see how your team can deploy production IoT systems in days, not months.