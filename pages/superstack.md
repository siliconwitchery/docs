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

<!-- <table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.digital.set_output(pin,&nbsp;value)</code>
        </td>
        <td>
            Sets or clears a digital output on a pin
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>value</code> - <b>boolean</b> - The level to set on the pin. <code>true</code> for high, or <code>false</code> for low</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table> -->

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.digital.set_output(pin, value)</code>
        </td>
        <td>
            Sets or clears a digital output on a pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>value</code> - <b>boolean</b> - The level to set on the pin. <code>true</code> for high, or <code>false</code> for low</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.get_input(pin, { pull="NO_PULL" })</code>
        </td>
        <td>
            Gets the digital value on a pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>pull</code> - optional <b>string</b> - Selects the pull mode on the pin. Can be <code>PULL_UP</code>, <code>PULL_DOWN</code>, or <code>NO_PULL</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>boolean</b> - <code>true</code> if the pin is high, or <code>false</code> if it's low</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.assign_input_event(pin, handler, { pull="NO_PULL", trigger="BOTH" })</code>
        </td>
        <td>
            Assigns an event handler that triggers whenever the input value of a pin changes.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>handler</code> - <b>function</b> - The function to call whenever the pin value changes. This function will be called with one argument of type <b>boolean</b> which represents the input value on that pin. <code>true</code> if high, or <code>false</code> if low</li>
                <li><code>pull</code> - optional <b>string</b> - As described above</li>
                <li><code>trigger</code> - optional <b>string</b> - The specific transition to trigger the event on. Can be either <code>"LOW_TO_HIGH"</code>, <code>"HIGH_TO_LOW"</code>, or <code>"BOTH"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>metatable</b> - An object representing the event</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.unassign(event)</code>
        </td>
        <td>
            Disables the event and detaches the pin from the handler.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>event</code> - <b>metatable</b> - The object that was returned from <code>device.digital.assign_input_event()</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table>

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

local my_c3_event = device.digital.assign_input_event("C3", my_pin_handler)

-- Disable the event and detach the pin from the handler if no longer needed
my_c3_event:unassign()
```

### Analog input

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.analog.get_input(pin, { acquisition_time=40, range=Vout })</code>
        </td>
        <td>
            Reads the analog value on an analog-capable pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>acquisition_time</code> - optional <b>integer</b> - A time in microseconds across which to make the measurement. Can be either <code>3</code>, <code>5</code>, <code>10</code>, <code>15</code>, <code>20</code>, <code>40</code>, or multiples of 40 e.g. <code>80</code>, <code>120</code>, <code>160</code>, etc. Higher values allow for accurate measurement of greater source resistances. Those maximum resistances being 10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ and 800kΩ respectively, with 800kΩ being the maximum source resistance for acquisition times greater than 40 microseconds</li>
                <li><code>range</code> - optional <b>integer</b> - The maximum expected voltage for the input signal. Defaults to the same value as V<sub>OUT</sub></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>table</b> - A table containing two key-value pairs. <code>voltage</code> a <b>number</b> representing the voltage on the pin, or <code>percentage</code> a <b>number</b> representing the real voltage represented as a percentage with respect to the range of 0V and the <code>range</code> value</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40, range=Vout })</code>
        </td>
        <td>
            Reads the analog value across two analog capable pins.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>positive_pin</code> - <b>string</b> - The pin name of the positive pin</li>
                <li><code>negative_pin</code> - <b>string</b> - The pin name of the negative pin</li>
                <li><code>acquisition_time</code> - optional <b>integer</b> - As described above</li>
                <li><code>range</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>table</b> - Same as above</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.analog.assign_input_high_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })</code>
        </td>
        <td>
            Assigns an event handler that triggers whenever the input pin crosses a high threshold.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>D0</code></li>
                <li><code>handler</code> - <b>function</b> - The function to call whenever the threshold is crossed. This function will be called with one argument of type <b>boolean</b> which represents if the value has crossed above or below the threshold. <code>true</code> if crossed above, or <code>false</code> if crossed below</li>
                <li><code>percentage</code> - <b>number</b> - The level represented as a percentage at which to trigger the event. Either <code>percentage</code> or <code>voltage</code> must be provided, not both</li>
                <li><code>voltage</code> - <b>number</b> - The level represented as a voltage at which to trigger the event. Either <code>percentage</code> or <code>voltage</code> must be provided, not both</li>
                <li><code>acquisition_time</code> - optional <b>integer</b> - As described above</li>
                <li><code>range</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>metatable</b> - An object representing the event</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.analog.assign_input_low_event(pin, handler, { percentage, voltage, acquisition_time=40, range=Vout })</code>
        </td>
        <td>
            Assigns an event handler that triggers whenever the input pin crosses a low threshold.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>D0</code></li>
                <li><code>handler</code> - <b>function</b> - The function to call whenever the threshold is crossed. This function will be called with one argument of type <b>boolean</b> which represents if the value has crossed above or below the threshold. <code>true</code> if crossed above, or <code>false</code> if crossed below</li>
                <li><code>percentage</code> - <b>number</b> - The level represented as a percentage at which to trigger the event. Either <code>percentage</code> or <code>voltage</code> must be provided, not both</li>
                <li><code>voltage</code> - <b>number</b> - The level represented as a voltage at which to trigger the event. Either <code>percentage</code> or <code>voltage</code> must be provided, not both</li>
                <li><code>acquisition_time</code> - optional <b>integer</b> - As described above</li>
                <li><code>range</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li> <b>metatable</b> - As described above</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.analog.unassign(event)</code>
        </td>
        <td>
            Disables the event and detaches the pin from the handler.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>event</code> - <b>metatable</b> - The object that was returned from <code>device.analog.assign_input_high_event()</code> or <code>device.analog.assign_input_low_event()</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table>

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

local my_d1_event = device.analog.assign_input_high_event("D1", my_low_voltage_handler, { voltage=1.5 })

-- Disable the event and detach the pin from the handler if no longer needed
my_d1_event:unassign()
```

