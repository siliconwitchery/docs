---
title: S1 Module
description: Hardware datasheet for the S1 Bluetooth-FPGA Module.
image: images/annotated-module.png
nav_order: 2
last_modified_date: 21st October 2021, 12:51 PM
---

# S1 Module
{: .no_toc }
{: .d-inline-block }
Launching Q4 - Preliminary datasheet
{: .label}

Bluetooth – FPGA – Battery Management – One Tiny Footprint
{: .fs-6 .fw-300 }

---

![Silicon Witchery S1 Module](/images/annotated-module.png)

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## General Description 

The S1 module combines an FPGA with wireless and battery management suitable for low power applications such as wearables or small IoT devices*. 

Occupying a volume of just 6 x 12 x 1.6mm, the device can be integrated into very small designs, with little to no external components. Ground and Vcc are the only required connections required for the device to function.

There are 8 exposed IO pins which go directly to the [Lattice ICE40UP5K](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus) FPGA. These pins may be used as general purpose IO, or serial lines. The FPGA contains two hardware SPI/I2C blocks rotatable to any pins, as well as I3C compatible IO for use with a user provided I3C IP block. The FPGA features 5280 LUTs, 1Mb of SPRAM and 8 DSP blocks.

The wireless portion of the module uses a [Nordic nRF52811](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52811) Bluetooth SoC featuring support for Bluetooth 5.2 (with direction finding) as well as Zigbee, Thread or Bluetooth Mesh. The SoC is user programmable via the exposed debug port, or may be preloaded with our [SuperStack]() Firmware should you choose. Additionally, 2 ADC lines are also conveniently exposed for general purpose use.

To manage power, the module contains a dedicated PMIC (Power management IC). It integrates a Li charger, battery monitor (via an nRF52811 ADC pin), three buck-boost regulator outputs and one LDO regulator output. All of which are independently configurable. This architecture allows the module to output several voltage rails for external circuits, one of which can be boosted to 5.5V, even from a single Lithium cell. Additionally, the voltage rails may be dynamically adjusted or switched off all-together to save power.

Finally, 4Mb of on board flash storage is available for holding the FPGA boot data, and any remaining space may be used for user application data.

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

![S1 Module Block Diagram](/s1-module/images/s1-block-diagram.png)


---

## Pinout

![S1 Module Pinout]({{ site.baseurl }}{% link s1-module/images/s1-pinout-diagram.png %})

|       Pin Number       |       Signal        | Direction | Description                                                  |
| :--------------------: | :-----------------: | :-------: | ------------------------------------------------------------ |
|       1, 20, 14        |         GND         |     –     | Ground. Pins 1 and 20 are close to the antenna and must connect to a good ground plane for optimal antenna performance. Pin 14 isn't as critical, however is strongly recommended when high currents may be required from the power rails, or when using the battery charging feature. |
|           2            |        USBN         |    IO     | USB data – signal. May be used as general purpose complementary IO. |
|           5            |        USBP         |    IO     | USB data + signal. May be used as general purpose complementary IO. |
| 2, 3, 4, 5, 6, 7, 8, 9 |       D1 - D8       |    IO     | General purpose IO pins directly connected to the FPGA. Signal voltage range is set internally to the V<sub>IO</sub> pin. |
|           10           |   V<sub>CHG</sub>   |     I     | Main power input                                             |
|           11           |  V<sub>BATT</sub>   |    IO     |                                                              |
|           12           |   V<sub>AUX</sub>   |     O     |                                                              |
|           13           |   V<sub>IO</sub>    |     O     |                                                              |
|         15, 16         |     ADC1, ADC2      |   I(O*)   |                                                              |
|           17           | V<sub>nRF/ADC</sub> |     O     |                                                              |
|           18           |        SWDIO        |    IO     |                                                              |
|           19           |       SWDCLK        |     I     |                                                              |



---

## Wireless Radio

### Programming Interface

<mark>The S1 Module comes pre-programmed with the [SuperStack]() Runtime so do not need factory programming if a custom Bluetooth application is not required.

However it is possible to program or re-program the S1 module via the exposed programming pins.

![S1 Module JLINK Connection Diagram]({{ site.baseurl }}{% link s1-module/images/s1-jlink-pinout.png %})

### ADC

### FPGA & Flash Storage Interface

### Power Options

### Recommended Tools & Software



---

## FPGA

