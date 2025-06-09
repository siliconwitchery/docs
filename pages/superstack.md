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
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
                <li><code>value</code> - <strong>boolean</strong> - The level to set on the pin. <code>true</code> for high, or <code>false</code> for low</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.get_input(pin, { pull="PULL_DOWN" })</code>
        </td>
        <td>
            Gets the digital value on a pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>pull</code> - <strong>string</strong> - Selects the pull mode on the pin. Can be <code>"PULL_UP"</code>, <code>"PULL_DOWN"</code>, or <code>"NO_PULL"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>boolean</strong> - <code>true</code> if the pin is high, or <code>false</code> if it's low</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.assign_input_event(pin, handler, { pull="PULL_DOWN" })</code>
        </td>
        <td>
            Assigns an event handler that triggers whenever the input value of a pin changes.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
                <li><code>handler</code> - <strong>function</strong> - The function to call whenever the pin value changes. This function will be called with two arguments:</li>
                <ul>
                    <li><code>pin</code> - <strong>string</strong> - The pin name that generated the event. E.g. <code>A0</code></li>
                    <li><code>state</code> - <strong>boolean</strong> - The value on the pin when the event occurred. <code>true</code> if the pin was high, or <code>false</code> if the pin was low</li>
                </ul>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>pull</code> - <strong>string</strong> - Selects the pull mode on the pin. Can be <code>"PULL_UP"</code>, <code>"PULL_DOWN"</code>, or <code>"NO_PULL"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.digital.unassign_input_event(pin)</code>
        </td>
        <td>
            Disables the event and detaches the pin from the handler.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
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
function my_pin_handler(pin, state)
    if state == true then
        print(pin.." went high")
    else
        print(pin.." went low")
    end
end

device.digital.assign_input_event("C3", my_pin_handler)

-- Disable the event and detach the pin from the handler if no longer needed
device.digital.unassign_input_event("C3")
```

### Analog input

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.analog.get_input(pin, { acquisition_time=40 })</code>
        </td>
        <td>
            Reads the analog value on an analog-capable pin.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>acquisition_time</code> - <strong>integer</strong> - A time in microseconds across which to make the measurement. Can be either <code>3</code>, <code>5</code>, <code>10</code>, <code>15</code>, <code>20</code>, or <code>40</code>. Higher values allow for accurate measurement of greater source resistances. Those maximum resistances being 10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ and 800kΩ respectively</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>number</strong> - The voltage present on the pin</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40 })</code>
        </td>
        <td>
            Reads the analog value across two analog capable pins.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>positive_pin</code> - <strong>string</strong> - The pin name of the positive pin</li>
                <li><code>negative_pin</code> - <strong>string</strong> - The pin name of the negative pin</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>acquisition_time</code> - <strong>integer</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>number</strong> - The voltage present on the pin</li>
            </ul>
        </td>
    </tr>
</table>

Example usage:

```lua
-- Read the analog value on pin D1 and print both the percentage and voltage values
local d0_val = device.analog.get_input("D1")
print(d0_val.percentage)
print(d0_val.voltage)

-- Trigger a print whenever the voltage on D2 drops below 1.5V
function my_low_voltage_handler(pin, exceeded)
    if (exceeded) then
        print("Voltage fell below 1.5V")
    else
        print("Voltage has returned back above 1.5V")
    end
end

device.analog.assign_input_high_event("D1", my_low_voltage_handler, { voltage=1.5 })

