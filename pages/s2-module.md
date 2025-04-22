---
title: S2 Module
description: Hardware datasheet for the LTE-enabled S2 Module
image: /assets/images/s2-module-annotated-masthead.png
nav_order: 2
last_modified_date: April 21th 2025, 13:07 UTC
---

# S2 Module
{: .no_toc }
{: .d-inline-block }
In development
{: .label .label-yellow }

{: .note }
This page is actively being updated. Information may change so be sure to check back frequently 

---

![Silicon Witchery S2 Module](/assets/images/s2-module-annotated-masthead.png)

The S2 is a production-ready IoT module built around an advanced ARM SiP with integrated LTE Cat-M1 connectivity. Featuring comprehensive I/O support (SPI, I2C, analog), built-in GNSS, and sophisticated power management with battery charging capabilities, it's designed for rapid deployment and remote development. The module comes pre-configured with a softsim and flexible data plan, eliminating cellular integration complexity. Engineers can program and debug directly over LTE using our Lua-based runtime environment, with all device management and updates handled through the Superstack platform – No local toolchain required.

## Feature summary
{: .no_toc}

### Hardware
{: .no_toc}
- ARM SiP with integrated LTE Cat-M1 and GNSS
- Built-in antenna supporting major LTE bands
- Multiple I/O: SPI, I<sup>2</sup>C, analog inputs, GPIO
- Advanced power management with battery charging
- Multiple power inputs with low power modes

### Connectivity
{: .no_toc}
- Pre-configured softsim with global coverage
- No-contract data plan included
- One-click device pairing

### Development
{: .no_toc}
- Over-the-air programming and debugging
- Lua-based runtime environment
- Zero-touch firmware updates and fleet management
- No local toolchain required

## Use cases
{: .no_toc}

### Industrial & Manufacturing
{: .no_toc}
- Remote equipment monitoring and predictive maintenance
- Environmental monitoring in factories
- Production line automation and monitoring

### Smart Agriculture
{: .no_toc}
- Crop monitoring and automated irrigation
- Livestock tracking and health monitoring
- Weather station networks

### Smart Cities & Infrastructure
{: .no_toc}
- Energy consumption optimization
- Environmental sensing networks
- Waste management optimization
- Occupancy monitoring
- Traffic flow monitoring

### Supply Chain & Logistics
{: .no_toc}
- Cold chain monitoring
- Asset tracking and management
- Warehouse automation
- Fleet tracking and diagnostics

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Block diagram

The S2 Module features two key devices:

- ARM Cortex-M33 System in Package with Cellular & GNSS - [Nordic nRF9151](https://docs.nordicsemi.com/bundle/ps_nrf9151/page/nRF9151_html5_keyfeatures.html)
- Power management IC with switching regulation & battery charging - [Nordic nPM1300](https://docs.nordicsemi.com/bundle/ps_npm1300/page/keyfeatures_html5.html)

The module includes all supporting circuitry such that no external hardware except a simple power source is needed to operate the device.

![Silicon Witchery S2 Module Hardware Block Diagram](/assets/images/s2-module-block-diagram.drawio.svg)

The device exposes a range of IO that can be used to connect external devices and features smart power management to run off either external power, or a single cell lithium polymer battery, saving power whenever possible. 

A single button is included for easy setup and two status LEDs indicate network and power status at a glance.

## Pinout

The S2 Module features six IO ports and three power ports. Digital IO is freely configurable across all ports, while analog inputs are limited to certain pins. A detailed description of all the pins are shown in the diagram below.

![Silicon Witchery S2 Module Top Pinout](/assets/images/s2-module-top-pinout-diagram.png)

The bottom of the module additionally exposes the same IO as the physical connectors such that the board can be mounted to a carrier PCB and electrically interfaced via pogo-pins. See the section on [mechanical dimensions](#mechanical-dimensions) for a recommended landing pattern.

![Silicon Witchery S2 Module Bottom Pinout](/assets/images/s2-module-bottom-pinout-diagram.png)

## Status LEDs & button

The on board button is only used for initial pairing of the device with the cloud. Once paired, the button has no other functionality. This is to prevent tampering of the device when in the field. If needed, the device can later be unpaired from within Superstack, and then paired again to a different deployment using the button.

The status LEDs meanwhile, indicate the networking and power status of the device throughout the lifetime of the application. 

![Silicon Witchery S2 Module Button and LEDs](/assets/images/s2-module-button-led-diagram.png)

The table below describes each of the LED states.

| Network LED | Meaning |
|-------------|---------|
| Slow blinking | Searching for LTE network
| Solid         | Network found – Not connected to deployment
| Fast blinking | Button pressed – Attempting to pair to deployment
| Off           | Connected & idle
| Short blinks  | Data transmission

| Power LED | Meaning |
|-----------|---------|
| Solid         | Battery charging or running on external power
| Off           | No battery detected and running on external power
| Slow blinking | Battery charged
| Fast blinking | Battery temperature too high

## LTE & GNSS connectivity

The S2 Module ships with **LTE Cat-M1** enabled with support for the following bands: **1**, **2**, **3**, **4**, **5**, **8**, **12**, **13**, **17**, **18**, **19**, **20**, **25**, **26**, **28**, **65**, **66** and **85**.

A softsim is pre-programmed into each module for included connectivity out of the box, where data allowance can be managed from inside the Superstack webapp.

The module also supports **GPS L1 C/A** and **QZSS L1 C/A** reception with a maximum accuracy of 2.0m in continuous tracking mode, or 3.4m in periodic tracking mode.

![Silicon Witchery S2 Module GNSS section](/assets/images/s2-module-lte-and-gnss-diagram.png)

To ensure optimal performance of the antennas, the antenna area must be kept clear of metal objects, and the module must not be placed inside an enclosed metal area. See the [antenna considerations](#antenna-considerations) for more details.

For optimum GPS accuracy, the antenna should have line of sight to open sky.

## Power & battery interface

## Programming

## Schematics

---

## Characteristics

### Absolute maximum ratings

### DC characteristics

### RF characteristics

## Mechanical dimensions

## Antenna considerations

## Packaging

## Compliance

### Approved bands

### Type certifications

---

## Terms of purchase