### PWM output (analog output)

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.analog.set_output(pin, percentage { frequency=1 })</code>
        </td>
        <td>
            Sets a PWM duty cycle on a pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <b>string</b> - The pin name. E.g. <code>A0</code></li>
                <li><code>percentage</code> - <b>number</b> - The duty cycle to output on the pin as a percentage</li>
                <li><code>frequency</code> - optional <b>number</b> - The PWM frequency in Hz</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table>

Example usage:

```lua
-- Set pin E1 to a 25% duty cycle at the default PWM frequency
device.analog.set_output("E1", 25)
```

### I2C communication

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.i2c.read(address, register, length, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400, register_address_size=8 })</code>
        </td>
        <td>
            Reads a number of bytes from a register on an I2C connected device.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>address</code> - <b>integer</b> - The 7-bit address of the I2C device</li>
                <li><code>register</code> - <b>number</b> - The address of the register to read from</li>
                <li><code>length</code> - <b>integer</b> - The number of bytes to read</li>
                <li><code>port</code> - optional <b>string</b> - The 4-pin port which the I2C device is connected to. I.e. <code>"PORTA"</code>, <code>"PORTB"</code>, <code>"PORTE"</code>, or <code>"PORTF"</code>. Using this parameter will assume the SCL and SDA pin order to match the <a href="https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma">Stemma QT</a> and <a href="https://www.sparkfun.com/qwiic">Qwiic</a> pinout. If a different pin order is required, the <code>scl_pin</code> and <code>sda_pin</code> parameters should be provided instead</li>
                <li><code>scl_pin</code> - optional <b>string</b> - Specifies the pin to use for the SCL signal. Any IO pin may be specified as a string, e.g. <code>"C3"</code>. Must be used in conjunction with <code>sda_pin</code> and cannot be used if the <code>port</code> parameter is already specified</li>
                <li><code>sda_pin</code> - optional <b>string</b> - Specifies the pin to use for the SDA signal. Any IO pin may be specified as a string, e.g. <code>"C4"</code>. Must be used in conjunction with <code>scl_pin</code> and cannot be used if the <code>port</code> parameter is already specified</li>
                <li><code>frequency</code> - optional <b>integer</b> - The frequency to use for I2C communications in kHz. Can be either <code>100</code>, <code>250</code> or <code>400</code></li>
                <li><code>register_address_size</code> - optional <b>integer</b> - The size of the register to read in bits. Can be either <code>8</code>, <code>16</code> or <code>32</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>table</b> - A table containing three key-value pairs. <code>success</code>, a <b>boolean</b> representing if the transaction was a success. <code>data</code>, a <b>string</b> representing the bytes read. Always of size <code>length</code> as specified in the function call. <code>value</code>, an <b>integer</b> representing the first data value, useful if only one byte was requested </li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.i2c.write(address, register, data, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400, register_address_size=8 })</code>
        </td>
        <td>
            Writes a number of bytes to a register on an I2C connected device.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>address</code> - <b>integer</b> - As described above</li>
                <li><code>register</code> - <b>number</b> - As described above</li>
                <li><code>data</code> - <b>string</b> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
                <li><code>port</code> - optional <b>string</b> - As described above</li>
                <li><code>scl_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>sda_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>frequency</code> - optional <b>integer</b> - As described above</li>
                <li><code>register_address_size</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>boolean</b> - Returns <code>true</code> if the write was successful, or <code>false</code> otherwise</li></ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.spi.read(register, length, { mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500, register_address_size=8 })</code>
        </td>
        <td>
            Reads a number of bytes from a register on an SPI connected device.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>register</code> - <b>integer</b> - The address of the register to read from</li>
                <li><code>length</code> - <b>integer</b> - The number of bytes to read</li>
                <li><code>mosi_pin</code> - optional <b>string</b> - Specifies the pin to use for the MOSI signal. Any IO pin may be specified as a string, e.g. <code>"D0"</code></li>
                <li><code>miso_pin</code> - optional <b>string</b> - Specifies the pin to use for the MISO signal. Any IO pin may be specified as a string, e.g. <code>"D1"</code></li>
                <li><code>sck_pin</code> - optional <b>string</b> - Specifies the pin to use for the SCK signal. Any IO pin may be specified as a string, e.g. <code>"D2"</code></li>
                <li><code>cs_pin</code> - optional <b>string</b> - Specifies the pin to use for the CS signal. Any IO pin may be specified as a string, e.g. <code>"D3"</code></li>
                <li><code>frequency</code> - optional <b>integer</b> - The frequency to use for SPI transactions in kHz</li>
                <li><code>register_address_size</code> - optional <b>integer</b> - The size of the register address in bits. Can be either <code>8</code>, <code>16</code> or <code>32</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>table</b> - A table containing two key-value pairs. <code>data</code>, a <b>string</b> representing the bytes read. Always of size <code>length</code> as specified in the function call. <code>value</code>, an <b>integer</b> representing the first data value, useful if only one byte was requested</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.spi.write(register, data, { mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500, register_address_size=8 })</code>
        </td>
        <td>
            Writes a number of bytes from a register on an SPI connected device.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>register</code> - <b>integer</b> - Same as above</li>
                <li><code>data</code> - <b>string</b> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
                <li><code>mosi_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>miso_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>sck_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>cs_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>frequency</code> - optional <b>integer</b> - As described above</li>
                <li><code>register_address_size</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.spi.transaction{ read_length, write_data, hold_cs=false, mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500 }</code>
        </td>
        <td>
            Reads and writes an arbitrary number of bytes at the same time. I.e while data is being clocked out on the MOSI pin, any data received on the MISO pin will be recorded in parallel. The total number of bytes transacted will therefore be the larger of <code>read_length</code> or <code>write_data</code>. If you wish to, for example, write 5 bytes, and then read 10 bytes, <code>read_length</code> must be set to 15. The first 5 bytes can be ignored, and the remaining 10 bytes will contain the read data.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>read_length</code> - <b>integer</b> - The number of bytes to read from</li>
                <li><code>write_data</code> - <b>string</b> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
                <li><code>hold_cs</code> - optional <b>boolean</b> - If set to <code>true</code> will continue to hold the CS pin low after the transaction is completed. This can be useful if the transaction needs to be broken up into multiple steps, or if the CS pin needs to be held for any other reason. Any subsequent call to <code>device.spi.transaction</code> with <code>hold_cs</code> set to false will then return the CS pin to a high value once completed</li>
                <li><code>mosi_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>miso_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>sck_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>cs_pin</code> - optional <b>string</b> - As described above</li>
                <li><code>frequency</code> - optional <b>integer</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>string</b> - The bytes read. Always of size <code>read_length</code>, or <code>#write_data</code>, whichever was larger</li></ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.uart.write(data, { baudrate=9600, tx_pin="B1", cts_pin=nil, parity=false, stop_bits=1 })</code>
        </td>
        <td>
            Writes UART data to a pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>data</code> - <b>string</b> - The data to send</li>
                <li><code>baudrate</code> - optional <b>integer</b> - The baudrate in bits-per-second at which to send the data. Can be <code>1200</code>, <code>2400</code>, <code>4800</code>, <code>9600</code>, <code>14400</code>, <code>19200</code>, <code>28800</code>, <code>31250</code>, <code>38400</code>, <code>56000</code>, <code>57600</code>, <code>76800</code>, <code>115200</code>, <code>230400</code>, <code>250000</code>, <code>460800</code>, <code>921600</code>, or <code>1000000</code></li>
                <li><code>tx_pin</code> - optional <b>string</b> - Specifies the pin to use for the transmit signal. Any IO pin may be specified as a string, e.g. <code>"C1"</code></li>
                <li><code>cts_pin</code> - optional <b>string</b> - Specifies the pin to use for the clear-to-send signal. Any IO pin may be specified as a string, e.g. <code>"C3"</code>. If <code>nil</code> is given, the signal isn't used</li>
                <li><code>parity</code> - optional <b>boolean</b> - Enables the parity bit if set to <code>true</code></li>
                <li><code>stop_bits</code> - optional <b>integer</b> - Sets the number of stop bits. Can be either <code>1</code> or <code>2</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.uart.assign_read_event(terminator, handler, { baudrate=9600, rx_pin="B0", tx_pin="B1", rts_pin=nil, cts_pin=nil, parity=false, stop_bits=1 })</code>
        </td>
        <td>
            Buffers UART data from a pin, and triggers an event whenever a specified terminating character is seen.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>terminator</code> - <b>string</b> - The character to wait for until triggering the event. If set to <code>nil</code>, the event is triggered for every new character received</li>
                <li><code>handler</code> - <b>function</b> - The function to call whenever data is received. This function will be called with one argument of type <b>string</b> which will contain all the buffered bytes since the last event was triggered, or the event was enabled</li>
                <li><code>baudrate</code> - optional <b>integer</b> - As described above</li>
                <li><code>rx_pin</code> - optional <b>string</b> - Specifies the pin to use for the receive signal. Any IO pin may be specified as a string, e.g. <code>"C0"</code></li>
                <li><code>rts_pin</code> - optional <b>string</b> - Specifies the pin to use for the ready-to-send signal. Any IO pin may be specified as a string, e.g. <code>"C2"</code>. If <code>nil</code> is given, the signal isn't used</li>
                <li><code>parity</code> - optional <b>boolean</b> - As described above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>metatable</b> - An object representing the event</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.uart.unassign(event)</code>
        </td>
        <td>
            Disables the event and detaches the pin from the handler.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>event</code> - <b>metatable</b> - The object that was returned from <code>device.uart.assign_read_event()</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table>

