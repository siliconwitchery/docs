---
title: machine.Pin
description: Pin class
image: images/s1-micropython.png
nav_order: 2
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.Pin` – Functions to control the nRF GPIO pins

---

The `machine.Pin` class contains all of the functions to control the nRF52 GPIO. Import it using

```python
from machine import Pin
```

To see what's contained inside the class you can use the `help()` command

```python
help(Pin)
```

---

## Constructor

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

## Functions

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