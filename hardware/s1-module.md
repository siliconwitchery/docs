---
layout: default
title: S1 Module
nav_order: 3
# parent: Hardware
# has_children: true
---

# S1 Wearable Module | **Datasheet**
{: .fs-9 }
{: .d-inline-block }
Preliminary
{: .label .label-yellow }

Bluetooth 5.2 Wearable Module with FPGA & Battery Management
{: .fs-6 .fw-300 }

---

![Silicon Witchery S1 Module]()

## Description 

An FPGA, Bluetooth Radio and Battery Management IC combined into one tiny form factor.

The S1 module features several high speed IO for connecting sensors or other devices, as well as adjustable voltage output rails for quickly building highly integrated solutions.

The built in battery management allows for charging and monitoring, resulting in a clean and straightforward integration of the module into your final product. Only use the pins you need and ignore the rest. No external component are required for basic operation, with crystals and decoupling capacitors are already integrated.

Should you wish to not develop your own wireless firmware, the module comes preloaded with our SuperStack RTOS which allows anyone to remotely deploy algorithms, read sensors and store data, without the need to deal with any C code. Simply use our JSON API over Bluetooth UART and get a response back with your data. There is ofcourse still the option to re-flash the Bluetooth IC with your own firmware should you choose over the Serial Wire Debug pins.

SuperStack also supports asynchronous notifications, autonomous sleep, firmware updates and loading of your DSP algorithms onto the FPGA without the need to worry about system architecture of any of these features. Simply follow our API and get started with our browser based WebBluetooth test tool (coming soon for Chrome and Edge).

The compact form factor allows for tight integration into existing products where space is limited with a total footprint is 6mm x 12mm and a thickness of just 1.6mm.

## Features

- **Bluetooth 5.2** with Direction Finding
- **FPGA** Lattice UP5k with 5k LUT & 8 MAC Blocks for DSP
- **Single Cell Battery Charger** with built in protection
- **User Adjustable Output Voltage Rails** up to 5.5V boost voltage
- **4 Mb User Flash Storage**
- **I3C IO** for use with I3C master IP
- **Dual hardware I2C/SPI blocks** for two concurrent serial buses
- **ADC** two lines
- **8 GPIO** (Including differential for USB)
- **<100μA Idle Current**
- **Preloaded Firmware** and [SuperStack]({{ site.baseurl }}{% link superstack/superstack.md %}) ready

## Applications
- Aggregation of many sensors
- Data Preprocessing at the Edge
- Remote Machine Learning
- Realtime ML Inferencing
- Bespoke AI algorithm deployment
- Bespoke DSP algorithm deployment
- Enabling IoT on non-connected devices
- Lightweight Battery Management
- General Wearable/IoT applications