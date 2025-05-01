---
title: Superstack Platform
description: Documentation for the Superstack platform
image: /assets/images/superstack-annotated-masthead.png
nav_order: 3
last_modified_date: April 21th 2025, 13:07 UTC
---

# Superstack IoT Platform
{: .no_toc }
{: .d-inline-block }
Preliminary
{: .label .label-yellow }

{: .note }
This page is actively being updated. Information may change so be sure to check back frequently 

---

![Silicon Witchery Superstack platform](/assets/images/superstack-annotated-masthead.png)

TODO: Blurb & feature-set

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Connecting your first module

## Lua programming & API

### Digital IO

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.digital.set_output(pin, value)`           | Sets or clears a digital output on a pin                                         | `pin` - **string** - The pin name. E.g. `"A0"`<br><br>`value` - **boolean** - The level to set on the pin. `true` for high, or `false` for low                                                                                                                                          | **nil**
| `device.digital.get_input(pin)`                   | Gets the digital value on a pin                                                  | `pin` - **string** - The pin name. E.g. `"A0"`                                                                                                                                                                                                                                      | **boolean** - `true` if the pin is high, or `false` if it's low
| `device.digital.assign_input_event(pin, handler)` | Assigns an event handler that triggers whenever the input value of a pin changes | `pin` - **string** - The pin name. E.g. `"A0"`<br><br>`handler` - **function** - The function to call whenever the pin value changes. This function will be called with one argument of type **boolean** which represents the input value on that pin. `true` if high, or `false` if low | **nil**
| `device.digital.unassign_input_event(pin)`        | Removes any previously assigned event handler function attached to a pin         | `pin` - **string** - The pin name. E.g. `"A0"`                                                                                                                                                                                                                                      | **nil**

Example usage:

```lua
-- Set pin B1 to a high value
device.digital.set_output("B1")

-- Print the value on pin D0
local val = device.digital.get_input("D0")
print(val)

-- Assign a function that triggers whenever the input value of C3 changes
function my_pin_handler(value)
    if value == true then
        print("C3 went high")
    else
        print("C3 went low")
    end
end

device.digital.assign_input_event("C3", my_pin_handler)
```

### Analog input

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.analog.get_input(pin, { acquisition_time=40, range=Vout })`                                             | Reads the analog value on an analog capable pin                                         | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`acquisition_time` *optional* - **integer** - A time in microseconds across to which to make the measurement. Can be either `3`, `5`, `10`, `15`, `20`, `40`, or multiples of 40 e.g. `80`, `120`, `160`, etc. Higher values allow for accurate measurement of greater source resistances. Those maximum resistances being 10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ and 800kΩ respectively, with 800kΩ being the maximum source resistance for acquisition times greater than 40 microseconds<br><br>`range` *optional* - **integer** - The maximum expected voltage for the input signal. Defaults to the same value as V<sub>OUT</sub>                                                                                                                             | **table** - A table containing two key value pairs. `voltage` a **number** representing the voltage on the pin, or `percentage` a **number** representing the real voltage represented as a percentage with respect to the range of 0V and the `range` value
| `device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40, range=Vout })`         | Reads the analog value across two analog capable pins                                   | `positive_pin` - **string** - The pin name of the positive pin<br><br>`negative_pin` - **string** - The pin name of the negative pin<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **table** - Same as above
| `device.analog.assign_input_high_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })` | Assigns an event handler that triggers whenever the input pin crosses a high threshold. | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`handler` - **function** - The function to call whenever the threshold is crossed. This function will be called with one argument of type **boolean** which represents if the value has crossed above or below the threshold. `true` if crossed above, or `false` if crossed below<br><br>`percentage` - **number** - The level represented as a percentage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`voltage` - **number** - The level represented as a voltage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above | **nil**
| `device.analog.assign_input_low_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })`  | Assigns an event handler that triggers whenever the input pin crosses a low threshold.  | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`handler` - **function** - The function to call whenever the threshold is crossed. This function will be called with one argument of type **boolean** which represents if the value has crossed above or below the threshold. `true` if crossed below, or `false` if crossed above<br><br>`percentage` - **number** - The level represented as a percentage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`voltage` - **number** - The level represented as a voltage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above | **nil**
| `device.analog.unassign_input_high_event(pin)`                                                                  | Removes any previously assigned high level event handler attached to a pin              | `pin` - **string** - The pin name. E.g. `"D0"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **nil**
| `device.analog.unassign_input_low_event(pin)`                                                                   | Removes any previously assigned low level event handler attached to a pin               | `pin` - **string** - The pin name. E.g. `"D0"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **nil**

Example usage:

```lua
-- Read the analog value on pin D1 and print both the percentage and voltage values
local d0_val = device.analog.get_input("D1")
print(d0_val["percentage"])
print(d0_val["voltage"])
```

### PWM output (analog output)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.analog.set_output(pin, percentage { frequency=1 })` | Sets a PWM duty cycle on a pin | `pin` - **string** - The pin name. E.g. `"A0"`<br><br>`percentage` - **number** - The duty cycle to output on the pin as a percentage<br><br>`frequency` *optional* - **number** - The PWM frequency in Hz | **nil**

Example usage:

```lua
-- Set pin E1 to a 25% duty cycle at the default PWM frequency
device.analog.set_output("E1", 25)
```

### I2C communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### SPI communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### UART communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### PDM microphone input

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### LTE communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### DSP & types

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### File system

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

### Miscellaneous functions

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.sleep(time)` | Puts the device into a low power sleep for a certain amount of time | `time` - **number** - The time to sleep in seconds. E.g. `1.5` | **nil** 

| Constant | Description | Value |
|----------|-------------|-------|
| `device.HARDWARE_VERSION` | The hardware version of the device                                            | **string** - Always `"s2-module"` 
| `device.FIRMWARE_VERSION` | The current firmware version of the Superstack firmware running on the device | **string** - A string representing the current firmware version. E.g. `"0.1.0+0"`

## Working with data

### Data API

## Advanced AI usage

### Natural language API

## Managing devices & deployments

### Un-pairing devices

## Managing your subscription

