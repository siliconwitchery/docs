---
title: Superstack Platform
description: Documentation for the Superstack platform
image: /assets/images/superstack-annotated-masthead.png
nav_order: 3
last_modified_date: May 5th 2025, 08:20 UTC
---

# Superstack IoT Platform
{: .no_toc }
{: .d-inline-block }
Preliminary
{: .label .label-yellow }

{: .note }
This page is actively being updated. Information may change, so be sure to check back frequently.

---

![Silicon Witchery Superstack platform](/assets/images/superstack-annotated-masthead.png)

Superstack is a cloud IoT platform that lets you deploy, program, and manage connected devices from anywhere. You can update firmware, monitor data in real-time, and run AI-powered analytics, all through a secure web dashboard or API. Superstack handles connectivity, device onboarding, and fleet management, so you can focus on building your application. Its natural language query engine and easy business integration make it simple to turn raw device data into actionable insights at scale.

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Connecting your first module

<!-- TODO -->
Detailed setup and commissioning steps will be added soon. 

In the meantime, the short video below describes the general setup, as well as overall features.

<!-- TODO add a video of the step by step setup guide -->
<div style="position: relative; width: 100%; overflow: hidden; padding-top: 56.25%;">
    <iframe style="position: absolute; top: 0; left: 0; right: 0; width: 100%; height: 100%; border: none;"
        src="https://www.youtube.com/embed/3L_OU-fMW_w" title="YouTube video player"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        referrerpolicy="strict-origin-when-cross-origin" allowfullscreen>
    </iframe>
</div>

## Lua programming & API

All Superstack-compatible devices, including the [S2 Module](/pages/s2-module), run a unified firmware that includes the **Lua 5.4.7** runtime. A powerful yet simple scripting engine that can be picked up easily by new and seasoned programmers alike.

This engine allows devices to be programmed remotely to run scripts that gather data from sensors, process it, and then return data to Superstack. All the exposed Lua functions are hardware-accelerated under the hood, allowing for performance close to that of bare-metal in C.

Thanks to this scriptable nature, applications can be iterated and debugged incredibly quickly without having to maintain any local development tools or wait for compilations to complete. Best of all, this can all be done remotely, with devices that may be located across countries or continents.

### Standard Lua libraries

Many of the standard libraries are included for the user to take advantage of.

