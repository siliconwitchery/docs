---
title: S1 ECG Kit
description: An all-in-kit to build and test heart algorithms with ease.
image: images/annotated-ecg-kit.png
nav_order: 4
last_modified_date: 21st October 2021, 03:51 PM
---

# S1 ECG Kit
{: .no_toc }
{: .d-inline-block }
Launching Q4
{: .label .label-blue }

A powerful analog frontend combined with the S1 Module makes this an all-in-one kit to deploy and test algorithms with ease. Be that for learning, research, or as the starting point for your next product.

---

![Silicon Witchery S1 ECG Reference Kit](/images/annotated-ecg-kit.png)

---

**Applications**

- Learning and teaching around heart health
- Researching ML based ECG algorithms
- Wireless data logging
- New product development

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## S1 Module

The built-in S1 Module is designed for IoT projects where performance is key, yet space and power constraints cannot be compromised.

**It features a clever combination of four ICs.**

- A Bluetooth 5.2 SoC
- An FPGA designed for low power AI/ML
- A complete battery management IC
- And 32Mb of flash memory

Additionally, the module breaks out high speed IO and several adjustable power rails so that your design can remain compact.

To read more about the S1 Module, be sure to check out the full datasheet [here](/s1-module/s1-module).

---

## Block Diagram

The block diagram below shows the simplistic nature of devices built with the S1 Module.

This design features a single ECG frontend amplifier as the only active external component in the system. All other processing is done within the S1 Module.

![S1 ECG kit system block diagram](/s1-ecg-kit/images/s1-ecg-kit-block-diagram.png)

---

## ECG Frontend

The ECG frontend is based on the Analog Devices [AD8233](https://www.analog.com/en/products/ad8233.html). It contains low noise signal conditioning for amplifying ECG signals along with leads-off detection to allow for auto-sleep when the probes are not in contact with the skin.

The S1 ECG kit makes full use of the device by exposing all three probes (two on the front, and one on the back) which come into contact with the user when they hold the board with both hands.

The leads-off detection allows for automatic sleep-wake depending on if the user is holding the device. Application targeted for low power can therefore be designed using the board.

---

## Built-in Battery

For ease of portability, as well as low noise measurements. The board features a build in 150mAh lithium battery. The battery charges automatically when the USB-C is connected. Thanks to the auto-sleep features, there is no need for any power switch, and the device can retain its charge for weeks in standby.

A 0.1" jumper and pin header is exposed on the back of the board for measuring the battery current (both charging and discharging) during development.

**WARNING** The S1 ECG Kit standard firmware comes with the appropriate settings configured for safely charging the included lithium battery. These settings should be changed with care as higher charge currents and voltages can be set which may damage the battery and risk fire. If in doubt, the current sense jumper should be removed which will fully disconnect the battery from the S1 charge circuit.

--- 

## LEDs & IO

---

## Programming



---

## Schematic

The complete schematic for the S1 ECG Kit is shown below. A PDF version is available [here](https://github.com/siliconwitchery/s1-ecg-demo/blob/3a8f1f18de6bf9068e17d3fa44eaa844272473b1/schematic.pdf).

![S1 ECG kit schematic](/s1-ecg-kit/images/s1-ecg-kit-schematic.png)

---

## Design Files & Source Code

All the design files can be found within the S1 ECG Kit [repository](https://github.com/siliconwitchery/s1-ecg-demo).

---

## Suitability for Critical Applications

The S1 ECG Kit is intended for development, and is not verified for real medical use where performance and accuracy would be critical to human health and well-being.

Additionally, it has not been designed according to any standards in order to guarantee performance or accuracy. No responsibility is assumed by Silicon Witchery for its use.

---

## Licence

**This design is released under the [Creative Commons Attribution 4.0 International](https://creativecommons.org/licenses/by/4.0/) Licence.**

This is a human-readable summary of (and not a substitute for) the [license](https://creativecommons.org/licenses/by/4.0/legalcode).

### You are free to:
{: .no_toc }

**Share** — copy and redistribute the material in any medium or format

**Adapt** — remix, transform, and build upon the material
for any purpose, even commercially.

The licensor cannot revoke these freedoms as long as you follow the license terms.

### Under the following terms:
{: .no_toc }

**Attribution** — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.

**No additional restrictions** — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

### Notices:
{: .no_toc }

You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.

No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.