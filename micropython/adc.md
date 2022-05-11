---
title: machine.ADC
description: ADC class
image: images/s1-micropython.png
nav_order: 3
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.ADC` – Functions to control the nRF ADC

---

The `machine.ADC` class contains all of the functions to control the nRF52 ADC. Import it using

```python
from machine import ADC
```

To see what's contained inside the class you can use the `help()` command

```python
help(ADC)
```

---

## Constructor

`class machine.ADC(channel, pPin, res=14[bit], samp=32, pRes=PULL_DISABLED, nRes=PULL_DISABLED, gain=GAIN_DIV6, ref=REF_INTERNAL, acq=10[us], mode=MODE_SINGLE)`

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

---

## Functions

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