Example usage:

```lua
-- Create a handler for receiving UART data
function my_receive_handler(data)
    print("Got a new line: "..data)
end

local my_rx_event = device.uart.assign_read_event("\n", my_receive_handler, { baudrate=19200 })

-- Send UART data
device.uart.write("Hello there. This is some data\n", { baudrate=19200 })

-- Disable the event and detach the pin from the handler if no longer needed
my_rx_event:unassign()
```

### PDM microphone input

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.audio.record(length, handler, { data_pin="E0", clock_pin="E1", sample_rate=8000, bit_depth=8 })</code>
        </td>
        <td>
            Begins recording microphone input and and outputs the data to an event handler. The handler is called every <code>length</code> seconds and repeats until the <code>stop()</code> function is called.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>length</code> - <b>float</b> - The length to record in seconds. The maximum allowable time will depend on the RAM currently used on the device. Using a lower <code>sample_rate</code> and <code>bit_depth</code> will allow for longer recordings but at reduced quality</li>
                <li><code>handler</code> - <b>function</b> - The function to call whenever data is ready to be processed. The function will be called with one argument of type <b>string</b> representing 1-byte-per-sample in the case of <code>bit_depth=8</code>, or 2-bytes-per-sample in the case of <code>bit_depth=16</code>. The samples will be signed values. This function should not spend longer than <code>length</code> time to process the data and exit, otherwise the internal buffer will overflow and cause glitches in the final audio</li>
                <li><code>data_pin</code> - optional <b>string</b> - Specifies the pin to use for the data input. Any IO pin may be specified as a string, e.g. <code>"F0"</code></li>
                <li><code>clock_pin</code> - optional <b>string</b> - Specifies the pin to use for the clock input. Any IO pin may be specified as a string, e.g. <code>"F1"</code></li>
                <li><code>sample_rate</code> - <b>integer</b> - The sample rate to record in samples per second. Can be either <code>8000</code> or <code>16000</code></li>
                <li><code>but_depth</code> - <b>integer</b> - he dynamic range of the samples recorded. Can be either <code>8</code> or <code>16</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><b>metatable</b> - An object representing the event</li></ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.audio.stop(event)</code>
        </td>
        <td>
            Stops recording samples and calls the event handler one last time with any remaining data in the internal buffer.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>event</code> - <b>metatable</b> - The object that was returned from <code>device.uart.assign_read_event()</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li>nil</li></ul>
        </td>
    </tr>
