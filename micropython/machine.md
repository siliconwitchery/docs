---
title: machine
description: machine class
image: images/s1-micropython.png
nav_order: 1
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine` – Functions related to the hardware

---

The `machine` class contains everything required to control the S1 Module. Import it using

```python
import machine
```

To see what's contained inside the class you can use the `help()` command

```python
help(machine)
```

---

## Classes

`machine.Pin` 

- Functions related to the nRF GPIO pins. **See more info about the [Pin class](/micropython/pin)**

`machine.ADC`
    
- Functions related to the nRF ADC. **See more info about the [ADC class](/micropython/adc)**

`machine.RTC`

- Functions related to the real time clock and time functions. **See more info about the [RTC class](/micropython/rtc)**

`machine.FPGA`

- Functions related to the iCE40 FPGA. **See more info about the [FPGA class](/micropython/fpga)**

`machine.Flash`

- Functions related to the 32 Mbit flash memory. **See more info about the [Flash class](/micropython/flash)**

`machine.PMIC`

- Functions related to S1 power and battery management IC. **See more info about the [PMIC class](/micropython/pmic)**

---

## Functions

`machine.mac_address()`

- Returns the 48bit MAC address as a 11 character hex *string*

`machine.reset()`

- Resets the nRF52. Both MicroPython and the Bluetooth connection will be reset. **Note that the PMIC configuration remains unchanged**

`machine.reset_cause()`
    
- Displays one of the following causes for the last reset. After calling this function, the reset cause is atomatically cleared to `RESET_CAUSE_NONE`

    | `RESET_CAUSE_NONE` | No resets since power on, or the reset cause has already been read |
    | `RESET_CAUSE_SOFT` | Last reset via `machine.reset()` |
    | `RESET_CAUSE_LOCKUP` | System was reset from a CPU lockup or crash |
    | `RESET_CAUSE_GPIO_WAKE` | System woken up from deep sleep by a `Pin` interrupt |

`machine.power_down()`

- Puts the device into the lowest power deep sleep. Can only be woken up using a `Pin` interrupt, or power cycle

- Once woken up, the device will be reset. `machine.reset_cause()` will show the cause `RESET_CAUSE_GPIO_WAKE`

- **Note: To ensure the lowest power consumption**, follow the sequence below to ensure all other devices are powered down before going to sleep

    ```python
    FPGA.reset() # Stop the FPGA
    Flash.sleep() # Place the flash into deep sleep
    PMIC.battery_level(False) # Disable battery monitoring
    PMIC.fpga_power(False) # Shutdown FPGA power
    PMIC.vaux_config(0) # Turn off the Vaux buck-boost convertor

    # Remember to set up a Pin.irq if pin based wake is required

    machine.power_down()
    ```

---

## Constants

`machine.version`

- Displays the current MicroPython version as a *tuple*

`machine.git_tag`

- Displays the Git tag of the current MicroPython build as a *string*

`machine.build_date`

- Displays the build date of the current MicroPython build as a *string*

`machine.board_name`

- Returns the board name as a *string*. Always `s1 module`

`machine.mcu_name`

-  Returns the MCU name as a *string*. always `nrf52811`