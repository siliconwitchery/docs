---
title: MicroPython
description: MicroPython docs for the S1 Module series products
image: /images/s1-micropython.png
nav_order: 5
has_children: true
last_modified_date: May 11th 2022, 07:00 PM
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

## Installing MicroPython on the S1 Module

MicroPython works great on all of our S1 products. 

1. Download the latest `.hex` release from [here](https://github.com/siliconwitchery/micropython/releases) 📁 <!-- TODO add link-->

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

    ![Animation of the S1 Web REPL connecting](/micropython/images/s1-micropython-connecting-repl.gif)

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

## Improvements

Spotted something? Feel free to report any bugs you find, or suggest improvements. We're always willing to improve things.

Submit an issue to our [GitHub](https://github.com/siliconwitchery/micropython/issues) or [contact us](mailto:info@siliconwitchery.com?subject=MicroPython) if something is unclear.

---

That's it! For the full list of classes and functions, check out the pages below. Happy tinkering!