</table>

Example usage:

```lua
-- Create a handler for receiving and processing audio samples
function my_microphone_handler(data)
    for i = 1, #data do
        local value = string.sub(data, i, i)
        
        if value > 128 or value < -128 then
            print("Loud noise detected")
        end
    end
end

-- Will capture 1s worth of audio at a time
local my_mic_event = device.audio.record(1, my_microphone_handler)

-- Recording can be stopped at any time
my_mic_event:stop()
```

### Sleep, power & system info

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `device.sleep(time)` | Puts the device into a low-power sleep for a certain amount of time | `time` - **number** - The time to sleep in seconds. E.g. `1.5` | **nil** 
| `device.power.battery.set_charger_cv_cc(voltage, current)` | Sets the termination voltage and constant current values for the charger | `voltage` - **number** - The termination voltage of the cell. Can be either `3.50`, `3.55`, `3.60`, `3.65`, `4.00`, `4.05`, `4.10`, `4.15`, `4.20`, `4.25`, `4.30`, `4.35`, `4.40`, or `4.45`<br><br>`current` - **number** - The constant current to charge the cell at. Must be between `32` and `800` in steps of `2` | **nil**
| `device.power.battery.get_voltage()` | Gets the voltage of the cell | - | **number** - The voltage of the cell in volts
| `device.power.battery.get_charging_status()` | Gets the charging status of the cell | - | **string** - The current charging status. Either `charging`, `charged` or `discharging` if the battery is connected, or `external_power` if either no battery is installed, or the battery has a fault |
| `device.power.set_vout(voltage)` | Sets the voltage of V<sub>OUT</sub> | `voltage` - **number** - The voltage to set. Can be between `1.8` and `3.3` in steps of `0.1` | **nil**`

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

-- Configure the battery charger for a 4.2V 200mAh rated Li-Po cell
device.power.battery.set_charger_cv_cc(4.2, 200)

-- Get the current battery status
local voltage = device.power.battery.get_voltage()
local status = device.power.battery.get_charging_status()

if status ~= "external_power" then
    print("Battery is "..status)
    print("Battery voltage is "..tostring(voltage).."V")
else
    print("Battery not connected. On external power")
end

-- Set the voltage of Vout to 3.3V
device.power.set_vout(3.3)
```

