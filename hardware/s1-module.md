---
layout: default
title: S1 Module
nav_order: 2
has_toc: false
---

# S1 Module | **Datasheet**
{: .fs-9 .no_toc }
{: .d-inline-block }
Preliminary
{: .label .label-yellow }

Bluetooth – FPGA – Battery Management – One Tiny Footprint
{: .fs-6 .fw-300 }

---

![Silicon Witchery S1 Module]()

## Contents
{: .no_toc .text-delta }

1. TOC
{:toc}

## General Description 

The S1 module combines an FPGA with wireless and battery management suitable for low power applicaions such as wearables or small IoT devices*. 

Occupying a volume of just 6 x 12 x 1.6mm, the device can be integrated into very small designs, with little to no external components. Ground and Vcc are the only required connections required for the device to function.

There are 8 exposed IO pins which go directly to the [Lattice ICE40UP5K](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus) FPGA. These pins may be used as general purpose IO, or serial lines. The FPGA contains two hardware SPI/I2C blocks routable to any pins, as well as I3C compatible IO for use with a user provided I3C IP block. The FPGA features 5280 LUTs, 1Mb of SPRAM and 8 DSP blocks.

The wireless portion of the module uses a [Nordic nRF52811](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52811) Bluetooth SoC featuring support for Bluetooth 5.2 (with direction finding) as well as Zigbee, Thread or Bluetooth Mesh. The SoC is user programmable via the exposed debug port, or may be preloaded with our [SuperStack]() Firmware should you choose. Additionally, 2 ADC lines are also conveniently exposed for general purpose use.

To manage power, the module contains a dedicated PMIC (Power management IC). It integrates a Li charger, battery monitor (via an nRF52811 ADC pin), three buck-boost regulator outputs and one LDO regulator output. All of which are independently configurable. This architecture allows the module to output several voltage rails for external circuits, one of which can be boosted to 5.5V, even from a single Lithium cell. Additionally, the voltage rails may be dynamically adjusted or switched off all-together to save power.

Finally, 4Mb of on board flash storage is availble for holding the FPGA boot data, and any remaining space may be used for user application data.

The device hardare design is open source and is licensed under a [Creative Commons Attribution 4.0 International License](http://creativecommons.org/licenses/by/4.0/).

### Features

- **Bluetooth 5.2** Supporting Direction Finding
- **5k FPGA** with 8 DSP Blocks & Two Serial Drivers
- **4 Mb** Flash Storage
- **8 GPIO** Pins
- **2 ADC** Pins
- **4 Configurable Voltage Outputs**
- **Li Battery Charger**
- **No External Passive Components Needed**

### Use Cases
- High Speed & Time Critical Sensor DSP
- Lower Power Data Pre-Processing
- Parallel Data Processing
- Realtime AI Inferencing
- Remote Machine Learning
- Bespoke AI Algorithm Deployment
- Bespoke DSP Algorithm Deployment

### Applications

- Wearable Devices
- Small Form Factor IoT Devices
- Implantable or Medical Devices**
- Remote Interfacing & Sensing
- Sensor Data Collection & ML Data Labeling

**Our devices and components used within are not pre-qualified for any kind of regulatory requirements, medical or life support applications. You will need to fully qualify the device in order to use it in such applications and take complete responsibility fully indemnifying Silicon Witchery AB for any failure arising from use of our devices or software.

---

## Block Diagram

![S1 Module Block Diagram]({{ site.baseurl }}{% link hardware/s1-module-images/s1-block-diagram.png %})


---

## Pinout

![S1 Module Pinout]({{ site.baseurl }}{% link hardware/s1-module-images/s1-pinout-diagram.png %})

---

## Wireless Radio

### Programming Interface

### ADC

### FPGA & Flash Storage Interface

### Power Options

### Recommended Tools & Software



---

## FPGA

### Programming Interface

### Auto-Boot

### IO

### Power Options

### Recommended Tools & Software



---

## Flash Storage



---

## Power Management

### How to not Blow Up the Module

### Battery Charging

### Buck-Boost Supplies

### Low Dropout Regulator

---

## Ratings

### Absolute Maximum Ratings

|                   |                               | Min   | Max   | Unit  |
|:------------------|:------------------------------|:------|:------|:------|
|V<sub>CHG-MAX</sub>| Charge input terminal voltage |       |       |  V    |
|V<sub>BAT-MAX</sub>| Battery terminal voltage      |       |       |  V    |
|V<sub>IO-MAX</sub> | Bus/GPIO voltage              |       |       |  V    |
|V<sub>ADC-MAX</sub>| ADC voltage                   |       |       |  V    |
|P<sub>VO1</sub>    | V<sub>OUT1</sub> power draw   |       |       |  W    |
|P<sub>VO2</sub>    | V<sub>OUT2</sub> power draw   |       |       |  W    |
|T<sub>amb</sub>    | Operating ambient temperature |       |       | °C    |
|T<sub>stg</sub>    | Storage temperature           |       |       | °C    |

### Electrostatic Discharge (ESD)

|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|V<sub>ESD-HBM</sub>| ESD - Human body model        |       |  V    |
|V<sub>ESD-CDM</sub>| ESD - Charged device model    |       |  V    |


### Thermal Information

V<sub>CHG</sub> = 0V, V<sub>BAT</sub> = 3.7V unless specified

|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|T<sub>RF</sub>| 1Mbps cont. TX radio temperature * |       |  °C   |
|T<sub>RF+FPGA</sub>| Full speed FPGA temperature * |       |  °C   |
|T<sub>CHG</sub>| Charge IC temperature V<sub>CHG</sub> = 5V * |   | °C  |

\* lab measured values

### DC Characteristics & Power Consumption

|                   |                               | Min   | Max   | Unit  |
|:------------------|:------------------------------|:------|:------|:------|
|V<sub>CHG</sub>    | Charger supply voltage        |       |       |  V    |
|V<sub>BAT</sub>    | Battery input voltage         |       |       |  V    |
|V<sub>BAT-CV</sub> | Charge constant voltage range |       |       |  V    |
|I<sub>BAT-CC</sub> | Charge constant current range |       |       |  mA   |
|V<sub>VO1</sub>    | Configurable rail 1 V range   |       |       |  V    |
|V<sub>VO1</sub>    | Configurable rail 1 current   |       |       |  mA   |
|V<sub>VO2</sub>    | Configurable rail 2 V range   |       |       |  V    |
|I<sub>VO2</sub>    | Configurable rail 2 current   |       |       |  mA   |
|V<sub>ADC</sub>    | Usable ADC range              |       |       |  V    |
|I<sub>IO</sub>     | GPIO/Bus current source/sink  |       |       |  mA   |
|I<sub>sleep</sub>  | Sleep mode current            |       |       |  mA   |
|I<sub>RF-TX</sub>  | RF TX mode current            |       |       |  mA   |
|I<sub>RF-RX</sub>  | RF RX mode current            |       |       |  mA   |
|I<sub>FPGA</sub>   | FPGA active current           |       |       |  mA   |

### RF Characteristics 

|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|V<sub>ESD-HBM</sub>| Max transmit power            | +4    |  dBm  |
|V<sub>ESD-CDM</sub>| Receive sensitivity           | -96   |  dBm  |
|V<sub>ESD-CDM</sub>| Whip antenna gain             | 3     |  dBi  |


---

## Footprint & Layout

### PCB Footprint Guide

### Antenna Considerations

### Mechanical Drawing

---

## Firmware Information



---

## Ordering Information



---

## Schematics & PCB Design