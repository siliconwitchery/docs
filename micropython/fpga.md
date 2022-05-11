---
title: machine.FPGA
description: FPGA class
image: images/s1-micropython.png
nav_order: 5
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.FPGA` – Functions to control the FPGA

---

The `machine.FPGA` class contains all of the functions to control the iCE40 FPGA. Import it using

```python
from machine import FPGA
```

To see what's contained inside the class you can use the `help()` command

```python
help(FPGA)
```

---

## Functions

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