### Networking (LTE)

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

### Location (GPS)

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `location.get_latest()` | Returns the latest GPS data | - | **table** - A table containing key-value pairs. `valid`, a **boolean** representing if the GPS data is valid. `latitude`, a **number** representing the latitude. `longitude`, a **number** representing the longitude. `altitude`, a **number** representing the altitude. `accuracy`, a **number** representing the location and altitude accuracy. `speed`, a **number** representing the current speed. `speed_accuracy`, a **number** representing the speed accuracy. `satellites`, a **table** representing the current satellites statistics. `satellites` in turn contains three key-value pairs. `tracked`. an **integer** representing the number of satellites currently being tracked. `in_fix`. an **integer** representing the number of satellites currently being used for measurement. `unhealthy`. an **integer** representing the number of satellites that could not be used for measurement. |
| `location.set_options({ accuracy="HIGH", power_saving="MEDIUM", tracking_interval=1 })` | Sets options related to the GPS module | `accuracy` *optional* - **string** - The accuracy of the reading to acquire. Can either be `"LOW"` where only three satellites are required to attain a fix, or `"HIGH"` where four satellites are required to attain a fix<br><br>`power_saving` *optional* - **string** - The level of power saving that the GPS aim to achieve. Can either be `"OFF"`, `"MEDIUM"`, `"MAX"`. A higher level of power saving will result in less accuracy and a slower time to attain a fix<br><br>`tracking_interval` *optional* - **integer** - The period to poll for new location updates. Can either be `1` for continuous 1-second updates, or a value in seconds between `10` and `65535` for slower updates which can save power | **nil**

Example usage:

