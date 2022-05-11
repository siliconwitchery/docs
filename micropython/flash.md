---
title: machine.Flash
description: Flash class
image: images/s1-micropython.png
nav_order: 6
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.Flash` – Functions to control the 32 Mbit flash IC

---

The `machine.Flash` class contains all of the functions to read and write to the flash IC. Import it using

```python
from machine import Flash
```

To see what's contained inside the class you can use the `help()` command

```python
help(Flash)
```

---

## Functions

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