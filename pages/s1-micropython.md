---
title: S1 MicroPython
description: MicroPython docs for the S1 Module series products
image: /images/annotated-micropython.png
nav_order: 7
last_modified_date: May 11th 2022, 07:00 PM
redirect_from:
  - /micropython/micropython/
  - /micropython/adc/
  - /micropython/flash/
  - /micropython/fpga/
  - /micropython/machine/
  - /micropython/pin/
  - /micropython/pmic/
  - /micropython/rtc/
---

# MicroPython on the S1 Module
{: .no_toc }
{: .d-inline-block }
v1.18-387
{: .label .label-blue }

---

MicroPython on the S1 lets you quickly prototype and test your algorithms without having to get deep into C development. You can easily test FPGA binaries, read or write data, and control all module features over the air.

**No programmer needed**

MicroPython also functions as an excellent network stack. Allowing you to interface to a mobile app, or Bluetooth gateway, using simple strings.

```python
from machine import RTC
from machine import FPGA

FPGA.run() # Boot the FPGA application
processedData = bytearray(100) # Data from the FPGA will be stored here

while True:
    FPGA.read(processData) # Read 100 bytes over SPI
    processedData # Print out the data
    RTC.sleep_ms(1000) # Repeat again every second
```

---

## Contents
{: .no_toc }

1. TOC
{:toc}

---

## Installing MicroPython on the S1 Module

MicroPython works great on all of our S1 products. 

