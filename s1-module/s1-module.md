---
title: S1 Module
description: Hardware datasheet for the S1 Bluetooth-FPGA Module.
image: /images/annotated-module.png
nav_order: 2
last_modified_date: December 12th 2022, 13:56 UTC
---

# S1 Module
{: .no_toc }
{: .d-inline-block }
Active
{: .label}

![Silicon Witchery S1 Module](https://github.com/siliconwitchery/docs/raw/master/images/annotated-module.png)

The S1 module combines Bluetooth, FPGA and power management into a single module. It's intended for low power applications where the flexibility of an FPGA is required, while still having the conveniences of a wireless microcontroller.

With a footprint of just 6 x 11.5 x 1.6mm, the module can be integrated into small form factor products. The built in battery and power management further reduces the need for external components and can allow for incredibly integrated designs.

Simply connect a battery, and the module is fully operational.

The on board [Lattice iCE40 Ultra Plus](https://www.latticesemi.com/en/Products/FPGAandCPLD/iCE40UltraPlus) FPGA features 5k LUTs, 1Mb RAM, DSP blocks, PLL, and hardware serial blocks. 8 GPIO pins are exposed, including I3C capable IO and a differential pair for USB.

The main processor is a [Nordic nRF52811](https://www.nordicsemi.com/Products/Low-power-short-range-wireless/nRF52811) supporting Bluetooth 5.2,  Long Range, and Thread. The module includes an integrated antenna and two additional GPIO pins connected to the nRF52 which may be used as ADC channels, or wake from deep sleep triggers.

Power control and battery charging is managed from a dedicated [Maxim MAX77654 PMIC](https://www.maximintegrated.com/en/products/power/power-management-ics/MAX77654.html). The PMIC provides three adjustable voltage rails, one of which may be used as a buck-boost output and can provide up to 5.5V from a single lithium cell. The lithium cell may be charged and monitored directly from the module with a wide range of rate and safety options.

[32-Mbit of on board Flash](https://www.mouser.se/datasheet/2/590/AT25SL321_112-1385816.pdf) allow the FPGA binary to be stored on the module, as well as other user data which can be read or written to during runtime.

## Feature summary
{: .no_toc}
- **Bluetooth 5.2** support including Long Range.
- **Thread** support.
- **64MHz Cortex M4** processor.
- **FPGA** with 5k LUT and DSP blocks.
- **8x FPGA IO** including I3C and USB support.
- **2x nRF GPIO** pins with ADC and low power wake.
- **Lithium battery charging** and monitoring.
- **3x adjustable Vout rails** including 1x buck-boost up to 5.5V.
- **32-Mbit** flash storage.
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

The devices are fully supported internally including all RF, power and decoupling circuitry. Simply connecting a battery powers up the module and brings it into its normal operating mode.

It's recommended to study the [module schematics](#schematics) as well as the datasheets of each of the devices listed above to fully understand the features of the S1 Module.

## Pinout

![S1 Module pinout](/s1-module/images/s1-module-pinout.png)

| Pin Number | Signal                            | Direction | Description |
| :--------: | :-------------------------------: | :-------: | ----------- |
| 2 - 9      | D1 - D8                           | IO        | FPGA IO. These pins can be used as general purpose IO. They are all referenced to V<sub>IO</sub> and can be configured as push-pull, open drain/collector or tristates. Internal pull resistors may also be configured individually for each pin. Some pins provide extra functions as described below. |
| 2,5        | USBP / USBN                       | IO        | These FPGA pins can be used as a complimentary pair for USB data or other complimentary signals. |
| 8, 9       | I3C                               | IO        | These FPGA pins support high speed I3C with built in terminations and pull resistors. |
| 15, 16     | ADC1, ADC2                        | IO        | ADC pins connected directly to the nRF52. These pins can be used as GPIO or low power wake-up pins when the module is in deep sleep. These pins are referenced to the V<sub>ADC</sub> rail, typically 1.8V. |
| 10         | V<sub>CHG</sub>                   | I         | Main power input for the charging circuit. This pin can be used to power the module, typically from a 5V<sub>USB</sub> rail. |
| 11         | V<sub>BATT</sub>                  | IO        | A lithium cell can be connected to this pin, and will be charged whenever V<sub>CHG</sub> is applied. The module supports a wide range lithium technologies where both charge voltage and current may be configured in software to support each type. |
| 12         | V<sub>AUX</sub>                   | O         | Software configurable buck-boost rail which also powers the internal LDO exposed on V<sub>IO</sub>. Can be set up to 5.5V regardless of the input supply voltage. |
| 13         | V<sub>IO</sub>                    | O         | Software configurable 100mA LDO that can also be configured as a load switch. This pin acts as the logic reference for all of the FPGA IO and is limited to 3.6V. It is internally powered from the exposed V<sub>AUX</sub> rail which must also be enabled. |
| 17         | V<sub>nRF</sub> / V<sub>ADC</sub> | O         | 1.8V voltage rail powering the nRF52 and flash memory. Can be used to power external devices. When the ADC is used, this voltage also functions as the ADC reference output. |
| 1, 20, 14  | GND                               | –         | Ground. Pins 1 and 20 are close to the antenna and must connect to a good ground plane. Pin 14 aids as the return path for the power rails and battery charging. |
| 18         | SWDIO                             | IO        | Serial wire debug IO for the ARM core of the nRF52. Should not exceed the V<sub>NRF</sub> voltage. |
| 19         | SWDCLK                            | I         | Serial wire debug clock for the ARM core of the nRF52. Should not exceed the V<sub>NRF</sub> voltage. |

Download and print out a [S1 Module reference card](/s1-module/images/s1-module-pinout-card.png).

## Programming interface

### Programming the nRF52

The module may be programmed after assembly through the SWD pins located on pins 18 and 19. Many ARM Cortex debuggers are suitable such as the [J-Link probes](https://www.segger.com/products/debug-probes/j-link/).

![S1 Module JLINK connection diagram](/s1-module/images/s1-module-programming-interface.png)

Note, it is important that the interface voltage matches the voltage of the V<sub>nRF</sub> pin, otherwise the module may be damaged. Additionally, the module shouldn't be powered through the V<sub>nRF</sub> pin during programming, but rather through the V<sub>CHG</sub> or V<sub>BATT</sub> pins.

It is also possible to program the module using a [Nordic nRF52 development kit](https://www.nordicsemi.com/Products/Development-hardware/nrf52-dk) which includes an integrated J-Link debugger. Further details of this method can be found [here](https://infocenter.nordicsemi.com/index.jsp?topic=%2Fug_nrf52832_dk%2FUG%2Fnrf52_DK%2Fintro.html).

![Programming S1 Module using Nordic nRF development kit](/s1-popout-board/images/s1-nrfdk-wiring.jpg)

### Programming the FPGA

The module does not expose the FPGA programming interface directly. It is intended that the nRF52 dynamically updates the FPGA binary during runtime via the flash memory. Further details on this communication are detailed below. Examples of how the nRF52 firmware can be used to update the FPGA can be found in the GitHub examples. We suggest looking at the [S1 blinky project](https://github.com/siliconwitchery/s1-blinky-demo) to see how it works.

## nRF52, FPGA & memory intercommunication

The three devices are internally connected via SPI. The nRF52 controls overall communication flow, though communication is possible in any direction between the three devices. 

![Internal communication bus of the S1 Module](/s1-module/images/s1-internal-spi-interface.png)

In order to configure the FPGA with an application binary, the nRF52 must first load the binary onto the flash memory. After this, the FPGA will automatically use that binary after power cycling or resets. The procedure shown below describes this process.

1. FPGA core and IO voltages must be enabled from the PMIC.
1. The nRF52 pulls the FPGA reset line LOW.
1. The nRF52 issues a wake up sequence to the Flash via SPI.
1. The nRF52 programs the FPGA binary to the flash memory.
1. The nRF52 releases the SPI pins and sets its pins to high impedance.
1. The nRF52 pulls the FPGA reset line HIGH.
1. Once the FPGA DONE pin goes HIGH, the FPGA is ready.

Further details of this process can be found in the iCE40 Programming and Configuration [Technical note](https://www.latticesemi.com/view_document?document_id=46502).

After the flash is programmed, it remains so until erased. The nRF52 can at power-on check the flash contents and only update it if needed. While the nRF can hold an entire FPGA binary, it's recommended that this binary is downloaded over Bluetooth and saved directly to the flash. This saves space for the user application and Bluetooth stack.

After the FPGA is booted, the nRF52 may communicate with either the FPGA or flash directly on the same line. this can be achieved by using an inverted chip select for the FPGA application, while the flash remains as active low select.

The DONE pin may also be used after configuration as user defined pin.

In order for direct communication between the FPGA and flash, the nRF52 must keep its SPI pins at high impedance during the transfer.

## Power management

All of the internal devices of the S1 Module are powered from an ultra low power PMIC. This device contains a battery controller, buck-boost convertor with three independent outputs, low noise LDO, as well as software controls for adjusting many of the PMIC parameters.

The PMIC is I2C controlled from the nRF52 which allow the user to dynamically adjust power requirements on they fly.

![S1 Module power internal management](/s1-module/images/s1-power-management.png)

### Battery management

A wide range of lithium technologies are supported. The integrated battery charger can be configured for charge regulation voltages between 3.6V and 4.6V, as well as charging currents between 7.4mA, and 300mA. Various timing and rate controls are available, details of which can be found within the [MAX77654 datasheet](https://datasheets.maximintegrated.com/en/ds/MAX77654.pdf).

A battery monitoring output is also available for measuring battery voltage, current and consumption. It is internally routed to a third ADC pin on the nRF52.

### Power rails

The buck-boost rails can provide a total combined output current of 1A. The LDO is sourced from V<sub>AUX</sub> and can be used as either a low noise supply rail, or a load switch.

Each rail provides specific functions:

- V<sub>nRF</sub> - Main supply rail for the nRF52 and flash. This rail is typically 1.8V and can be used to support external 1.8V circuits. It is also the nRF ADC reference voltage when the ADC is set to use the VDD reference.
- V<sub>FPGA</sub> - Main supply rail for the FPGA core. This rail is typically 1.1V and is not externally exposed. It can be software controlled and totally shut down if the FPGA not is required.
- V<sub>AUX</sub> - User auxiliary rail. Can be set between 0.8 and 5.5V for external use. It also powers the LDO for V<sub>IO</sub>.
- V<sub>IO</sub> - This rail can either be used as a 100mA low noise LDO, or 100mA load switch. It also powers the FPGA IO bank for D1 - D8, and is limited to 3.6V.

The PMIC is highly configurable and full details can be found in the [MAX77654 datasheet](https://datasheets.maximintegrated.com/en/ds/MAX77654.pdf).

### Limitations

In order to avoid damage to the internal components of the module. Some constraints must be kept on the following rails.

- FPGA core voltage connected to **PMIC pin SBB1** must not exceed **1.42V**.
- FPGA IO voltage connected to **PMIC pin LDO0** must not exceed **3.6V**.
- nRF52 and flash voltage connected to **PMIC pin SBB2** must not exceed **2.4V**.

### Battery safety

Lithium batteries are of course dangerous if improperly handled. The MAX77654 features safety mechanisms to avoid battery related accidents, however it is possible to misconfigure the integrated power management IC to overvolt, undervolt or charge a lithium cell with too much current.

Precautions should be taken when developing software and changing configurations while a battery is in circuit. During development, it is recommended to measure current and voltage in situ, and add software safety measures to prevent misconfigurations that might damage the module, property, or persons nearby.

## Ratings

### Absolute maximum ratings

| Symbol                  | Parameter                                   | Min  | Max                    | Unit            |
| :---------------------: | ------------------------------------------- | :--: | :--------------------: | :-------------: |
| V<sub>CHG-MAX</sub>     | Charge input terminal voltage               | -0.3 | 30                     | V               |
| V<sub>BAT-MAX</sub>     | Battery terminal voltage                    | -0.3 | 6                      | V               |
| V<sub>AUX-MAX</sub>     | V<sub>AUX</sub> terminal voltage            | -0.3 | 6                      | V               |
| V<sub>IO-MAX</sub>      | V<sub>IO</sub> terminal voltage             | -0.3 | 3.6                    | V               |
| V<sub>nRF-MAX</sub>     | V<sub>nRF</sub> terminal voltage            | -0.3 | 2.4                    | V               |
| V<sub>FPGA-IO-MAX</sub> | Voltage on FPGA IO pins D1 - D8             | -0.5 | 3.6                    | V               |
| V<sub>nRF-IO-MAX</sub>  | Voltage on ADC1, ADC2 and SWD pins          | -0.3 | V<sub>nRF</sub>+0.3    | V               |
| I<sub>SYS</sub>         | Continuous current through module           | –    | 1.2                    | A<sub>RMS</sub> |
| T<sub>AMB-OP</sub>      | Operating temperature range                 | -40  | 85                     | °C              |
| T<sub>AMB-STG</sub>     | Storage temperature range                   | -40  | 125                    | °C              |

For detailed ESD performance and other parameters, see the datasheets of the individual devices. They are linked within the [Block diagram](#block-diagram) section above.

### Flash endurance and data retention

| Parameter                                        | Min     | Max                    | Unit   |
| ------------------------------------------------ | :-----: | :--------------------: | :----: |
| Flash IC erase / program cycles                  | 100,000 | –                      | Cycles |
| Flash IC data retention (full temperature range) | –       | 20                     | Years  |
| nRF IC erase / program cycles                    | 10,000  | –                      | Cycles |
| nRF IC data retention (40°C)                     | –       | 10                     | Years  |

### Sensitivity to light

The wafer level chip packages used on the module are sensitive to visible and near infrared light. Bright flashes of light such as from camera flashes may unintentionally trigger logic and malfunctions within the devices. In best case scenarios, this may result in lockups or resets, but in worst case, may damage internal circuitry. The final product design must shield the chips properly.

### DC characteristics

For accurate information it is recommended to check the individual IC datasheets as linked to from the [Block diagram](#block-diagram) section. There are many configurations and modes of the nRF52, FPGA, and PMIC which may result in different operating characteristics.

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
| V<sub>nRF</sub>      | Adjustable nRF52 / flash supply voltage range                | 1.7             | 2.2 **          | V    |
| I<sub>IO</sub>       | V<sub>IO</sub> maximum output current                        | –               | 50 / 100 \*\*\* | mA   | 
| I<sub>AUX</sub>      | V<sub>AUX</sub> maximum output current                       | –               | 1 \*\*\*\*      | A    |
| I<sub>nRF</sub>      | V<sub>nRF</sub> maximum output current                       | –               | 1 \*\*\*\*      | A    |

\* V<sub>IO</sub> is powered from V<sub>AUX</sub>. In LDO mode, V<sub>AUX</sub> must be 100mV higher than the desired V<sub>IO</sub> voltage. In load switch mode. V<sub>IO</sub> always matches V<sub>AUX</sub>.

\*\* Range is limited to avoid damage to the nRF52, Flash and FPGA which uses the respective rails.

\*\*\* I<sub>IO</sub> is dependent on  V<sub>AUX</sub> voltage and current availability. See [MAX77654 datasheet](https://datasheets.maximintegrated.com/en/ds/MAX77654.pdf) for full details.

\*\*\*\* Up to 1A of peak current can be shared across all of the combined power rails. These include V<sub>AUX</sub>, V<sub>nRF</sub> as well as the internal FPGA rail.

### RF characteristics 

| Symbol              | Parameter                        | Min  | Max  | Unit |
| :-----------------: | -------------------------------- | :--: | :--: | :--: |
| f<sub>OP</sub>      | Operating frequency range        | 2360 | 2500 | MHz  |
| fsk<sub>BPS</sub>   | On-the-air data rate             | 125  | 2000 | kbps |
| P<sub>RF</sub>      | Transmit power at nRF output pin | –    | 4    | dBm  |
| P<sub>SENS</sub>    | Receive sensitivity \*           | -91  | -104 | dBm  |
| A<sub>ANT-PK</sub>  | Integrated antenna peak gain     | –    | 3.5  | dBi  |
| A<sub>ANT-AVG</sub> | Integrated antenna average gain  | –    | -1.5 | dBi  |

\* Receiver sensitivity minimum specified at 2Mbps BLE ideal transmitter, and maximum specified at 125kbps long range BLE ideal transmitter. In between specifications can be found within the [nRF52811 datasheet](https://infocenter.nordicsemi.com/pdf/nRF52811_PS_v1.0.pdf).

## Schematics

The full schematics of the S1 Module. A PDF version can be downloaded [here](/s1-module/images/s1-module-schematic-rev-5.pdf).

![S1 Module Schematic](/s1-module/images/s1-module-schematic-rev-5.png)

## Footprint & layout

![S1 Module Footprint](/s1-module/images/s1-module-footprint-drawing.png)

Module footprint is symmetrical left-to-right. Ensure soldermask is present between the pads to prevent shorting. 

A cutout should be present on the carrier board to clear the passive components on the underside of the module.

### PCB considerations

To ensure good antenna performance, the antenna side of the module should be placed along the edge of the carrier PCB. A good ground connection should be made from pins 1 and 20 to the ground plane of the carrier PCB.

![S1 Module antenna edge placement on PCB](/s1-module/images/s1-antenna-edge-placement.png)

The area directly below the antenna should not contain any ground pour or signal traces, however on either side of the antenna, a ground fill is recommended.

![S1 Module antenna corner placement on PCB](/s1-module/images/s1-antenna-corner-clearance.png)

When the module cannot be placed centered to the board edge, it may be placed offset from a corner by 6mm.

In the case of highly integrated designs where the module must reside in a tight space, the module can still be used without heavy grounding, however nearby components such as batteries, metallic casings and fasteners should be kept as far away from the antenna as possible.

### Mechanical drawing

![S1 Mechanical Drawing](/s1-module/images/s1-module-mechanical-drawing.png)

Dimensions shown are in mm.

## Ordering information

### Packaging

Modules are supplied in ESD cartons with foam inserts. For reeling or tray options, contact Silicon Witchery [via email](mailto:info@siliconwitchery.com).

### Certification

The S1 Module is not yet pre-qualified for EMC compliance, however this status may change. For queries about certification status, contact Silicon Witchery [via email](mailto:info@siliconwitchery.com).

### Terms of purchase

The S1 Module and related software or development kits have not been or approved for life sustaining or other applications where failure may cause harm to human life, health or damage to property or equipment. Additionally, they have not been designed according to any standards in order to guarantee performance or accuracy. No responsibility is assumed by Silicon Witchery for its use, nor for any infringements of patents or other rights of third parties that may result from its use. These specifications are subject to change without notice.

No liability is held by Silicon Witchery for any delay or failure in performance arising as a result of any occurrence beyond its reasonable control, including but not limited to, capacity constraints, accident, act of God, labour disputes, civil commotion, war, medical outbreak, unanticipated manufacturing problems, shortage of energy, raw materials or other supplies, requirements or acts of any government or agency thereof, including trade embargoes or medical quarantines, judicial action and/or failure or delays in transportation.

Purchasing parties agree to take responsibility that any delivered hardware, software, documentation and/or other materials, tangible or otherwise, shall not be consigned, transferred, re-exported or sold to any party or person in any way that does not adhere to the most current Export Control Regulations (“Regulations”) of the European Union Dual Use Regulations, and the Export Administration Regulations of the United States of America.

Silicon Witchery may hold back from delivering goods, services, or any other materials in its position, if it suspects they may be used outside the accordance of these Regulations.

The Purchasing Parties agree to indemnify and hold harmless Silicon Witchery against any damages, costs, losses, and/or liabilities arising out of any non-compliance with Regulations.

Copyright 2022 © Silicon Witchery.