- ✅ [Basic functions](https://www.lua.org/manual/5.4/manual.html#6.1)
- ✅ [Math functions](https://www.lua.org/manual/5.4/manual.html#6.7)
- ✅ [String manipulation](https://www.lua.org/manual/5.4/manual.html#6.4)
- ✅ [Table manipulation](https://www.lua.org/manual/5.4/manual.html#6.6)
- ✅ [UTF-8 support](https://www.lua.org/manual/5.4/manual.html#6.5)
- ✅ [Coroutine manipulation](https://www.lua.org/manual/5.4/manual.html#6.2)
- ✅ [Debug library](https://www.lua.org/manual/5.4/manual.html#6.10)

Standard libraries which are not included are superseded by similar device specific libraries:

- ❎ File IO functions - Replaced by the [non-volatile memory](#non-volatile-memory-file-system) library
- ❎ Operating system functions - Replaced by the [timekeeping ](#timekeeping-functions) and [device](#miscellaneous-functions) libraries

---

The following device-specific libraries allow access to all aspects of the device I/O and feature set such as LTE-based communication and GPS. Additionally, some other libraries provide convenient functions for running DSP operations and type conversions.

These functions may accept a combination of positional and named arguments. Named arguments are passed as tables which essentially expect key-value pairs. Most of these keys will take on a default value if not provided. These are marked as *optional*.

```lua
-- Calling a function with only positional arguments
device.digital.set_output("A0", true)

-- Calling a function with both positional and named arguments
device.i2c.write(0x12, 0x4F, "\x01", { scl_pin="B0", sda_pin="B1"})

-- Calling a function with only positional arguments. Note how the () can be omitted
network.send{ sensor_value=31.5 }
```

### Digital IO

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.digital.set_output(pin, value)` | Sets or clears a digital output on a pin | `pin` - **string** - The pin name. E.g. `"A0"`<br><br>`value` - **boolean** - The level to set on the pin. `true` for high, or `false` for low | **nil**
| `device.digital.get_input(pin)` | Gets the digital value on a pin | `pin` - **string** - The pin name. E.g. `"A0"` | **boolean** - `true` if the pin is high, or `false` if it's low
| `device.digital.assign_input_event(pin, handler)` | Assigns an event handler that triggers whenever the input value of a pin changes | `pin` - **string** - The pin name. E.g. `"A0"`<br><br>`handler` - **function** - The function to call whenever the pin value changes. This function will be called with one argument of type **boolean** which represents the input value on that pin. `true` if high, or `false` if low | **nil**
| `device.digital.unassign_input_event(pin)` | Removes any previously assigned event handler function attached to a pin | `pin` - **string** - The pin name. E.g. `"A0"` | **nil**

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
| `device.analog.get_input(pin, { acquisition_time=40, range=Vout })` | Reads the analog value on an analog-capable pin | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`acquisition_time` *optional* - **integer** - A time in microseconds across which to make the measurement. Can be either `3`, `5`, `10`, `15`, `20`, `40`, or multiples of 40 e.g. `80`, `120`, `160`, etc. Higher values allow for accurate measurement of greater source resistances. Those maximum resistances being 10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ and 800kΩ respectively, with 800kΩ being the maximum source resistance for acquisition times greater than 40 microseconds<br><br>`range` *optional* - **integer** - The maximum expected voltage for the input signal. Defaults to the same value as V<sub>OUT</sub> | **table** - A table containing two key-value pairs. `voltage` a **number** representing the voltage on the pin, or `percentage` a **number** representing the real voltage represented as a percentage with respect to the range of 0V and the `range` value
| `device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40, range=Vout })` | Reads the analog value across two analog capable pins | `positive_pin` - **string** - The pin name of the positive pin<br><br>`negative_pin` - **string** - The pin name of the negative pin<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | **table** - Same as above
| `device.analog.assign_input_high_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })` | Assigns an event handler that triggers whenever the input pin crosses a high threshold. | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`handler` - **function** - The function to call whenever the threshold is crossed. This function will be called with one argument of type **boolean** which represents if the value has crossed above or below the threshold. `true` if crossed above, or `false` if crossed below<br><br>`percentage` - **number** - The level represented as a percentage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`voltage` - **number** - The level represented as a voltage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above | **nil**
| `device.analog.assign_input_low_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })` | Assigns an event handler that triggers whenever the input pin crosses a low threshold.  | `pin` - **string** - The pin name. E.g. `"D0"`<br><br>`handler` - **function** - The function to call whenever the threshold is crossed. This function will be called with one argument of type **boolean** which represents if the value has crossed above or below the threshold. `true` if crossed below, or `false` if crossed above<br><br>`percentage` - **number** - The level represented as a percentage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`voltage` - **number** - The level represented as a voltage at which to trigger the event. Either `percentage` or `voltage` must be provided. Not both.<br><br>`acquisition_time` *optional* - **integer** - As described above<br><br>`range` *optional* - **integer** - As described above | **nil**
| `device.analog.unassign_input_high_event(pin)` | Removes any previously assigned high level event handler attached to a pin | `pin` - **string** - The pin name. E.g. `"D0"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **nil**
| `device.analog.unassign_input_low_event(pin)` | Removes any previously assigned low level event handler attached to a pin | `pin` - **string** - The pin name. E.g. `"D0"`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | **nil**

Example usage:

```lua
-- Read the analog value on pin D1 and print both the percentage and voltage values
local d0_val = device.analog.get_input("D1")
print(d0_val["percentage"])
print(d0_val["voltage"])

-- Trigger a print whenever the voltage on D2 drops below 1.5V
function my_low_voltage_handler(triggered)
    if (triggered) then
        print("Voltage fell below 1.5V")
    else
        print("Voltage has returned back above 1.5V")
    end
end

device.analog.assign_input_high_event("D1", my_low_voltage_handler, { voltage=1.5 })
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
| `device.i2c.read(address, register, length, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400, register_address_size=8 })` | Reads a number of bytes from a register on an I2C connected device | `address` - **integer** - The 7-bit address of the I2C device<br><br>`register` - **integer** - The address of the register to read from<br><br>`length` - **integer** - The number of bytes to read<br><br>`port` *optional* - **string** - The 4-pin port which the I2C device is connected to. I.e. `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`. Using this parameter will assume the SCL and SDA pin order to match the [Stemma QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma) and [Qwiic](https://www.sparkfun.com/qwiic) pinout. If a different pin order is required, the `scl_pin` and `sda_pin` parameters should be provided instead<br><br>`scl_pin` *optional* - **string** - Specifies the pin to use for the SCL signal. Any IO pin may be specified as a string, e.g. `"C3"`. Must be used in conjunction with `sda_pin` and cannot be used if the `port` parameter is already specified.<br><br>`sda_pin` *optional* - **string** - Specifies the pin to use for the SDA signal. Any IO pin may be specified as a string, e.g. `"C4"`. Must be used in conjunction with `scl_pin` and cannot be used if the `port` parameter is already specified.<br><br>`frequency` *optional* - The frequency to use for I2C communications in kHz.<br><br>`register_address_size` *optional* - **integer** - The size of the register to read in bits. Can be either `8`, `16` or `32`. | **table** - A table containing three key-value pairs. `success`, a **boolean** representing if the transaction was a success. `data`, a **string** representing the bytes read. Always of size `length` as specified in the function call. `value`, an **integer** representing the first data value, useful if only one byte was requested
| `device.i2c.write(address, register, data, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400, register_address_size=8 })` | Writes a number of bytes to a register on an I2C connected device | `address` - **integer** - As described above<br><br>`register` - **integer** - As described above<br><br>`data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`<br><br>`port` *optional* - **string** - As described above<br><br>`scl_pin` *optional* - **string** - As described above<br><br>`sda_pin` *optional* - **string** - As described above<br><br>`frequency` *optional* - **integer** - As described above<br><br>`register_address_size` *optional* - **integer** - As described above | **boolean** - Returns `true` if the write was successful, or `false` otherwise

Example usage:

```lua
-- Read a byte from register 0x1F on a device with address 0x23
local result = device.i2c.read(0x23, 0x1F, 1)

if result.success then
    print(result.value)
end

-- Read multiple bytes from the device and print the fourth byte
local result = device.i2c.read(0x23, 0x1F, 4)

if result.success then
    print(result.data[4])
end

-- Write 0x1234 to the register 0xF9
device.i2c.write(0x23, 0xF9, "\x12\x34")
```

### SPI communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.spi.read(register, length, { mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500, register_address_size=8 })` | Reads a number of bytes from a register on an SPI connected device | `register` - **integer** - The address of the register to read from<br><br>`length` - **integer** - The number of bytes to read<br><br>`mosi_pin` *optional* - **string** - Specifies the pin to use for the MOSI signal. Any IO pin may be specified as a string, e.g. "D0".<br><br>`miso_pin` *optional* - **string** - Specifies the pin to use for the MISO signal. Any IO pin may be specified as a string, e.g. "D1".<br><br>`sck_pin` *optional* - **string** - Specifies the pin to use for the SCK signal. Any IO pin may be specified as a string, e.g. "D2".<br><br>`cs_pin` *optional* - **string** - Specifies the pin to use for the CS signal. Any IO pin may be specified as a string, e.g. "D3".<br><br>`frequency` *optional* - **integer** - The frequency to use for SPI transactions in kHz<br><br>`register_address_size` *optional* - **integer** - The size of the register address in bits. Can be either `8`, `16` or `32` | **table** - A table containing two key-value pairs. `data`, a **string** representing the bytes read. Always of size `length` as specified in the function call. `value`, an **integer** representing the first data value, useful if only one byte was requested
| `device.spi.write(register, data, { mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500, register_address_size=8 })`  | Writes a number of bytes to a register on an SPI connected device  | `register` - **integer** - Same as above<br><br>`data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`<br><br>`mosi_pin` *optional* - **string** - As described above<br><br>`miso_pin` *optional* - **string** - As described above<br><br>`sck_pin` *optional* - **string** - As described above<br><br>`cs_pin` *optional* - **string** - As described above<br><br>`frequency` *optional* - **integer** - As described above<br><br>`register_address_size` *optional* - **integer** - As described above | **nil**
| `device.spi.transaction{ read_length, write_data, hold_cs=false, mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500 }` | Reads and writes an arbitrary number of bytes at the same time. I.e while data is being clocked out on the MOSI pin, any data received on the MISO pin will be recorded in parallel. The total number of bytes transacted will therefore be the larger of `read_length` or `write_data`. If you wish to, for example, write 5 bytes, and then read 10 bytes, `read_length` must be set to 15. The first 5 bytes can be ignored, and the remaining 10 bytes will contain the read data | `read_length` - **integer** -  The number of bytes to read<br><br>`write_data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`<br><br>`hold_cs` *optional* - **boolean** - If set to `true` will continue to hold the CS pin low after the transaction is completed. This can be useful if the transaction needs to be broken up into multiple steps, or if the CS pin needs to be held for any other reason. Any subsequent call to `device.spi.transaction` with `hold_cs` set to false will then return the CS pin to a high value once completed<br><br>`mosi_pin` *optional* - **string** - As described above<br><br>`miso_pin` *optional* - **string** - As described above<br><br>`sck_pin` *optional* - **string** - As described above<br><br>`cs_pin` *optional* - **string** - As described above<br><br>`frequency` *optional* - **integer** - As described above | **string** - The bytes read. Always of size `read_length`, or `#write_data`, whichever was larger

Example usage:

```lua
-- Read and print 4 bytes from the 0x12 register
local result = device.spi.read(0x12, 4)

print(result[1])
print(result[2])
print(result[3])
print(result[4])

-- Write a 32-bit value (4 bytes) to the 0xA1 register at 1MHz
device.spi.write(0xA1, "\12\x34\x56\x78", { frequency=1000 })

-- Write 4 bytes to the device and then read back 10 bytes
device.spi.transaction{ write_data="\12\x34\x56\x78", hold_cs=true }
result = device.spi.transaction{ read_length=10 }
```

### UART communication

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### PDM microphone input

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### LTE communication

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `network.send{ data }` | Sends data to Superstack | `data` - **table** - A table representing any data as key-value pairs. Will be converted to an equivalent JSON once it reaches Superstack. It's recommended to name keys in a full and clear way as that will be how the AI tools of Superstack will infer the meaning of the data. E.g. `temperature_celsius = 43.5` will help the AI understand that `43.5` represents temperature in Celsius units | **nil**

Example usage:

```lua
-- A simple sensor value
my_sensor_value = 23.5

network.send{ temperature=my_sensor_value }

-- Network send can contain any arbitrary data
network.send{ 
    some_int = -42, 
    some_float = 23.1
    some_string = "test"
    some_array = {1, 2, 3, 4},
    some_nested_thing = {
        another_int = 54,
        another_string = "test again"
    }
}
```

### GPS

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### Accelerated signal processing

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### Non-volatile memory (file system)

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### Type conversions

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### Timekeeping functions

Details coming soon

<!-- TODO -->
<!--
| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
|  |  |  | 

Example usage:

```lua
```
-->

### Miscellaneous functions

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.sleep(time)` | Puts the device into a low-power sleep for a certain amount of time | `time` - **number** - The time to sleep in seconds. E.g. `1.5` | **nil** 

| Constant | Description | Value |
|----------|-------------|-------|
| `device.HARDWARE_VERSION` | The hardware version of the device | **string** - Always `"s2-module"` 
| `device.FIRMWARE_VERSION` | The current firmware version of the Superstack firmware running on the device | **string** - A string representing the current firmware version. E.g. `"0.1.0+0"`

Example usage:

```lua
-- Print the hardware version, sleep for 1.5 seconds and then print firmware version
print(device.HARDWARE_VERSION)

device.sleep(1.5)

print(device.FIRMWARE_VERSION)
```

## Working with data

Details coming soon
<!-- TODO -->

### Data API

Details coming soon
<!-- TODO -->

## Advanced AI usage

Details coming soon
<!-- TODO -->

### Natural language API

Details coming soon
<!-- TODO -->

## Managing devices & deployments

Details coming soon
<!-- TODO -->

### Un-pairing devices

Details coming soon
<!-- TODO -->

## Managing your subscription

Details coming soon
<!-- TODO -->