-- Disable the event and detach the pin from the handler if no longer needed
device.analog.unassign_input_event("D1")
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
                <li><code>pin</code> - <strong>string</strong> - The pin name. E.g. <code>A0</code></li>
                <li><code>percentage</code> - <strong>number</strong> - The duty cycle to output on the pin as a percentage</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>frequency</code> - <strong>number</strong> - The PWM frequency in Hz</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
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
                <li><code>address</code> - <strong>integer</strong> - The 7-bit address of the I2C device</li>
                <li><code>register</code> - <strong>number</strong> - The address of the register to read from</li>
                <li><code>length</code> - <strong>integer</strong> - The number of bytes to read</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>port</code> - <strong>string</strong> - The 4-pin port which the I2C device is connected to. I.e. <code>"PORTA"</code>, <code>"PORTB"</code>, <code>"PORTE"</code>, or <code>"PORTF"</code>. Using this parameter will assume the SCL and SDA pin order to match the <a href="https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma">Stemma QT</a> and <a href="https://www.sparkfun.com/qwiic">Qwiic</a> pinout. If a different pin order is required, the <code>scl_pin</code> and <code>sda_pin</code> parameters should be provided instead</li>
                <li><code>scl_pin</code> - <strong>string</strong> - The pin name to use for the SCL signal. E.g <code>"C3"</code>. Must be used in conjunction with <code>sda_pin</code> and cannot be used if the <code>port</code> parameter is already specified</li>
                <li><code>sda_pin</code> - <strong>string</strong> - The pin name to use for the SDA signal. E.g <code>"C4"</code>. Must be used in conjunction with <code>scl_pin</code> and cannot be used if the <code>port</code> parameter is already specified</li>
                <li><code>frequency</code> - <strong>integer</strong> - The frequency to use for I2C communications in kHz. Can be either <code>100</code>, <code>250</code> or <code>400</code></li>
                <li><code>register_address_size</code> - <strong>integer</strong> - The size of the register to read in bits. Can be either <code>8</code>, <code>16</code> or <code>32</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of key-value pairs:</li>
                <ul>
                    <li><code>success</code> - <strong>string</strong> - <code>true</code> if the transaction was a success, or <code>false</code> otherwise</li>
                    <li><code>data</code> - <strong>string</strong> - The bytes read. Always of size <code>length</code> as specified in the function call</li>
                    <li><code>value</code> - <strong>string</strong> - The first data value, useful if only one byte was requested</li>
                </ul>
            </ul>
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
                <li><code>address</code> - <strong>integer</strong> - Same as above</li>
                <li><code>register</code> - <strong>number</strong> - Same as above</li>
                <li><code>data</code> - <strong>string</strong> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>port</code> - <strong>string</strong> - Same as above</li>
                <li><code>scl_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>sda_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>frequency</code> - <strong>integer</strong> - Same as above</li>
                <li><code>register_address_size</code> - <strong>integer</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>boolean</strong> - <code>true</code> if the transaction was a success, or <code>false</code> otherwise</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.i2c.scan({ port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400 })</code>
        </td>
        <td>
            Scans the given port for all connected I2C devices.
            <br><br>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>port</code> - <strong>string</strong> - Same as above</li>
                <li><code>scl_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>sda_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>frequency</code> - <strong>integer</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of <strong>integers</strong> listing the 7-bit addresses of all the devices found</li>
            </ul>
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

-- Scan a port for devices
local d = device.i2c.scan({port="PORTF"})

