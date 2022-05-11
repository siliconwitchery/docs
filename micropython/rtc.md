---
title: machine.RTC
description: RTC class
image: images/s1-micropython.png
nav_order: 4
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.RTC` – Functions to control the nRF RTC

---

The `machine.RTC` class contains all of the classes and methods to control the nRF52 RTC and timing functions. Import it with:

```python
from machine import RTC
```

To see what's contained inside the class you can use the `help()` command:

```python
help(RTC)
```

---

## Functions

`RTC.time(setTime)`

- If the RTC.time function is called without an argument, it will return the time in seconds since power on.

    ```python
    RTC.time()
    4699 # Around 1.3 hours
    ```

- If a value is provided, the internal timer is changed to that time, and following reads will return the time from then on. **Note** Due to a 30bit limitation of MicroPython numbers, standard epoch time cannot be used here. Instead use a different reference, such as seconds since 1st Jan 2000:

    ```python
    RTC.time(705580080) # Set date and time to May 11th 2022, 11:28:00 AM
    
    # 5 minutes later
    RTC.time()
    705580380
    ```

`RTC.sleep_ms(ms)`

- Puts the nRF into a light sleep for a number of milliseconds provided. The device will remain connected, but won't respond until the time is up. It can be used to create simple delays in loops.