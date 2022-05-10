---
title: MicroPython
description: MicroPython docs for the S1 Module series products
image: images/s1-micropython.png
nav_order: 5
has_children: true
last_modified_date: May 10th 2022, 06:27 PM
---

# MicroPython on the S1 Module
{: .no_toc }
{: .d-inline-block }
v.1.1.8-322
{: .label .label-blue }

---

MicroPython on the S1 lets you quickly prototype and test your algorithms without having to get into C/C++ development. You can easily upload FPGA binaries, read/write data, and control all module features over the air.

**No programmer needed.**

It can also functions as an excellent network stack. Allowing interface to a mobile app, using simple strings.

```python
from machine import RTC
from machine import FPGA

FPGA.run() # Boots the FPGA application
processedData = bytearray(100) # Data from the FPGA will go here

while True:
    FPGA.read(processData) # Read 100 bytes over SPI

    processedData # Print the data out

    RTC.sleep_ms(1000) # Repeat again every second

```

---

## Installing MicroPython on the S1 Module

MicroPython works great on all of our S1 products. 

1. Download the latest release from [here](#). <!-- TODO add link-->

1. You'll need a [J-Link compatible programmer](https://docs.siliconwitchery.com/s1-popout-board/s1-popout-board/#programming) and the [J-Link software](https://www.segger.com/downloads/jlink/) installed 

1. Make sure you have the [nRF command line tools](https://www.nordicsemi.com/Products/Development-tools/nrf-command-line-tools/download) installed

1. Flash the binary with the command

    ```bash
    nrfjprog --program micropython-vxxx.hex --chiperase -f nrf52
    ```

1. Access the MicroPython REPL wirelessly from our [Web REPL app](https://repl.siliconwitchery.com)

## First steps

1. Connect using the button and you should see your S1 device appear

    ![Animation of the S1 Web REPL connecting](/micropython/images/s1-micropython-connecting-repl.gif)

1. Press Ctrl-B to enter the friendly REPL mode

1. All the S1 related functions are located inside the `machine` module. Import it

    ```python
    import machine
    ```

1. To see what's contained inside the module, you can call `help()` on it

    ```python
    help(machine)
    ```

1. You can also import the S1 classes directly and use them without having to specify `machine`

    ```python
    from machine import Pin

    myPin = Pin(Pin.PIN_A1, pull=Pin.PULL_DOWN)
    myPin() # Reads the pin value
    ```

1. You can also call help on classes to see the contained methods and constants
    ```python
    from machine import Pin
    help(Pin)
    ```

1. That's it! For the full list of classes and methods, check out the pages below. Happy tinkering!