print("Found " .. tostring(#d) .. " devices")
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
                <li><code>register</code> - <strong>integer</strong> - The address of the register to read from</li>
                <li><code>length</code> - <strong>integer</strong> - The number of bytes to read</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>mosi_pin</code> - <strong>string</strong> - The pin name to use for the MOSI signal. E.g <code>"D0"</code></li>
                <li><code>miso_pin</code> - <strong>string</strong> - The pin name to use for the MISO signal. E.g <code>"D1"</code></li>
                <li><code>sck_pin</code> - <strong>string</strong> - The pin name to use for the SCK signal. E.g <code>"D2"</code></li>
                <li><code>cs_pin</code> - <strong>string</strong> - The pin name to use for the CS signal. E.g <code>"D3"</code></li>
                <li><code>frequency</code> - <strong>integer</strong> - The frequency to use for SPI transactions in kHz</li>
                <li><code>register_address_size</code> - <strong>integer</strong> - The size of the register address in bits. Can be either <code>8</code>, <code>16</code> or <code>32</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of key-value pairs:</li>
                <ul>
                    <li><code>data</code> - <strong>string</strong> - The bytes read. Always of size <code>length</code> as specified in the function call</li>
                    <li><code>value</code> - <strong>string</strong> - The first data value, useful if only one byte was requested</li>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.spi.write(register, data, { mosi_pin="C0", miso_pin="C1", sck_pin="C2", cs_pin="C3", frequency=500, register_address_size=8 })</code>
        </td>
        <td>
            Writes a number of bytes to a register on an SPI connected device.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>register</code> - <strong>integer</strong> - Same as above</li>
                <li><code>data</code> - <strong>string</strong> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>mosi_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>miso_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>sck_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>cs_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>frequency</code> - <strong>integer</strong> - Same as above</li>
                <li><code>register_address_size</code> - <strong>integer</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul><li><strong>nil</strong></li></ul>
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
                <li><code>read_length</code> - <strong>integer</strong> - The number of bytes to read from</li>
                <li><code>write_data</code> - <strong>string</strong> - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. <code>"\x1A\x50\x00\xF1"</code></li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>hold_cs</code> - <strong>boolean</strong> - If set to <code>true</code> will continue to hold the CS pin low after the transaction is completed. This can be useful if the transaction needs to be broken up into multiple steps. Any subsequent call to <code>device.spi.transaction</code> with <code>hold_cs</code> set to false will then return the CS pin to a high value once completed</li>
                <li><code>mosi_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>miso_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>sck_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>cs_pin</code> - <strong>string</strong> - Same as above</li>
                <li><code>frequency</code> - <strong>integer</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>string</strong> - The bytes read. Always of size <code>length</code> as specified in the function call</li>
            </ul>
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
                <li><code>data</code> - <strong>string</strong> - The data to send</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>baudrate</code> - <strong>integer</strong> - The baudrate in bits-per-second at which to send the data. Can be <code>1200</code>, <code>2400</code>, <code>4800</code>, <code>9600</code>, <code>14400</code>, <code>19200</code>, <code>28800</code>, <code>31250</code>, <code>38400</code>, <code>56000</code>, <code>57600</code>, <code>76800</code>, <code>115200</code>, <code>230400</code>, <code>250000</code>, <code>460800</code>, <code>921600</code>, or <code>1000000</code></li>
                <li><code>tx_pin</code> - <strong>string</strong> - The pin name to use for the transmit signal. E.g <code>"C1"</code></li>
                <li><code>cts_pin</code> - <strong>string</strong> - The pin name to use for the clear-to-send signal. E.g <code>"C3"</code>. If <code>nil</code> is given, the signal isn't used</li>
                <li><code>parity</code> - <strong>boolean</strong> - Enables the parity bit if set to <code>true</code></li>
                <li><code>stop_bits</code> - <strong>integer</strong> - Sets the number of stop bits. Can be either <code>1</code> or <code>2</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
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
                <li><code>terminator</code> - <strong>string</strong> - The character to wait for until triggering the event. If set to <code>nil</code>, the event is triggered for every new character received</li>
                <li><code>handler</code> - <strong>function</strong> - The function to call whenever data is received. This function will be called with one argument:</li>
                <ul>
                    <li><code>data</code> - <strong>string</strong> - All the buffered bytes since the last event was triggered, or the event was enabled</li>
                </ul>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>baudrate</code> - <strong>integer</strong> - Same as above</li>
                <li><code>rx_pin</code> - <strong>string</strong> - The pin name to use for the receive signal. E.g <code>"C0"</code></li>
                <li><code>rts_pin</code> - <strong>string</strong> - The pin name to use for the ready-to-send signal. E.g <code>"C2"</code>. If <code>nil</code> is given, the signal isn't used</li>
                <li><code>parity</code> - <strong>boolean</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.uart.unassign_read_event(rx_pin)</code>
        </td>
        <td>
            Disables the event and detaches the pin from the handler.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>rx_pin</code> - <strong>string</strong> - The pin name of the receive signal. E.g <code>"C0"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
</table>

Example usage:

```lua
-- Create a handler for receiving UART data
function my_receive_handler(data)
    print("Got a new line: "..data)
end

device.uart.assign_read_event("\n", my_receive_handler, { baudrate=19200 })

-- Send UART data
device.uart.write("Hello there. This is some data\n", { baudrate=19200 })

-- Disable the event and detach the pin from the handler if no longer needed
device.uart.unassign_read_event("B0")
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
                <li><code>length</code> - <strong>float</strong> - The length to record in seconds. The maximum allowable time will depend on the RAM currently used on the device. Using a lower <code>sample_rate</code> and <code>bit_depth</code> will allow for longer recordings but at reduced quality</li>
                <li><code>handler</code> - <strong>function</strong> - The function to call whenever data is ready to be processed. The function will be called with one argument:</li>
                <ul>
                    <li><code>data</code> - <strong>string</strong> - Audio data as 1-byte-per-sample in the case of <code>bit_depth=8</code>, or 2-bytes-per-sample in the case of <code>bit_depth=16</code>. The samples will be signed values. This function should not spend longer than <code>length</code> time to process the data and exit, otherwise the internal buffer will overflow and cause glitches in the final audio</li>
                </ul>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>data_pin</code> - <strong>string</strong> - The pin name to use for the data input. E.g <code>"F0"</code></li>
                <li><code>clock_pin</code> - <strong>string</strong> - The pin name to use for the clock input. E.g <code>"F1"</code></li>
                <li><code>sample_rate</code> - <strong>integer</strong> - The sample rate to record in samples per second. Can be either <code>8000</code> or <code>16000</code></li>
                <li><code>but_depth</code> - <strong>integer</strong> - he dynamic range of the samples recorded. Can be either <code>8</code> or <code>16</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.audio.stop(data_pin)</code>
        </td>
        <td>
            Stops recording samples and calls the event handler one last time with any remaining data in the internal buffer.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>data_pin</code> - <strong>string</strong> - The pin name of the data input. E.g <code>"F0"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
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
device.audio.record(1, my_microphone_handler)

-- Recording can be stopped at any time
device.audio.stop("E0")
```

### Sleep, power & system info

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.sleep(time)</code>
        </td>
        <td>
            Puts the device into a low-power sleep for a certain amount of time.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>time</code> - <strong>number</strong> - The time to sleep in seconds. E.g. <code>1.5</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.power.battery.set_charger_cv_cc(voltage, current)</code>
        </td>
        <td>
            Sets the termination voltage and constant current values for the charger.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>voltage</code> - <strong>number</strong> - The termination voltage of the cell. Can be either <code>3.50</code>, <code>3.55</code>, <code>3.60</code>, <code>3.65</code>, <code>4.00</code>, <code>4.05</code>, <code>4.10</code>, <code>4.15</code>, <code>4.20</code>, <code>4.25</code>, <code>4.30</code>, <code>4.35</code>, <code>4.40</code>, or <code>4.45</code></li>
                <li><code>current</code> - <strong>number</strong> - The constant current to charge the cell at. Must be between <code>32</code> and <code>800</code> in steps of <code>2</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.power.battery.get_voltage()</code>
        </td>
        <td>
            Gets the voltage of the cell.
            <br><br>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>number</strong> - The voltage of the cell in volts</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.power.battery.get_charging_status()</code>
        </td>
        <td>
            Gets the charging status of the cell.
            <br><br>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>string</strong> - The current charging status. Either <code>charging</code>, <code>charged</code> or <code>discharging</code> if the battery is connected, or <code>external_power</code> if either no battery is installed, or the battery has a fault</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.power.battery.set_vout(voltage)</code>
        </td>
        <td>
            Sets the voltage of V<sub>OUT</sub>.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>voltage</code> - <strong>number</strong> - The voltage to set. Can be between <code>1.8</code> and <code>3.3</code> in steps of <code>0.1</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
</table>

<table>
    <tr>
        <th>Constant</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>device.HARDWARE_VERSION</code>
        </td>
        <td>
            The hardware version of the device.
            <br><br>
            <strong>Returns:</strong>
            <ul>
                <li><strong>string</strong> - Always <code>"s2-module"</code></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>device.FIRMWARE_VERSION</code>
        </td>
        <td>
            The current firmware version of the Superstack firmware running on the device.
            <br><br>
            <strong>Returns:</strong>
            <ul>
                <li><strong>string</strong> - A string representing the current firmware version. E.g. <code>"0.1.0+0"</code></li>
            </ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>network.send{ data }</code>
        </td>
        <td>
            Sends data to Superstack.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>data</code> - <strong>table</strong> - A table representing any data as key-value pairs. Will be converted to an equivalent JSON once it reaches Superstack. It's recommended to name keys in a full and clear way as that will be how the AI tools of Superstack will infer the meaning of the data. E.g. <code>temperature_celsius = 43.5</code> will help the AI understand that <code>43.5</code> represents temperature in Celsius units</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>location.get_latest()</code>
        </td>
        <td>
            Returns the latest GPS data.
            <br><br>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of key-value pairs:</li>
                <ul>
                    <li><code>valid</code> - <strong>boolean</strong> - <code>true</code> if the GPS data is valid, or <code>false</code> otherwise</li>
                    <li><code>latitude</code> - <strong>number</strong> - The current latitude</li>
                    <li><code>longitude</code> - <strong>number</strong> - The current longitude</li>
                    <li><code>altitude</code> - <strong>number</strong> - The current altitude</li>
                    <li><code>accuracy</code> - <strong>number</strong> - The location and altitude accuracy</li>
                    <li><code>speed</code> - <strong>number</strong> - The current speed</li>
                    <li><code>speed_accuracy</code> - <strong>number</strong> - The speed accuracy</li>
                    <li><code>satellites</code> - <strong>table</strong> - A table of key-value pairs:</li>
                    <ul>
                        <li><code>tracked</code> - <strong>integer</strong> - The number of satellites currently being tracked</li>
                        <li><code>in_fix</code> - <strong>integer</strong> - The number of satellites currently being used for measurement</li>
                        <li><code>unhealthy</code> - <strong>integer</strong> - The number of satellites that could not be used for measurement</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>location.set_options({ accuracy="HIGH", power_saving="MEDIUM", tracking_interval=1 })</code>
        </td>
        <td>
            Sets options related to the GPS module.
            <br><br>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>accuracy</code> - <strong>string</strong> - The accuracy of the reading to acquire. Can either be <code>"LOW"</code> where only three satellites are required to attain a fix, or <code>"HIGH"</code> where four satellites are required to attain a fix</li>
                <li><code>power_saving</code> - <strong>string</strong> - The level of power saving that the GPS aim to achieve. Can either be <code>"OFF"</code>, <code>"MEDIUM"</code>, <code>"MAX"</code>. A higher level of power saving will result in less accuracy and a slower time to attain a fix</li>
                <li><code>tracking_interval</code> - <strong>integer</strong> -  The period to poll for new location updates. Can either be <code>1</code> for continuous 1-second updates, or a value in seconds between <code>10</code> and <code>65535</code> for slower updates which can save power</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>storage.write(filename, data)</code>
        </td>
        <td>
            Creates a file and writes data to it. If the file already exists, it is overwritten.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>filename</code> - <strong>string</strong> - The name of the file</li>
                <li><code>data</code> - <strong>string</strong> - The data to save to the file</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>storage.append(filename, data)</code>
        </td>
        <td>
            Creates a file and writes data to it. If the file already exists, the new data is appended to the current contents of the file.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>filename</code> - <strong>string</strong> - Same as above</li>
                <li><code>data</code> - <strong>string</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>nil</strong></li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>storage.read(filename, { line=-1, length=nil, offset=0 })</code>
        </td>
        <td>
            Reads out the contents of the file. Either returning an entire <code>"\n"</code> terminated line, or alternatively, a number of bytes with length <code>length</code> at an offset of <code>offset</code>.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>filename</code> - <strong>string</strong> - Same as above</li>
            </ul>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>line</code> - <strong>integer</strong> - The index of the line to return. <code>1</code> being the first line, <code>2</code> being the second line, etc. Likewise, the lines can also be indexed from the end of the file. <code>-1</code> returns the last line of the file, <code>-2</code> the second to last, etc. <code>length</code> and <code>offset</code> are ignored when <code>line</code> is specified</li>
                <li><code>length</code></li> - <strong>integer</strong> - The number of bytes to read from the file. Cannot be used with the <code>line</code> option. If <code>length</code> is longer than the data present in the file, then a shorter result will be returned</li>
                <li><code>offset</code></li> - <strong>integer</strong> - When <code>length</code> is specified, this option allows reading from some arbitrary offset from within the file</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>string</strong> - The contents read</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>storage.delete(filename)</code>
        </td>
        <td>
            Deletes a file if it exists.
            <br><br>
            <strong>Parameters:</strong>
            <ul>
                <li><code>filename</code> - <strong>string</strong> - Same as above</li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>boolean</strong> - <code>true</code> if the file was found and deleted, <code>false</code> otherwise</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>storage.list()</code>
        </td>
        <td>
            Lists all the files stored on the device as a list of tables containing the filename and size.
            <br><br>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of <strong>tables</strong>:</li>
                <ul>
                    <li><strong>table</strong> - A table of key-value pairs:</li>
                    <ul>
                        <li><code>name</code> - <strong>string</strong> - The name of the file</li>
                        <li><code>size</code> - <strong>integer</strong> - The size of the file in bytes</li>
                    </ul>
                </ul>
            </ul>
        </td>
    </tr>
</table>

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

<table>
    <tr>
        <th>Function</th>
        <th>Details</th>
    </tr>
    <tr>
        <td>
            <code>time.get_unix_time()</code>
        </td>
        <td>
            Returns the current Unix timestamp (i.e the number of non-leap milliseconds that have elapsed since 00:00:00 UTC on 1 January 1970), or if the time is not yet known, returns the uptime of the device in milliseconds.
            <br><br>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>integer</strong> - A number of milliseconds</li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            <code>time.get_time_date({unix_epoch, timezone})</code>
        </td>
        <td>
            Gets either the current time and date information, or the time and date for a specified Unix timestamp.
            <br><br>
            <strong>Optional parameters:</strong>
            <ul>
                <li><code>unix_epoch</code> - <strong>number</strong> - A Unix timestamp that should be converted to a real time and date</li>
                <li><code>timezone</code> - <strong>string</strong> - The timezone to observe when returning the time and date. Can be given as a standard timezone offset such as <code>"+02:00"</code> or <code>"-07:30"</code></li>
            </ul>
            <strong>Returns:</strong><br>
            <ul>
                <li><strong>table</strong> - A table of key-value pairs:</li>
                <ul>
                    <li><code>year</code> - <strong>integer</strong> - The current year</li>
                    <li><code>month</code> - <strong>integer</strong> - The current month</li>
                    <li><code>day</code> - <strong>integer</strong> - The current day</li>
                    <li><code>yearday</code> - <strong>string</strong> - The current day of the year</li>
                    <li><code>weekday</code> - <strong>string</strong> - The current weekday since Sunday</li>
                    <li><code>hour</code> - <strong>integer</strong> - The current hour</li>
                    <li><code>minute</code> - <strong>integer</strong> - The current minute</li>
                    <li><code>second</code> - <strong>integer</strong> - The current second</li>
                </ul>
            </ul>
        </td>
    </tr>
</table>

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