1. Download the latest `.hex` release from [here](https://github.com/siliconwitchery/s1-micropython/releases) 📁 <!-- TODO add link-->

1. You'll need a [J-Link compatible programmer](https://docs.siliconwitchery.com/s1-popout-board/s1-popout-board/#programming) and the [J-Link software](https://www.segger.com/downloads/jlink/) installed 

1. Make sure you have the [nRF command line tools](https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools/download) installed

1. Flash the binary using the command

    ```bash
    nrfjprog --program micropython-s1-*.hex --chiperase -f nrf52 --verify -r
    ```

1. Access MicroPython wirelessly using our [Web REPL](https://repl.siliconwitchery.com)

---

## First steps

1. Click **Connect** and you'll see your S1 device appear. Select it and click **Pair**

    ![Animation of the S1 Web REPL connecting](/assets/images/s1-micropython-connecting-repl.gif)

1. Press **Ctrl-B** to enter the friendly REPL mode

1. All of the S1 related functions are located inside the `machine` module. Import it using the command

    ```python
    import machine
    ```

1. To see what's contained inside `machine`, you can use the `help()` function

    ```python
    help(machine)
    ```

1. You can import any class contained within `machine`, and use them directly without having to specify `machine` before the class name

    ```python
    from machine import Pin

    myPin = Pin(Pin.PIN_A1, pull=Pin.PULL_DOWN)
    myPin() # Reads the pin value
    ```

1. You can also call help on these inner classes to see the functions contained within

    ```python
    from machine import Pin
    help(Pin)
    ```

---

## Library Reference

The hardware specific libraries for the S1 are described below. Each library must be imported before use like so:

```python
from machine import ADC
from machine import FPGA
...
```

To list what functions and definitions a library contains, the `help()` command can be used after importing:

```python
from machine import ADC

help(ADC)
```

---

### `machine` – S1 module hardware library

This class contains everything required to control the S1 Module.

#### Classes

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

#### Functions

`machine.mac_address()`

- Returns the 48bit MAC address as a 12 character hex *string*

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

#### Constants

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

---

### `machine.Pin` – General purpose digital IO

This class contains all of the functions to control the nRF52 GPIO.

#### Constructor

`class machine.Pin(pin, mode=IN, pull=PULL_DISABLED, drive=S0S1)`

- The S1 Module breaks out two nRF52 GPIO pins. `PIN_A1` and `PIN_A2`. These can be configured as inputs, outputs, interrupts, or ADC inputs *(see the ADC class for more info about how to use the pins as ADC inputs)*

- To initialize a pin, call the `Pin` constructor

    ```python
    myPin = Pin(Pin.PIN_A1, mode=Pin.OUT, pull=Pin.PULL_DISABLED, drive=Pin.S0H1)
    ```

- To view the current configuration, you can simply print the object

    ```python
    myPin
    # Will print out the configuration for myPin
    Pin(Pin.PIN_A1, mode=OUT, pull=PULL_DISABLED)
    ```

- Various options can be provided when setting up the pin

    | mode | |
    |---|---|
    | `IN` | Pin will be an input. **Default** |
    | `OUT` | Pin will be an output |

    | pull | |
    |---|---|
    | `PULL_DISABLED` | Internal pull resistor will be disabled. **Default** |
    | `PULL_UP` | Pin will be pulled up |
    | `PULL_DOWN` | Pin will be pulled down |

    | drive | Drive strength only applicable in output mode |
    |---|---|
    | S0S1 | Standard 0, standard 1. **Default** |
    | H0S1 | High drive 0, standard 1 |
    | S0H1 | Standard 0, high drive 1 |
    | H0H1 | High drive 0, high drive 1 |
    | D0S1 | Disconnect 0, standard drive 1 |
    | D0H1 | Disconenct 0, high drive 1 |
    | S0D1 | Standard 0, disconnect 1 |
    | H0D1 | High drive 0, disconnect 1 |

#### Functions

`Pin(outputValue)`

- Gets or sets the pin value depending on the mode that is configured

    ```python
    myPin() # Reads the value on the pin
    myPin(True) # Sets the value of the pin if in output mode
    ```

`Pin.irq(callback, trigger=IRQ_TOGGLE)`

- Sets up an interrupt for a pin that's configured as an input. When a trigger is detected, MicroPython will run the callback provided

    ```python
    # First set up a callback
    def myCallback():
        print("Do stuff")

    # Set up a pin as an input
    myPin = Pin(Pin.PIN_A1, mode=Pin.IN, pull=Pin.PULL_DOWN)

    # Set up the interrupt
    myPin.irq(myCallback, toggle=Pin.IRQ_RISING)
    ```

- One of three trigger modes can be selected when configuring an interrupt

    | trigger | |
    |---|---|
    | `IRQ_TOGGLE` | Interrupt will detect both rising and falling edges. **Default** |
    | `IRQ_RISING` | Interrupt will only detect rising edges |
    | `IRQ_FALLING` | Interrupt will only detect falling edges |

`Pin.irq_disable()`

- Disables any interrupt set up for that pin

    ```python
    myPin.irq_disable()

    ## myCallback will no longer trigger on a rising edge of PIN_A1
    ```

---

### `machine.ADC` – Analog to digital convertor

This class contains all of the functions to control the nRF52 ADC.

#### Constructor

```python
class machine.ADC(channel, pPin, res=14[bit], samp=32, pRes=PULL_DISABLED, nRes=PULL_DISABLED, gain=GAIN_DIV6, ref=REF_INTERNAL, acq=10[us], mode=MODE_SINGLE)
```

- The S1 module breaks out two nRF GPIO pins. `PIN_A1` and `PIN_A2`. Both of these pins can be used as ADC inputs, either as two single ended inputs, or a differential pair

- To initialize an ADC input pin, call the `ADC` constructor

    ```python
    myPin = ADC(0, ADC.PIN_A1) # Channel 0, and pin A1
    ```

- The channel can be from 0 - 6. Different channels can be set using the same pin for different configurations. To fully understand the ADC features and limitations, have a look at the **SAADC** section of the [nRF52811 datasheet](https://infocenter.nordicsemi.com/pdf/nRF52811_PS_v1.1.pdf)

- To view the current configuration, you can simply print the object

    ```python
    myPin
    # Prints out the configuration for myPin
    ADC(ch=0, pPin=PIN_A1, res=14[bit], samp=32, pRes=PULL_DISABLED, nRes=PULL_DISABLED, gain=GAIN_DIV6, ref=REF_INTERNAL, acq=10[us], mode=MODE_SINGLE)
    ```

- Various options can be provided when setting up the ADC pin

    | res | |
    |---|---|
    | `14` | Uses a 14 bit ADC resolution. **Default** |
    | `12` | Uses a 12 bit ADC resolution |
    | `10` | Uses a 10 bit ADC resolution |
    | `8` | Uses an 8 bit ADC resolution |

    | samp | |
    |---|---|
    | `1` | No oversampling |
    | `2` | Use 2x oversampling |
    | `4` | Use 4x oversampling |
    | `8` | Use 8x oversampling |
    | `16` | Use 16x oversampling |
    | `32` | Use 32x oversampling. **Default** |
    | `64` | Use 64x oversampling |
    | `128` | Use 128x oversampling |
    | `256` | Use 256x oversampling |

    | pRes/nRes | Note: nRes is only applicable in differential mode |
    |---|---|
    | `PULL_DISABLED` | Internal pull resistor is disabled. **Default** |
    | `PULL_UP` | Pin will be pulled up |
    | `PUUL_DOWN` | Pin will be pulled down |
    | `PULL_HALF` | Pin will be pulled to half the VDD of the nRF (1.8V/2) |

    | gain | |
    |---|---|
    | `GAIN_DIV6` | Set the ADC gain to 1/6. **Default** |
    | `GAIN_DIV5` | Set the ADC gain to 1/5 |
    | `GAIN_DIV4` | Set the ADC gain to 1/4 |
    | `GAIN_DIV3` | Set the ADC gain to 1/3 |
    | `GAIN_DIV2` | Set the ADC gain to 1/2 |
    | `GAIN_UNITY` | Set the ADC gain to 1 |
    | `GAIN_MUL2` | Set the ADC gain to 2 |
    | `GAIN_MUL4` | Set the ADC gain to 3 |

    | ref | |
    |---|---|
    | `REF_INTERNAL` | Use the internal 0.6V reference. **Default** |
    | `REF_QUARTER_VDD` | Use a 1/4 VDD reference ~1.8V/4 |

    | acq | |
    |---|---|
    | `3` | Use an acquisition time of 3us |
    | `5` | Use an acquisition time of 5us |
    | `10` | Use an acquisition time of 10us. **Default** |
    | `15` | Use an acquisition time of 15us |
    | `20` | Use an acquisition time of 20us |
    | `40` | Use an acquisition time of 40us |

    | mode | |
    |---|---|
    | `MODE_SINGLE` | Use the pin as a single ended input. **Default** |
    | `MODE_DIFF` | Enable differential input. The other pin will be automatically selected as the negative input |

#### Functions

`ADC()`

- Gets the raw *integer* register value of the ADC channel

    ```python
    myPin()
    # Returns the raw value
    399
    ```

`ADC.voltage()`

- Gets the ADC value and returns the voltage as a *float* based on the channel settings

    ```python
    myPin.voltage()
    # Returns the voltage as a float
    0.1010742
    ```

`ADC.calibrate()`

- Internally calibrates the ADC for more accurate readings. Can be called after power on, or periodically if the module will be subject to large temperature changes

---

### `machine.RTC` – Real time clock

This class contains all of the functions to control the nRF52 RTC and timing functions.

#### Functions

`RTC.time(setTime)`

- If `RTC.time()` is called without an argument, it will return the time in seconds since power on, or the last reset

    ```python
    RTC.time()
    4699 # Around 1.3 hours
    ```

- If a value is provided, the internal time is adjusted, and following reads will return the time from then on. **Note** Due to the 30 bit limitation of MicroPython integers, standard epoch time cannot be used. Instead, use a different reference, such as seconds since 1st Jan 2000

    ```python
    RTC.time(705580080) # Set date and time to May 11th 2022, 11:28:00 AM
    
    # 5 minutes later
    RTC.time()
    705580380
    ```

`RTC.sleep_ms(ms)`

- Puts the nRF into a light sleep for a number of milliseconds provided. The device will remain connected, but won't respond until the time is up. This can be used to create simple delays in loops

---

### `machine.FPGA` – FPGA controller

This class contains all of the functions to control the iCE40 FPGA.

#### Functions

`FPGA.run()`

- Brings the FPGA out of reset, and loads any binary stored in the flash

    ```python
    PMIC.fpga_power(True) # Ensure the FPGA is powered on, in case you disabled it before
    FPGA.run()
    ```

- Ensure a valid FPGA binary is stored within the flash, otherwise the FPGA won't configure

`FPGA.reset()`

- Resets the FPGA

`FPGA.status()`

- Gets the current status of the FPGA. Will return one of the following *strings*

    | `FPGA_RESET` | The FPGA is currently held in reset |
    | `FPGA_CONFIGURING` | The FPGA is configuring and loading the binary from the flash |
    | `FPGA_RUNNING` | The FPGA is running |

`FPGA.irq()`

- Once the FPGA is configured and running, the CDONE pin which tells us the state of the FPGA, can now be used as a user interrupt

- Similar to Pin.irq() it can be configured to execute a callback whenever the CDONE pin goes low (always a falling edge)

    ```python
    # First set up a callback
    def myCallback():
        print("Do stuff")

    FPGA.run()
    FPGA.irq(myCallback)
    ```

`FPGA.irq_disable()`

- Disables the FPGA interrupt

`FPGA.read(rxbuffer)`

- Reads data from the FPGA over the internal SPI bus

    ```python
    rx = bytearray(10) # Create a 10 byte buffer to read into
    FPGA.read(rx) # Reads 10 bytes over the SPI bus

    # The buffer can be printed, showing what was received
    rx
    # Will print out
    bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
    ```

`FPGA.write(txBuffer)`

- Writes data to the FPGA over the internal SPI bus

    ```python
    tx = [1, 2, 3, 4, 5] # Create an array of 5 bytes to send
    tx = "\x01\x02\x03\x04\x05" # The buffer can also be created as a string

    FPGA.write(tx) # Sends the 5 bytes from the tx buffer
    ```

`FPGA.read_write(rxBuffer, txBuffer)`

- Simultaneously reads and writes data

    ```python
    # rx and tx are the same as before
    FPGA.read_write(rx, tx) # Read 10 bytes, and write 5 bytes
    ```

---

### `machine.Flash` – Flash memory

This class contains all of the functions to read and write to the flash IC.

#### Functions

`Flash.sleep()`

- Puts the flash IC into deep sleep for saving power

- The flash IC will automatically be woken up if any of the flash operations below are called

`Flash.erase(blockNum)`

- Erases a 4kB block from the flash IC
    
    ```python
    Flash.erase(0) # Erase block 0
    Flash.erase(5) # Erase block 5
    ```

- If no block number is given, the chip is fully erased. This can take a while

    ```python
    Flash.erase() # Full chip erase can take up to 80 seconds
    ```

`Flash.read(pageNum, rxBuffer)`

- Reads the flash from the page number provided. Each page is 256 bytes long, therefore up to 256 bytes can be read at a time

    ```python
    rx = bytearray(256)
    Flash.read(0, rx) # Read 256 bytes from page 0

    # Shorter amounts can also be read using a smaller buffer
    rx = bytearray(10)
    Flash.read(4, rx) # Read 10 bytes from page 4
    ```

`Flash.write(pageNum, txBuffer)`

- Writes to the flash at the page number provided. Each page is 256 bytes long, therefore up to 256 bytes can be written at a time

    ```python
    tx = bytearray(256)

    for i in range(256):
        tx[i] = i # Populate some test data
    
    Flash.write(0, tx) # Write 256 bytes to page 0
    
    # Again, smaller amounts can also be written
    ```

---

### `machine.PMIC` – Power management

This class contains all of the functions to configure the S1 voltage rails, and configure the battery charger.

#### Functions

`PMIC.charge_config(v, i)`

- Configures the battery charger. If no arguments are given, the current setting is printed as a *tuple*

- If voltage, and/or current arguments are provided, the values will be set accordingly

- Voltage `v` can be set between 3.6V and 4.3V (in 50mV steps)

- Current `i` can be set between 7.5mA and 300mA (in 7.5mA steps). **Note** Value should be written as a *float* in mA, not A

    ```python
    PMIC.charge_config(v=4.21, i=100)

    PMIC.charge_config() # Read the set parameters
    # Note the difference due to the resolution that can be set
    (4.2, 97.5) 
    ```

`PMIC.battery_level(enable)`

- Displays the current battery voltage as a *float*

- Before reading the value, the voltage monitoring must be enabled

    ```python
    PMIC.battery_level(True) # Enable monitoring
    PMIC.battery_level() # Read the battery level
    3.46

    PMIC.battery_level(False) # The monitoring can be disabled to save a small amount of power if not needed
    ```

`PMIC.fpga_power(enable)`

- Enables or disables the FPGA core power rail

- Setting this to `False` will automatically disable the Vio rail to avoid damaging the FPGA. Vio will need to be reconfigured manually after reenabling the FPGA core power rail

    ```python
    PMIC.fpga_power() # Read the current state of the rail
    True

    PMIC.fpga_power(False) # Shuts down the FPGA core power rail

    PMIC.vio_config() # Read the Vio rail value
    # Will be set to 0V whenever the FPGA is shut down
    0

    PMIC.fpga_power(True) # Power on the FPGA again
    PMIC.vio_config(1.8) # You'll need to set the Vio rail again
    ```

`PMIC.vaux_config(voltage)`

- Configures the buck-boost convertor of the Vaux rail

- If no arguments are given, the current setting will be printed as a *float*

- Can be set to 0V which turns off the rail, or between 0.8V and 5.5V

    ```python
    PMIC.vaux_config(3.3) # Set the Vaux rail to 3.3V

    # Read the current setting
    PMIC.vaux_config()
    3.3
    ```

- If Vio is set to be in load switch mode, the Vaux rail will be limited to 3.45V

`PMIC.vio_config(voltage, lsw=False)`

- Configures the FPGA IO rail voltage, either in LDO mode, or load switch mode

- If no arguments are given, the current setting will be printed

    - If Vio is configured as an LDO, the voltage setting will be returned as a *float*

    - If Vio is configured as a load switch, the state will be returned as a *string*. Either `LOAD_SWITCH_ON` or `LOAD_SWITCH_OFF`

- Can be set to 0V which turns off the rail, regardless of the mode

    ```python
    PMIC.vio_config(0) # Shuts down the rail
    ```

- Can be set between 0.8V or 3.45V in LDO mode

    ```python
    PMIC.vio_config(3.3, lsw=False) # Set Vio to regulate 3.3V in LDO mode

    PMIC.vio_config(3.3) # The same as above. lsw=False by default
    ```

- Vio can also be configured as a load switch. In this mode the Vaux voltage is passed through directly to Vio. In this case, Vaux must not exceed 3.45V

    ```python
    PMIC.vio_config(True, lsw=True) # Turn on the load switch (pass Vaux to Vio)
    
    PMIC.vio_config(False, lsw=True) # Turn off the load switch
    ```

---

## Improvements

Spotted something? Feel free to report any bugs you find, or suggest improvements. We're always willing to improve things.

Submit an issue to our [GitHub](https://github.com/siliconwitchery/s1-micropython/issues) or [contact us](mailto:info@siliconwitchery.com?subject=MicroPython) if something is unclear.
