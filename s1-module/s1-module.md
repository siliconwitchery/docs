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
Launching Q4
{: .label}

![Silicon Witchery S1 Module](/images/annotated-module.png)

The S1 module combines Bluetooth, FPGA and power management into a single module. It's intended for low power applications where the flexibility of an FPGA is required, while still having the conveniences of a wireless microcontroller.

With a footprint of just 6 x 11.5 x 1.6mm, the module can be integrated into small form factor designs, without the need for extra power circuity due to the built in power management system.

Simply connect a battery, and the device is operational.

The FPGA used is a [Lattice iCE40 Ultra Plus](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus) featuring 5k LUTs, 1Mb RAM, DSP blocks, PLL, and hardware capable of SPI, I2C and I3C. 8 IO pins are exposed, including I3C capable IO and a differential pair for USB.

The Bluetooth device is a [Nordic nRF52811](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52811) with support for Bluetooth 5.2, Thread and long range capabilities. The module features an integrated antenna and clock circuity, and two ADC pins are exposed which can also be used as GPIO, or wake from sleep triggers.

Power control and battery charging is managed from a dedicated [Maxim MAX77654 PMIC](https://www.maximintegrated.com/en/products/power/power-management-ics/MAX77654.html). The device powers all the internal rails, and provides three external user adjustable voltage rails. One of the rails may be used as a buck-boost output and can provide up to 5V from a single LiPo source. Single lithium cells may be charged and monitored directly from the module with a wide range of rate and safety options.

[32Mbit of on board Flash](https://www.mouser.se/datasheet/2/590/AT25SL321_112-1385816.pdf) allow the FPGA binary to be stored on the module, as well as other user data which can be read or written to during runtime.

## Feature summary
{: .no_toc}
- **Bluetooth 5.2** including long range.
- **Thread** support.
- **64MHz Cortex M4** processor.
- **FPGA** with 5k LUT and DSP blocks.
- **8x GPIO** including I3C and USB support.
- **2x ADC/GPIO** pins with sleep/wake triggers.
- **Lithium battery charging** and monitoring.
- **3x Vout rails** adjustable including buck-boost modes.
- **32 Mb** flash storage.
- **Integrated antenna, passives and crystals**.

## Use cases
{: .no_toc}
- High speed & time critical DSP.
- Pre-processing data on the edge.
- Power efficient algorithm design.
- Parallel data processing.
- Realtime AI inferencing.
- Remote machine learning.
- Bespoke AI algorithm deployment.
- Bespoke DSP algorithm deployment.

## Contents
{: .no_toc}

1. TOC
{:toc}

## Block diagram

The S1 Module consists of four key devices:
- Bluetooth microcontroller - [Nordic nRF52811](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52811)
- Low power FPGA - [Lattice iCE40 Ultra Plus](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus)
- Power management IC - [Maxim MAX77654](https://www.maximintegrated.com/en/products/power/power-management-ics/MAX77654.html)
- 32-Mbit flash - [Adesto AT25SL321](https://www.mouser.se/datasheet/2/590/AT25SL321_112-1385816.pdf)
<br>
<br>
![S1 Module Block Diagram](/s1-module/images/s1-block-diagram.png)

The devices are fully supported internally, included antenna, decoupling, and clocking. Simply connecting a battery is enough to power and put the module into its normal operating mode.

To fully understand the inner workings of the module, it's recommended to study the module schematic shown in this datasheet, as well as the datasheets of each device linked above.

## Pinout

![S1 Module pinout](/s1-module/images/s1-module-pinout.png)

| Pin Number | Signal                            | Direction | Description |
| :--------: | :-------------------------------: | :-------: | ----------- |
| 2 - 9      | D1 - D8                           | IO        | FPGA IO. These pins can be used as general purpose IO. They are all referenced to V<subIO</sub> and can be configured as push-pull, open drain/collector or tristates. Internal pull resistors may also be configured within the FPGA individually for each pin. Some pins provide extra functions as described below. |
| 2,5        | USBP / USBN                       | IO        | These FPGA pins can be used as a complimentary pair for USB data or other complimentary signals. |
| 8, 9       | I3C                               | IO        | These FPGA pins support high speed I3C with built in terminations and pull resistors. |
| 15, 16     | ADC1, ADC2                        | IO        | ADC pins connected directly to the nRF52. These pins can be used as GPIO or low power wake-up pins when the module is in deep sleep. These pins are referenced to the V<sub>ADC</sub> rail, typically 1.8V. |
| 10         | V<sub>CHG</sub>                   | I         | Main power input for the charging circuit. This pin can be used to power the module, typically from a 5V<sub>USB</sub> rail. |
| 11         | V<sub>BATT</sub>                  | IO        | A lithium cell can be connected to this pin, and will be charged whenever V<sub>CHG</sub> is applied. The module supports many exotic lithium technologies and both voltage and current may be configured in software. |
| 12         | V<sub>AUX</sub>                   | O         | User configured buck-boost rail which also powers the internal LDO exposed on V<sub>IO</sub>. Can be set up to 5.5V regardless of the input supply voltage. |
| 13         | V<sub>IO</sub>                    | O         | User configurable 100mA LDO that can also be configured as a load switch. This pin acts as the logic reference for all of the FPGA IO and is limited to 3.6V. It is internally powered from the exposed V<sub>AUX</sub> rail which must also be enabled. |
| 17         | V<sub>nRF</sub> / V<sub>ADC</sub> | O         | Reference rail for the ADC pins, as well as the system voltage of the nRF52 device, and flash memory. This pin is typically 1.8V and can be used for powering external devices. |
| 1, 20, 14  | GND                               | –         | Ground. Pins 1 and 20 are close to the antenna and must connect to a good ground plane. Pin 14 aids as the return path for the power rails and battery charging. |
| 18         | SWDIO                             | IO        | Serial wire debug IO for the ARM core of the nRF52. Should not exceed the V<sub>NRF</sub> rail in voltage. |
| 19         | SWDCLK                            | I         | Serial wire debug clock for the ARM core of the nRF52. Should not exceed the V<sub>NRF</sub> rail in voltage. |

Download and print out a [S1 Module reference card](/s1-module/images/s1-module-pinout-card.png).

## Programming interface

### Programming the nRF52 device

The module may be programmed after assembly through the SWD pins located on pins 18 and 19. Many ARM Cortex debuggers are suitable such as the [J-Link probes](https://www.segger.com/products/debug-probes/j-link/).

![S1 Module JLINK connection diagram](/s1-module/images/s1-module-programming-interface.png)

Note, it is important that the interface voltage matches the voltage of the V<sub>nRF</sub> pin, otherwise the module may be damaged. Additionally, the module shouldn't be powered through the V<sub>nRF</sub> pin during programming, but rather through the V<sub>CHG</sub> or V<sub>BATT</sub> pins.

It is also possible to program the module using a [Nordic nRF52 development kit](https://www.nordicsemi.com/Products/Development-hardware/nrf52-dk) which includes an integrated J-Link debugger. Further details of this method can be found [here](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrf52832_dk%2FUG%2Fnrf52_DK%2Fintro.html).

![Programming S1 Module using Nordic nRF development kit](/s1-popout-board/images/s1-nrfdk-wiring.jpg)

### Programming the FPGA

The FPGA does not have any programming interface or JTAG externally exposed on the module. It it intended that the nRF52 dynamically updates the FPGA binary during runtime. Further details on this communication are detailed in the following section. Examples of how the nRF52 firmware can be used to update the FPGA can be found in the GitHub examples. We suggest looking at the [S1 blinky project](https://github.com/siliconwitchery/s1-blinky-demo) to see how it works.

## nRF52 - FPGA - memory intercommunication

The three devices are internally connected via SPI and some control signals. The nRF52 maintains overall control through the reset and chip select signals.

![Internal communication bus of the S1 Module](/s1-module/images/s1-internal-spi-interface.png)

In order to boot the FPGA, the nRF must first load a binary onto the flash memory. The following procedure describes the process.

1. PMIC enables the FPGA core and IO voltages.
1. nRF brings the FPGA reset line LOW.
1. nRF configures the SPI lines.
1. The flash wakeup sequence is issued over SPI.
1. The FPGA binary is programmed to the flash memory.
1. nRF releases control of the SPI and sets SPI pins to HiZ.
1. nRF brings the FPGA reset line HIGH.
1. Once the nRF detects the FPGA CDONE pin goes high, then the FPGA is ready.

Futher details of this process can be found in the [iCE40 Programming and Configuration Technical note](https://www.latticesemi.com/view_document?document_id=46502).

Once the flash is programmed, it remains so until erased. The nRF application can on power on check the flash contents and only update when needed. While the nRF can hold the entire FPGA application, it's recommended that this binary is downloaded dynamically over Bluetooth and saved directly to flash to save space for the user application and Bluetooth stack.

After the FPGA is booted, nRF may communicate with either the FPGA or Flash directly on the same line. this can be achieved by using an inverted chip select for the FPGA application, while the flash remains as active low select.

The CDONE pin may also be used after configuration as user defined pin.

In order for direct communication between the FPGA and flash IC, the nRF must release the SPI pins and keep them in HiZ.


## Power management

<mark>TODO update this

<mark>analog mux

### Limitations

In order to avoid damage to the internal components of the module. Some constraints must be kept on the following rails.

- FPGA core voltage connected on **PMIC pin SBB1** must not exceed **1.42V**.
- nRF52 / flash IC voltage connected on **PMIC pin SBB2** must not exceed **2.4V**.

### Battery safety

Lithium batteries are of course dangerous if improperly handled. The MAX77654 features safety mechanisms to avoid battery related accidents. However it is possible to misconfigure the integrated power management IC to overcharge/undercharge or charge the lithium battery with too much current.

Precautions should always be taken when working with software and changing configurations when the battery is in circuit. during development, it is recommended to develop battery related circuitry with proper current and voltage measurement in situ, and add software safety measures to prevent damage to the module, property, or persons nearby.

## Ratings

### Absolute maximum ratings

| Symbol                  | Parameter                                   | Min  | Max                    | Unit            |
| :---------------------: | ------------------------------------------- | :--: | :--------------------: | :-------------: |
| V<sub>CHG-MAX</sub>     | Charge input terminal voltage               | -0.3 | 30                     | V               |
| V<sub>BAT-MAX</sub>     | Battery terminal voltage                    | -0.3 | 6                      | V               |
| V<sub>AUX-MAX</sub>     | V<sub>AUX</sub> terminal voltage            | -0.3 | 6                      | V               |
| V<sub>IO-MAX</sub>      | V<sub>IO</sub> terminal voltage             | -0.3 | V<sub>AUX</sub>+0.3    | V               |
| V<sub>nRF-MAX</sub>     | V<sub>nRF</sub> terminal voltage            | -0.3 | 2.4                    | V               |
| V<sub>FPGA-IO-MAX</sub> | Voltage on FPGA IO pins D1 - D8             | -0.5 | 3.6                    | V               |
| V<sub>nRF-IO-MAX</sub>  | Voltage on nRF Pins ADC1, ADC2 and SWD pins | -0.3 | V<sub>nRF</sub>+0.3    | V               |
| I<sub>SYS</sub>         | Continuos system current through module     | –    | 1.2                    | A<sub>RMS</sub> |
| T<sub>AMB-OP</sub>      | Operating temperature range                 | -40  | 85                     | °C              |
| T<sub>AMB-STG</sub>     | Storage temperature range                   | -40  | 125                    | °C              |

For detailed ESD performance and other parameters, see the datasheets for the individual devices. They are linked within the Block Diagram section above.

### Flash endurance and data retention

| Parameter                                        | Min     | Max                    | Unit   |
| ------------------------------------------------ | :-----: | :--------------------: | :----: |
| Flash IC erase / program cycles                  | 100,000 | –                      | Cycles |
| Flash IC data retention (full temperature range) | –       | 20                     | Years  |
| nRF IC erase / program cycles                    | 10,000  | –                      | Cycles |
| nRF IC data retention (40°C)                     | –       | 10                     | Years  |

### Sensitivity to light

The wafer level chip packages used on the module are sensitive to visible and near infrared light. Bright flashes of light such as from camera flashes may unintentionally trigger logic and malfunctions within the devices. In best case scenarios, this may result in CPU lockups or resets, or in worst case, may damage internal circuitry. The final product design must shield the chips properly.

### DC characteristics

For accurate information it is recommended to check the individual IC datasheets as linked to from the Block Diagram section. There are many configurations and modes of both the nRF52, and FPGA which may result in different operating characteristics.

Some of the operating characteristics are listed here, but may not reflect all cases.

| Symbol               | Parameter                                                    | Min             | Max             | Unit |
| :------------------: | ------------------------------------------------------------ | :-------------: | :-------------: | :--: |
| V<sub>CHG</sub>      | Recommended charge in voltage                                | 4.1             | 7.25            | V    |
| V<sub>BAT-CHG</sub>  | Adjustable battery charge voltage range                      | 3.6             | 4.6             | V    |
| I<sub>BAT-CHG</sub>  | Adjustable battery charge current range                      | 7.5             | 300             | mA   |
| V<sub>BAT-PRE</sub>  | Adjustable battery pre-qualification threshold voltage range | 2.3             | 3.0             | V    |
| V<sub>IO-LDO</sub> * | Adjustable V<sub>IO</sub> output voltage in LDO mode         | 1.71            | 3.6 **          | V    |
| V<sub>IO-LSW</sub> * | Adjustable V<sub>IO</sub> output voltage in load switch mode | V<sub>AUX</sub> | V<sub>AUX</sub> | V    |
| V<sub>AUX</sub>      | Adjustable buck-boost output voltage range                   | 0.8             | 5.5             | V    |
| V<sub>nRF</sub>      | Adjustable nRF supply / ADC reference voltage range          | 1.7             | 2.2 **          | V    |
| I<sub>IO</sub>       | V<sub>IO</sub> maximum output current                        | –               | 50 / 100 \*\*\* | mA   | 
| I<sub>AUX</sub>      | V<sub>AUX</sub> maximum output current                       | –               | 1 \*\*\*\*      | A    |
| I<sub>nRF</sub>      | V<sub>nRF</sub> maximum output current                       | –               | 1 \*\*\*\*      | A    |

\* V<sub>IO</sub> is powered from V<sub>AUX</sub>. In LDO mode, V<sub>AUX</sub> must be 100mV higher than the desired V<sub>IO</sub> voltage. In load switch mode. V<sub>IO</sub> always matches V<sub>AUX</sub>.

\*\* Range is limited to avoid damage to nRF, Flash or FPGA which uses the respective rail.

\*\*\* I<sub>IO</sub> is a dependent on  V<sub>AUX</sub> voltage and current capability. See MAX77654 datasheet for details.

\*\*\*\* Up to 1A of peak current can be shared across all the combined power rails. These include V<sub>AUX</sub>, V<sub>nRF</sub> as well as the internal FPGA rail.

### RF characteristics 

| Symbol              | Parameter                        | Min  | Max  | Unit |
| :-----------------: | -------------------------------- | :--: | :--: | :--: |
| f<sub>OP</sub>      | Operating frequency range        | 2360 | 2500 | MHz  |
| fsk<sub>BPS</sub>   | On-the-air data rate             | 125  | 2000 | kbps |
| P<sub>RF</sub>      | Transmit power at nRF output pin | –    | 4    | dBm  |
| P<sub>SENS</sub>    | Receive sensitivity \*           | -91  | -104 | dBm  |
| A<sub>ANT-PK</sub>  | Integrated antenna peak gain     | –    | 3.5  | dBi  |
| A<sub>ANT-AVG</sub> | Integrated antenna average gain  | –    | -1.5 | dBi  |

\* Receiver sensitivity minumum specified at 2Mbps BLE ideal transmitter, and maximum specified at 125kbps long range BLE mode. In between specifications can be found within the nRF52811 datasheet.

## Schematics

<mark>TODO update this

![S1 Module Schematic](/s1-module/images/s1-schematic.png)

## Footprint & layout

<mark>TODO update this

![S1 Module Footprint](/s1-module/images/s1-footprint.png)

### PCB considerations

To ensure good antenna performance, the antenna side of the module should be placed along the edge of the carrier PCB and a good ground connection should be made from pins 1 and 20, to the ground plane on the carrier PCB.

![S1 Module antenna edge placement on PCB](/s1-module/images/s1-antenna-edge-placement.png)

The area directly below the antenna should not contain a ground pour or signal traces, however on either side of the antenna, a ground fill is recommended.

![S1 Module antenna corner placement on PCB](/s1-module/images/s1-antenna-corner-clearance.png)

When the module cannot be placed centered to the board edge, it may be placed offset from a corner by 6mm.

In the case of highly integrated designs where the module must reside in a tight space, the module can still be used without heavy grounding, however nearby components such as batteries, metallic casings and fasteners should be kept as far away from the antenna as possible.

### Mechanical drawing

<mark>TODO update this

![S1 Mechanical Drawing](/s1-module/images/s1-mechanical.png)

## Ordering information

### Packaging

The S1 module is currently supplied in ESD carton packaging options for small quantities. For reeling or tray options, contact [Silicon Witchery directly via email](mailto:info@siliconwitchery.com).

### Certification

The S1 Module is not yet pre-qualified for EMC compliance, however this status may change. For queries about certification status, contact [Silicon Witchery directly via email](mailto:info@siliconwitchery.com) for details.

### Terms of purchase

The S1 Module and related development kits designed by Silicon Witchery have not been or approved for life sustaining or other applications where failure may cause harm to human life, health or damage to property and equipment. Additionally, they have not been designed according to any standards in order to guarantee performance or accuracy. No responsibility is assumed by Silicon Witchery for its use, nor for any infringements of patents or other rights of third parties that may result from its use. These specifications are subject to change without notice.

No liability is held by Silicon Witchery for any delay or failure in performance arising as a result of any occurrence beyond its reasonable control, including but not limited to, capacity constraints, accident, act of God, labour disputes, civil commotion, war, medical outbreak, unanticipated manufacturing problems, shortage of energy, raw materials or other supplies, requirements or acts of any government or agency thereof, including trade embargoes or medical quarantines, judicial action and/or failure or delays in transportation (each, a “Force Majeure”).

Purchasing parties agree to take responsibility that any delivered hardware, software, documentation and/or other materials, tangible or otherwise, shall not be consigned, transferred, re-exported or sold to any party or person in any way that does not adhere to the most current Export Control Regulations (“Regulations”) of the European Union Dual Use Regulations, and the Export Administration Regulations of the United States of America.

Silicon Witchery may hold back from delivering goods, services, or any other materials in its position, if it suspects they may be used outside the accordance of these Regulations.

The Purchasing Parties agree to indemnify and hold harmless Silicon Witchery against any damages, costs, losses, and/or liabilities arising out of any non-compliance with Regulations.