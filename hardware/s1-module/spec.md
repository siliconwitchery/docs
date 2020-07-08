---
layout: default
title: Specification
nav_order: 1
parent: S1 Module
grand_parent: Hardware
---

## Absolute Maximum Ratings
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

## Electrostatic Discharge (ESD)
|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|V<sub>ESD-HBM</sub>| ESD - Human body model        |       |  V    |
|V<sub>ESD-CDM</sub>| ESD - Charged device model    |       |  V    |


## Thermal Information
V<sub>CHG</sub> = 0V, V<sub>BAT</sub> = 3.7V unless specified
|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|T<sub>RF</sub>| 1Mbps cont. TX radio temperature * |       |  °C   |
|T<sub>RF+FPGA</sub>| Full speed FPGA temperature * |       |  °C   |
|T<sub>CHG</sub>| Charge IC temperature V<sub>CHG</sub> = 5V * |   | °C  |
\* lab measured values

## Electrical Characteristics 
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

## RF Characteristics 
|                   |                               | Value | Unit  |
|:------------------|:------------------------------|:------|:------|
|V<sub>ESD-HBM</sub>| Max transmit power            | +4    |  dBm  |
|V<sub>ESD-CDM</sub>| Receive sensitivity           | -96   |  dBm  |
|V<sub>ESD-CDM</sub>| Whip antenna gain             | 3     |  dBi  |