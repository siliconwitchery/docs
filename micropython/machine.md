---
title: machine
description: machine class
# TODO create picture
image: images/s1-micropython.png
nav_order: 1
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine` – Functions related to the hardware

---

The `machine` class contains all of the classes and methods to control the S1 Module. Import it with:

```python
import machine
```

To see what's contained inside the class you can use the `help()` command:

```python
help(machine)
```

---

## Classes

`machine.Pin` - Functions related to the nRF GPIO pins. **See more info [here](/micropython/pin)**

`machine.ADC` - Functions related to the nRF ADC. **See more info [here](/micropython/adc)**

`machine.RTC` - Functions related to the nRF RTC and timing functions. **See more info [here](/micropython/rtc)**

`machine.FPGA` - Functions related to the iCE40 FPGA. **See more info [here](/micropython/fpga)**

`machine.Flash` - Functions related to the 32 Mbit flash memory. **See more info [here](/micropython/flash)**

`machine.PMIC` - Functions related to S1 power, and battery management. **See more info [here](/micropython/pmic)**

---

## Functions

`machine.mac_address()` - 

`machine.reset()` - 

`machine.reset_cause()` - 

- `RESET_CAUSE_NONE` - 

- `RESET_CAUSE_PIN_RESET` - 

- `RESET_CAUSE_WATCHDOG` - 

- `RESET_CAUSE_SOFT` - 

- `RESET_CAUSE_LOCKUP` - 

- `RESET_CAUSE_GPIO_WAKE` - 

- `RESET_CAUSE_DEBUG_WAKE` - 

`machine.power_down()` - 

---

## Constants

`machine.version` - 

`machine.git_tag` - 

`machine.build_date` - 

`machine.board_name` - 

`machine.mcu_name` - 