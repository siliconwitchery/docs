---
layout: default
title: S1 Module
nav_order: 1
parent: Hardware
has_children: true
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

An FPGA, Bluetooth Radio and Battery Management IC combined into a tiny and, *literally,* flexible module.

The module features several high speed busses for connecting many sensors or other devices, as well as adjustable power outputs for these devices with a focus on energy management for maximising battery life.

Of course the built in battery management allows for charging and monitoring, resulting in a clean and straightforward integration of the module into your final product. Only use the pins you need and ignore the rest.

The module comes preloaded with our SuperStack RTOS which allows anyone to remotely deploy algorithms, read sensors and store data, without the need to deal with any C code, or wireless encoding. Simply use our JSON API to send your request over Bluetooth and get a response back with your data.

SuperStack also supports asynchronous notifications, autonomous sleep, firmware updates and loading of your DSP algorithms onto the FPGA without the need to worry about system architecture of any of these features in your final product. Simply follow our API and get started with our browser based test tool today.

The compact and flexible module allows for tight integration into existing products where space is limited, or even sewn into garments and accessories using conductive thread to connect sensors across clothing.

## Features

- **Bluetooth 5.2** with Direction Finding
- **FPGA** with 5k LUT & DSP Blocks
- **Single Cell Battery Charger** with built in protection
- **Adjustable Output Voltage Rails**
- **4 Mb Flash Storage**
- **I3C Master** backward compatible with I2C
- **SPI Master** up to 8 Mbps
- **ADC**
- **GPIO** (Including differential & USB)
- **Solderable, Pluggable or Sewable**
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