### Programming Interface
The FPGA bitstream is written to the onboard flash using the nRF chip. The makefile handles this in the [S1 Blinky](https://github.com/siliconwitchery/s1-blinky-demo), and can be invoked as:
```
make build-verilog NRF_SDK_PATH=path_to_nrf5sdk GNU_INSTALL_ROOT=path_to_gcc
```
Alternately, you can use the configured tasks on VSCode. Note that the FPGA bitstream cannot be uploaded in an application using Softdevice, due to flash size constraints.

### Auto-Boot

### IO

### Power Options

### Recommended Tools & Software

- [yosys](https://yosyshq.net/yosys/download.html), [icestorm & NextPNR](http://www.clifford.at/icestorm/).
- Optionally [gtkwave](http://gtkwave.sourceforge.net) and [iVerilog](http://iverilog.icarus.com) are useful for simulation and verification.

MacOS - We recommend using [homebrew](https://brew.sh) along with our [brew formula](https://github.com/siliconwitchery/homebrew-oss-fpga) to install everything.

Windows - Most of these tools are available as installers, but some of them might need Cygwin or similar. It's best to Google how to do this, and we will update this page once we've tested it.

Linux - Most of these tools are available from standard package managers, but you can build them for source quite easily.



---

## Flash Storage



---

## Power Management

The S1 Module comes with a MAX77654 power management IC, with a buck-boost regulated outputs and a built-in LDO. The PMIC interfaces with the nRF52811 over I2C and a ADC line for battery monitoring.

### How to not Blow Up the Module
We recommend you use the helper functions from the [s1-sdk](https://github.com/siliconwitchery/s1-sdk). However, if you wish to manually modify PMIC settings, ensure that:
- FPGA core voltage is at 1.1V
- nRF voltage is at 1.8V (limited by flash chip)

### Battery Charging
which regs enable battery charging

### Buck-Boost Supplies

### Low Dropout Regulator

---

## Ratings

### Absolute Maximum Ratings

|                   |                               | Min   | Max   | Unit  |
|:------------------|:------------------------------|:------|:------|:------|
|V<sub>CHG-MAX</sub>| Charge input terminal voltage | -0.3  |  30   |  V    |
|V<sub>BAT-MAX</sub>| Battery terminal voltage      | -0.3  |   6   |  V    |
|V<sub>IO-MAX</sub> | Bus/GPIO voltage              | -0.3  |  2.1  |  V    |
|V<sub>ADC-MAX</sub>| ADC voltage                   | -0.3  |  2.1  |  V    |
|P<sub>VO1</sub>    | V<sub>OUT1</sub> power draw   |       |       |  W    |
|P<sub>VO2</sub>    | V<sub>OUT2</sub> power draw   |       |       |  W    |
|T<sub>amb</sub>    | Operating ambient temperature | -40   |  85   | °C    |
|T<sub>stg</sub>    | Storage temperature           | -40   |  125  | °C    |

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

### DC Characteristics & Power Consumption TODO

|                   |                               | Min   | Max   | Unit  |
|:------------------|:------------------------------|:------|:------|:------|
|V<sub>CHG</sub>    | Charger supply voltage        |  4.1  |  7.25 |  V    |
|V<sub>BAT</sub>    | Battery input voltage         |  3.6  |  4.6  |  V    |
|V<sub>BAT-CV</sub> | Charge constant voltage range |  3.6  |  4.6   |  V    |
|I<sub>BAT-CC</sub> | Charge constant current range | 7.5   |  300  |  mA   |
|V<sub>VO1</sub>    | Configurable rail 1 V range   |       |       |  V    |
|V<sub>VO1</sub>    | Configurable rail 1 current   |       |       |  mA   |
|V<sub>VO2</sub>    | Configurable rail 2 V range   |       |       |  V    |
|I<sub>VO2</sub>    | Configurable rail 2 current   |       |       |  mA   |
|V<sub>ADC</sub>    | Usable ADC range              |       |  0.6  |  V    |
|I<sub>IO</sub>     | GPIO/Bus current source/sink  |   1   |   4   |  mA   |
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

![S1 Module Footprint](/s1-module/images/s1-footprint.png)
![S1 Module Pads](/s1-module/images/s1-pad-dim.png)

### PCB Footprint Guide

### Antenna Considerations
The antenna should ideally be placed on the host PCB’s longest edge at the centre. Where the centre is not a viable option, the antenna can be placed offset on the PCB to within  the  limits  shown  below.  A  minimum  of  6mm  from  either  PCB  edge should  be observed. Where possible this distance should be greater than 6mm.

### Mechanical Drawing

---

## Firmware Information



---

## Ordering Information



---

## Schematics & PCB Design