```lua
location.set_options({ accuracy = "LOW" })

while true do

    local l = location.get_latest()

    print("valid: " .. tostring(l["valid"]))
    print("latitude: " .. tostring(l["latitude"]))
    print("longitude: " .. tostring(l["longitude"]))
    print("altitude: " .. tostring(l["altitude"]))
    print("accuracy: " .. tostring(l["accuracy"]))
    print("speed: " .. tostring(l["speed"]))
    print("speed_accuracy: " .. tostring(l["speed_accuracy"]))

    print("satellites tracked: " .. tostring(l["satellites"]["tracked"]))
    print("satellites in fix: " .. tostring(l["satellites"]["in_fix"]))
    print("satellites unhealthy: " .. tostring(l["satellites"]["unhealthy"]))

    -- Note that LTE network activity (including logging) will interrupt the
    -- GPS and delay attaining a fix. Therefore the device should avoid
    -- network activity for a brief period of time while waiting for a fix
    device.sleep(30)
end
```

### File storage

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `storage.write(filename, data)` | Creates a file and writes data to it. If the file already exists, it is overwritten | `filename` - **string** - The name of the file<br><br>`data` - **string** - The data to save to the file | **nil**
| `storage.append(filename, data)` | Creates a file and writes data to it. If the file already exists, the new data is appended to the current contents of the file | `filename` - **string** - As described above<br><br>`data` - **string** - As described above | **nil**
| `storage.read(filename, { line=-1, length=nil, offset=0 })` | Reads out the contents of the file. Either returning an entire `"\n"` terminated line, or alternatively, a number of bytes with length `length` at an offset of `offset` | `filename` - **string** - As described above<br><br>`line` *optional* - **integer** - The index of the line to return. `1` being the first line, `2` being the second line, etc. Likewise, the lines can also be indexed from the end of the file. `-1` returns the last line of the file, `-2` the second to last, etc. `length` and `offset` are ignored when `line` is specified<br><br>`length` *optional* - **integer** - The number of bytes to read from the file. Cannot be used with the `line` option. If `length` is longer than the data present in the file, then a shorter result will be returned<br><br>`offset` *optional* - **integer** - When `length` is specified, this option allows reading from some arbitrary offset from within the file | **string** - The contents read
| `storage.delete(filename)` | Deletes a file if it exists | `filename` - **string** - As described above | **bool** - `true` if the file was found and deleted, `false` otherwise
| `storage.list()` | Lists all the files stored on the device | - | **table** - A table of **strings** representing each file saved on the device

Example usage:

```lua
-- Create a file and read it
storage.write("my_file.txt", "Hello world")

print(storage.read("my_file.txt"))

-- Append more data to the file
storage.append("my_file.txt", "\nThis is another line of text")
storage.append("my_file.txt", "\nAnd this is a final line of text")

-- Print the last line from the file
print(storage.read("my_file.txt", { line=-1 }))

-- Delete the file
storage.delete("my_file.txt")
```

### Timekeeping

| Function | Description | Parameters | Returns |
|----------|-------------|------------|---------|
| `time.get_unix_time()` | Returns the current Unix epoch known by the device | - | **number** - The number of seconds since 00:00:00 UTC on 1 January 1970 with a resolution of 1mS. If the device hasn't yet connected to the network to acquire the time, the returned value represents the number of seconds since the device was powered on
| `time.get_time_date({unix_epoch, timezone})` | Gets the current time and date known by the device | `unix_epoch` *optional* - **number** - If supplied, the time and date at the given unix epoch will be returned. Otherwise the current time is used<br><br> `timezone` *optional* - **string** - The timezone to observe when returning the time and date. Can be given as a standard timezone abbreviation such as "EST", "GMT", or "CEST". If not used, the timezone of the network is used | **table** - A table containing key-value pairs. `known` a **boolean** representing if the device has obtained the time from the network, `second` an **integer** representing the current second. `minute` an **integer** representing the current minute. `hour` an **integer** representing the current hour. `day` an **integer** representing the current day. `weekday` a **string** representing the current weekday. `month` an **integer** representing the current month. `year` an **integer** representing the current year. `timezone` a **string** representing the current timezone as a standard timezone abbreviation |

Example usage:

```lua
-- Repeat something for 30 seconds
local t = time.get_unix_time()

while t + 30 > time.get_unix_time() do
    print("waiting")
    device.sleep(5)
end

-- Print the current time and date
local now = time.get_time_date()

print(string.format("The current time is: %02d:%02d", now.minute, now.hour))
print(string.format("The current date is: %d/%d/%d", now.year, now.month, now.day))
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
