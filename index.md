---
layout: default
title: Introduction
nav_order: 1
---

# Silicon Witchery/SuperStack Docs
{: .fs-9 }

An Ultra Low Power IoT Sensor Platform. Designed for AI on the Edge.
{: .fs-6 .fw-300 }

[Download Latest Binary](#){: .btn .btn-primary .fs-5 .mb-4 .mb-md-0 .mr-2 } [Order a development kit](#){: .btn .fs-5 .mb-4 .mb-md-0 }

---

## In a nutshell

The Silicon Witchery ecosystem makes IoT more capable than ever.
- Deploy your custom algorithms to the edge
- Integrate easily with our built in wireless
- No coding or translation needed between cloud and device
- Built in and best in-class low power battery management

## S1 Wearable Module

Our dedicated platform is based on a powerful trio of ICs tightly integrated into a flexible circuit board which can be soldered, socketed or even sewn into garments.

![Image of module](#)

### Wireless

The S1 features Bluetooth 5.2 wireless with a preconfiguered and easy to use set of Bluetooth Service Characteristics. Additionally this includes:
- Bluetooth LE to 5.2 fully compliant connectivity ready for iOS/Android integration
- Bluetooth Angle of Arrival direction finding
- Translationless JSON serial interface
- Advertising payloads for single gateway to many device operation.
- Configurable sleep modes for best power consumption

### FPGA Fabric

At the heart of the S1 module, a 5k LUT FPGA allows you to deploy custom algorithms and AI/ML models easily for realtime operation. Simply package your bitstream and use our wireless API to remotely deploy your model to the edge.

Some examples of what the device can be used for:
- Realtime sensor aggrigation of many distributed sensors
- Realtime processing of sensor data with DSP operations
- AI edge learning algorithms for creating ML models
- ML model deployment for realtime infrencing
- Preprocessing of personal data on the edge for user confidence and security before uploading to the cloud

### Battery & Power Controller

To round it all off, the S1 features best in class power and charge management which is highly user configurable. The adjustable charge voltage supports many single cell technologies including Li-Ion, Li-Poly and Li-Ceramic batteries, as well as the option to disable charging all together for use with single use batteries such as Lithium or Zinc button cells.

A built in multi output boost convertor allows for up to two user configurable voltage up to 5V from a sinlge cell. This is userful for driving LEDs in heart rate or pulse oximetry sensors.

Finally the device features numerous low power modes to ensure your application runs just as you need without wasting energy under idle.

### Flexible IO

The S1 is loaded with a magnitude of IO for connecting sensors and other interfaces. It can attached in multiple configurations, ranging from IO requirements, to high speed data transfer. See our [S1 Module Product Page](#) for detailed specifications.

## SuperStack

A custom low power embedded operating system designed specifically for our range of modules.

SuperStack is designed to be easy but still allow for advanced embedded functionality which would normally require dedicated development.

