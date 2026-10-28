---
title: Lua reference
parent: "S2 & Superstack"
description: Lua library reference for Superstack IoT devices including the S2 Module
image: /assets/images/superstack-annotated-masthead.png
nav_order: 2
---

# Superstack Lua reference
{: .no_toc }

---

Superstack devices such as the S2 Module run Lua. You upload your code with the [Superstack CLI](/pages/superstack/cli), and the device runs it. This reference lists every function your code can call to read sensors, drive IO, make web requests and receive messages from your application.

Each function runs C code in the firmware. Lua can't reach the parts of the firmware that check in with Superstack and install updates, so no code you upload can stop the device from receiving new code.

Complete, ready-to-run code is in the example repository. If you write code with an AI agent, the Superstack plugin for Claude Code and Codex teaches it this reference.

[Example code](https://github.com/siliconwitchery/s2-lua-examples){: .btn .btn-purple}
[Agent plugin](https://github.com/siliconwitchery/superstack-agent-plugins){: .btn}

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Coding principles and notation

The functions described in this reference typically represent single, atomic operations. For example `device.digital.set_output()` will output a high, or low voltage on a specified pin. Unlike most hardware level programming, a separate configuration step isn't needed. All configuration is optional and is passed directly into this function if desired.

The functions may accept a combination of **positional** and **named** arguments. Positional arguments always come first, with the named arguments provided at the end as a Lua table of key-value pairs.

Most of the named arguments will take on a default value if not provided. These are marked as _optional_.

```lua
-- Calling a function with only positional arguments
device.digital.set_output("A0", true)

-- Calling a function with both positional and named arguments
device.i2c.write(0x12, "\x4F\x01", { scl_pin="B0", sda_pin="B1" })

-- Calling a function with only named arguments. Note how the () can be omitted
location.enable{ accuracy="LOW" }
```

Event handlers, such as those assigned with `device.digital.assign_input_event()`, run only while the code is running. Code that reaches the end of `main.lua` ends, and its handlers stop. To keep handling events, end `main.lua` with a loop:

```lua
while true do
    device.sleep(1)
end
```

An error that the code doesn't catch with `pcall` ends the code. The log shows `Code crashed:` followed by the error, and the code's run state becomes crashed. An error inside a handler or a request callback ends the code the same way. Handlers and callbacks can't call `coroutine.yield()`, and doing so raises an error. To run the code again, upload it or run `superstack device start <imei>`.

If the code makes the S2 restart, the S2 doesn't run it again after the restart. The log shows `Code crashed the device, so it was not started again`.

---

## Standard libraries

The device runs **Lua 5.5**. Most of the standard Lua libraries that you would find on the desktop installation of Lua are included:

- ✅ [Basic functions](https://www.lua.org/manual/5.5/manual.html#6.1)
- ✅ [Math functions](https://www.lua.org/manual/5.5/manual.html#6.7)
- ✅ [String manipulation](https://www.lua.org/manual/5.5/manual.html#6.4)
- ✅ [Table manipulation](https://www.lua.org/manual/5.5/manual.html#6.6)
- ✅ [UTF-8 support](https://www.lua.org/manual/5.5/manual.html#6.5)
- ✅ [Coroutine manipulation](https://www.lua.org/manual/5.5/manual.html#6.2)

The remaining standard libraries are not included, as they are superseded by similar functionality provided by the device specific libraries:

- ❎ File IO functions - Replaced by the [temporary files](#temporary-files) library
- ❎ Operating system functions - Replaced by the [timekeeping](#timekeeping) and [device information](#device-information) libraries
- ❎ Debug library
- ❎ Package library - `require` loads [code files](#code-files) without it

Three basic functions differ from desktop Lua:

- `require` loads another code file. See [code files](#code-files)
- `load` accepts only text, not precompiled bytecode
- `dofile` and `loadfile` cannot open files. Use `require` instead

---

## Hardware libraries

### Digital IO

#### Set or clear a digital output on a pin
{: .no_toc}

```lua
device.digital.set_output(pin, value)
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `value` - **boolean** - The level to set. `true` for high, `false` for low

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> Setting an output on a pin removes any input event handler assigned to the pin.

{: .note-title }

> Example
>
> ```lua
> -- Set pin B1 to a high value
> device.digital.set_output("B1", true)
> ```

---

#### Get the digital value on a pin
{: .no_toc}

```lua
device.digital.get_input(pin, { pull="PULL_DOWN" })
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. E.g. `"A0"`

{: .note-title }

> Optional parameters
>
> - `pull` - **string** - The pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **boolean** - `true` if the pin is high, `false` if low

{: .note }

> Reading a pin removes any input event handler assigned to the pin.

{: .note-title }

> Example
>
> ```lua
> -- Print the value on pin D0
> local val = device.digital.get_input("D0")
> print(val)
> ```

---

#### Assign an event handler for a pin input change
{: .no_toc}

```lua
device.digital.assign_input_event(pin, handler, { pull="PULL_DOWN" })
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `handler` - **function** - The function to call when the pin value changes. Called with two arguments:
>     - `pin` - **string** - The pin name that generated the event. E.g. `"A0"`
>     - `state` - **boolean** - The pin value when the event occurred. `true` if high, `false` if low

{: .note-title }

> Optional parameters
>
> - `pull` - **string** - The pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Assign a function that triggers when the input value of C3 changes
> function my_pin_handler(pin, state)
>     if state == true then
>         print(pin.." went high")
>     else
>         print(pin.." went low")
>     end
> end
>
> device.digital.assign_input_event("C3", my_pin_handler)
> ```

---

#### Disable an input event handler on a pin
{: .no_toc}

```lua
device.digital.unassign_input_event(pin)
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. E.g. `"A0"`

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Disable the event and detach the pin from the handler
> device.digital.unassign_input_event("C3")
> ```

---

### PWM output

#### Output a PWM signal on a pin
{: .no_toc}

```lua
device.pwm.set_output(pin, duty_cycle, { frequency=1000 })
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `duty_cycle` - **number** - The percentage of each period that the pin is high. From `0` to `100`

{: .note-title }

> Optional parameters
>
> - `frequency` - **number** - The PWM frequency in Hz. From `4` to `5000000`

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> Up to four pins can output PWM at once. Starting PWM on a fifth pin stops it on the pin that started first. Any other function that uses the pin, such as `device.digital.set_output()`, also stops it.

{: .note-title }

> Example
>
> ```lua
> -- Dim an LED on pin A0 to 25% brightness
> device.pwm.set_output("A0", 25, { frequency=2000 })
> ```

---

### Analog input

#### Read the analog value on a pin
{: .no_toc}

```lua
device.analog.get_input(pin, { acquisition_time=10 })
```

{: .note-title }

> Parameters
>
> - `pin` - **string** - The pin name. Must be an analog capable pin: `"C2"` to `"C4"`, or `"D0"` to `"D4"`

{: .note-title }

> Optional parameters
>
> - `acquisition_time` - **integer** - The measurement time in microseconds. Can be `3`, `5`, `10`, `15`, `20`, or `40`. Higher values support greater source resistances (10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ, 800kΩ respectively)

{: .note-title }

> Returns
>
> - **number** - The voltage present on the pin in volts

{: .note-title }

> Example
>
> ```lua
> -- Read the analog voltage on pin D0
> local voltage = device.analog.get_input("D0")
> print(voltage)
> ```

---

#### Read the differential analog value across two pins
{: .no_toc}

```lua
device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=10 })
```

{: .note-title }

> Parameters
>
> - `positive_pin` - **string** - The pin name of the positive pin. Must be an analog capable pin. E.g. `"D0"`
> - `negative_pin` - **string** - The pin name of the negative pin. Must be an analog capable pin, and different from `positive_pin`. E.g. `"D1"`

{: .note-title }

> Optional parameters
>
> - `acquisition_time` - **integer** - The measurement time in microseconds. Can be `3`, `5`, `10`, `15`, `20`, or `40`. Higher values support greater source resistances (10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ, 800kΩ respectively)

{: .note-title }

> Returns
>
> - **number** - The voltage across the pins in volts. Negative when `negative_pin` is at the higher voltage

{: .note-title }

> Example
>
> ```lua
> -- Read the differential analog voltage across pins D0 and D1
> local voltage = device.analog.get_differential_input("D0", "D1")
> print(voltage)
> ```

---

### I2C communication

{: .note }

> A single I2C transaction may read or write at most **8191 bytes**. A transaction fails, and returns `success=false`, if the device does not acknowledge or does not finish within 2 seconds.

#### Read bytes from an I2C device
{: .no_toc}

```lua
device.i2c.read(address, length, { port="PORTA", scl_pin="A1", sda_pin="A0", frequency=100 })
```

{: .note-title }

> Parameters
>
> - `address` - **integer** - The 7-bit address of the I2C device
> - `length` - **integer** - The number of bytes to read

{: .note-title }

> Optional parameters
>
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`. Assumes [Stemma QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma)/[Qwiic](https://www.sparkfun.com/qwiic) pinout. For a different pin order, use `scl_pin` and `sda_pin` instead
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`. Must be used with `sda_pin`. Cannot be used with `port`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`. Must be used with `scl_pin`. Cannot be used with `port`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title }

> Returns
>
> - **table** - A table of key-value pairs:
>     - `success` - **boolean** - `true` if the transaction was successful, `false` otherwise
>     - `data` - **string** - The bytes read. Always of size `length`. Absent if `success` is `false`
>     - `value` - **integer** - The first byte read, useful if only one byte was requested. Absent if `success` is `false` or `length` is `0`

{: .note-title }

> Example
>
> ```lua
> -- Read multiple bytes from the device and print the fourth byte
> local result = device.i2c.read(0x23, 4)
>
> if result.success then
>     print(string.byte(result.data, 4))
> end
> ```

---

#### Write bytes to an I2C device
{: .no_toc}

```lua
device.i2c.write(address, data, { port="PORTA", scl_pin="A1", sda_pin="A0", frequency=100 })
```

{: .note-title }

> Parameters
>
> - `address` - **integer** - The 7-bit address of the I2C device
> - `data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`

{: .note-title }

> Optional parameters
>
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title }

> Returns
>
> - **table** - A table of key-value pairs:
>     - `success` - **boolean** - `true` if the transaction was successful, `false` otherwise

{: .note-title }

> Example
>
> ```lua
> -- Write 0x1234 to the register 0xF9
> device.i2c.write(0x23, "\xF9\x12\x34")
> ```

---

#### Write then read bytes from an I2C device
{: .no_toc}

```lua
device.i2c.write_read(address, write_data, read_length, { port="PORTA", scl_pin="A1", sda_pin="A0", frequency=100 })
```

{: .note-title }

> Parameters
>
> - `address` - **integer** - The 7-bit address of the I2C device
> - `write_data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`
> - `read_length` - **integer** - The number of bytes to read

{: .note-title }

> Optional parameters
>
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title }

> Returns
>
> - **table** - A table of key-value pairs:
>     - `success` - **boolean** - `true` if both the write and the read were successful, `false` otherwise
>     - `data` - **string** - The bytes read. Always of size `read_length`. Absent if `success` is `false`
>     - `value` - **integer** - The first byte read, useful if only one byte was requested. Absent if `success` is `false` or `read_length` is `0`

{: .note-title }

> Example
>
> ```lua
> -- Read a byte from register 0x1F on a device with address 0x23
> local result = device.i2c.write_read(0x23, "\x1F", 1)
>
> if result.success then
>     print(result.value)
> end
> ```

---

#### Scan for I2C devices
{: .no_toc}

```lua
device.i2c.scan({ port="PORTA", scl_pin="A1", sda_pin="A0", frequency=100 })
```

{: .note-title }

> Optional parameters
>
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title }

> Returns
>
> - **nil** - The scan logs `Scanning for I2C devices`, then `Device found: 0x23` for each device it finds, then `I2C scan complete`

{: .note-title }

> Example
>
> ```lua
> -- Log the address of every device on PORTF
> device.i2c.scan({ port="PORTF" })
> ```

---

### SPI communication

{: .note }

> The pin options `sclk_pin`, `mosi_pin`, `miso_pin` and `cs_pin` must all be specified together. Providing only some of them raises an error. A single transfer may read or write at most **8191 bytes**.

#### Write then read bytes from an SPI device
{: .no_toc}

```lua
device.spi.write_read(write_data, read_length, { sclk_pin="C0", mosi_pin="C1", miso_pin="C2", cs_pin="C3", mode=0, frequency=4000, bit_order="MSB_FIRST", hold_cs=false, cs_active_high=false, miso_pull="NO_PULL" })
```

{: .note-title }

> Parameters
>
> - `write_data` - **string** - The data to write to the device
> - `read_length` - **integer** - The number of bytes to read from the device

{: .note-title }

> Optional parameters
>
> - `sclk_pin` - **string** - The pin name for the SCK signal. E.g. `"D0"`
> - `mosi_pin` - **string** - The pin name for the MOSI signal. E.g. `"D1"`
> - `miso_pin` - **string** - The pin name for the MISO signal. E.g. `"D2"`
> - `cs_pin` - **string** - The pin name for the CS signal. E.g. `"D3"`
> - `mode` - **integer** - The SPI mode. Can be `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The SPI frequency in kHz. Can be `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for transactions. Can be `"MSB_FIRST"` or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If `true`, the CS pin remains held after the transaction completes. Useful for multi-step transactions
> - `cs_active_high` - **boolean** - If `true`, the CS pin is set high during the transaction and low once completed
> - `miso_pull` - **string** - The pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **string** - The bytes read. Always of size `read_length`

{: .note-title }

> Example
>
> ```lua
> -- Read data from an SPI flash device
> local data = device.spi.write_read("\x03\x00\x00\x00", 11)
> print(data)
> ```

---

#### Write bytes to an SPI device
{: .no_toc}

```lua
device.spi.write(data, { sclk_pin="C0", mosi_pin="C1", miso_pin="C2", cs_pin="C3", mode=0, frequency=4000, bit_order="MSB_FIRST", hold_cs=false, cs_active_high=false, miso_pull="NO_PULL" })
```

{: .note-title }

> Parameters
>
> - `data` - **string** - The data to write to the device

{: .note-title }

> Optional parameters
>
> - `sclk_pin` - **string** - The pin name for the SCK signal. E.g. `"D0"`
> - `mosi_pin` - **string** - The pin name for the MOSI signal. E.g. `"D1"`
> - `miso_pin` - **string** - The pin name for the MISO signal. E.g. `"D2"`
> - `cs_pin` - **string** - The pin name for the CS signal. E.g. `"D3"`
> - `mode` - **integer** - The SPI mode. Can be `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The SPI frequency in kHz. Can be `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for transactions. Can be `"MSB_FIRST"` or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If `true`, the CS pin remains held after the transaction completes
> - `cs_active_high` - **boolean** - If `true`, the CS pin is set high during the transaction and low once completed
> - `miso_pull` - **string** - The pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Wake up the flash with the 0xAB command
> device.spi.write("\xAB")
> ```

---

#### Read bytes from an SPI device
{: .no_toc}

```lua
device.spi.read(length, { sclk_pin="C0", mosi_pin="C1", miso_pin="C2", cs_pin="C3", mode=0, frequency=4000, bit_order="MSB_FIRST", hold_cs=false, cs_active_high=false, miso_pull="NO_PULL" })
```

{: .note-title }

> Parameters
>
> - `length` - **integer** - The number of bytes to read from the device

{: .note-title }

> Optional parameters
>
> - `sclk_pin` - **string** - The pin name for the SCK signal. E.g. `"D0"`
> - `mosi_pin` - **string** - The pin name for the MOSI signal. E.g. `"D1"`
> - `miso_pin` - **string** - The pin name for the MISO signal. E.g. `"D2"`
> - `cs_pin` - **string** - The pin name for the CS signal. E.g. `"D3"`
> - `mode` - **integer** - The SPI mode. Can be `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The SPI frequency in kHz. Can be `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for transactions. Can be `"MSB_FIRST"` or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If `true`, the CS pin remains held after the transaction completes
> - `cs_active_high` - **boolean** - If `true`, the CS pin is set high during the transaction and low once completed
> - `miso_pull` - **string** - The pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **string** - The bytes read. Always of size `length`

{: .note-title }

> Example
>
> ```lua
> -- Read 4 bytes from an SPI device
> local data = device.spi.read(4)
> print(data)
> ```

---

#### Transact bytes with an SPI device (write and read in parallel)
{: .no_toc}

```lua
device.spi.transact(write_data, read_length, { sclk_pin="C0", mosi_pin="C1", miso_pin="C2", cs_pin="C3", mode=0, frequency=4000, bit_order="MSB_FIRST", hold_cs=false, cs_active_high=false, miso_pull="NO_PULL" })
```

{: .note-title }

> Parameters
>
> - `write_data` - **string** - The data to write to the device
> - `read_length` - **integer** - The number of bytes to read from the device

{: .note-title }

> Optional parameters
>
> - `sclk_pin` - **string** - The pin name for the SCK signal. E.g. `"D0"`
> - `mosi_pin` - **string** - The pin name for the MOSI signal. E.g. `"D1"`
> - `miso_pin` - **string** - The pin name for the MISO signal. E.g. `"D2"`
> - `cs_pin` - **string** - The pin name for the CS signal. E.g. `"D3"`
> - `mode` - **integer** - The SPI mode. Can be `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The SPI frequency in kHz. Can be `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for transactions. Can be `"MSB_FIRST"` or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If `true`, the CS pin remains held after the transaction completes
> - `cs_active_high` - **boolean** - If `true`, the CS pin is set high during the transaction and low once completed
> - `miso_pull` - **string** - The pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title }

> Returns
>
> - **string** - The bytes read. Always of size `read_length` as specified in the function call

{: .note-title }

> Example
>
> ```lua
> -- Write and read data simultaneously
> local data = device.spi.transact("\x9F", 3)
> print(data)
> ```

---

### UART communication

#### Write UART data
{: .no_toc}

```lua
device.uart.write(data, { tx_pin="A1", baudrate=9600, parity=false, stop_bits=1 })
```

{: .note-title }

> Parameters
>
> - `data` - **string** - The data to send

{: .note-title }

> Optional parameters
>
> - `tx_pin` - **string** - The pin name for the transmit signal. E.g. `"C1"`
> - `baudrate` - **integer** - The baudrate in bits-per-second. Can be `1200`, `2400`, `4800`, `9600`, `14400`, `19200`, `28800`, `31250`, `38400`, `56000`, `57600`, `76800`, `115200`, `230400`, `250000`, `460800`, `921600`, or `1000000`
> - `parity` - **boolean** - If `true`, enables the parity bit
> - `stop_bits` - **integer** - The number of stop bits. Can be `1` or `2`

{: .note-title }

> Returns
>
> - **nil** - Returns once all the data is sent

{: .note-title }

> Example
>
> ```lua
> -- Send UART data
> device.uart.write("Hello there. This is some data\n", { baudrate=19200 })
> ```

---

#### Assign an event handler for UART data
{: .no_toc}

```lua
device.uart.assign_read_event(terminator, handler, { rx_pin="A0", baudrate=9600, parity=false, stop_bits=1 })
```

{: .note-title }

> Parameters
>
> - `terminator` - **string** - The character to wait for before calling `handler`. E.g. `"\n"`. A string that isn't exactly one character raises an error. If `nil`, `handler` is called with whatever data has arrived
> - `handler` - **function** - The function to call when data is received. Called with one argument:
>     - `data` - **string** - The bytes received since the last call, including the terminator

{: .note-title }

> Optional parameters
>
> - `rx_pin` - **string** - The pin name for the receive signal. E.g. `"C0"`
> - `baudrate` - **integer** - The baudrate in bits-per-second. Takes the same values as `device.uart.write()`
> - `parity` - **boolean** - If `true`, enables the parity bit
> - `stop_bits` - **integer** - The number of stop bits. Can be `1` or `2`

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> Only one UART read event can be assigned at a time. Assigning another replaces it. If 512 bytes arrive without a terminator, `handler` is called with them anyway. If more than 2048 bytes arrive before the code handles them, they are dropped.

{: .note-title }

> Example
>
> ```lua
> -- Log each line received
> device.uart.assign_read_event("\n", function(line)
>     print("Got a new line: " .. line)
> end, { baudrate=19200 })
> ```

---

#### Disable the UART read event handler
{: .no_toc}

```lua
device.uart.unassign_read_event()
```

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Stop receiving UART data
> device.uart.unassign_read_event()
> ```

---

## Networking libraries

### Networking (LTE)

#### Send a GET or DELETE request to a web service
{: .no_toc}

```lua
network.get(url, { headers=nil, callback=nil })
network.delete(url, { headers=nil, callback=nil })
```

{: .note-title }

> Parameters
>
> - `url` - **string** - The full address, starting with `https://` or `http://`, including any query string. E.g. `"https://example.com/api?city=Oslo"`. It must name a host, and any port must be a number. It can't contain control characters or invalid UTF-8, and outside the query a `%` must start an escape such as `%20`

{: .note-title }

> Optional parameters
>
> - `headers` - **table** - The request headers, as names mapped to values. E.g. `{ ["Authorization"]="Bearer abc" }`. A name can contain only letters, digits and ``!#$%&'*+-.^_`|~``. A value can't contain control characters other than tab, or invalid UTF-8
> - `callback` - **function** - If given, the call returns at once and this function is called when the request finishes. Called with the same `response` and `error` that the call would otherwise return

{: .note-title }

> Returns
>
> - `response` - **table** - A table of key-value pairs, or `nil` if `error` is set:
>     - `status` - **integer** - The HTTP status code. E.g. `200`
>     - `content` - **string** - The response body
> - `error` - **string** - `nil`, or the reason no response arrived:
>     - `"no network"` - The request did not reach Superstack, or Superstack did not accept it
>     - `"timeout"` - The web service did not answer in time, or its answer did not reach the device
>     - `"connection failed"` - Superstack could not connect to the web service
>     - `"too large"` - The response body was too long
>     - `"no credit"` - The fleet has no [credit](/pages/superstack/credit), so the device did not send the request
>
> With `callback`, the call returns only `error`, which is `nil`

{: .note }

> Superstack makes the request on the device's behalf. [Receive requests from a device](/pages/superstack/api#receive-requests-from-a-device) lists the limits the web service must meet, how Superstack follows redirects, and which responses reach Lua. Only one request can wait at a time, with or without `callback`, and making another raises an error.
>
> A `url` or `headers` that breaks a rule above raises an error that names the rule. The URL and headers fit in about 5000 bytes, and a longer request raises the error `url and headers are too long`.

{: .note-title }

> Example
>
> ```lua
> local response, err = network.get("https://example.com/api/weather?city=Oslo")
>
> if response then
>     print(response.status, response.content)
> else
>     print("Request failed: " .. err)
> end
> ```

---

#### Send a POST, PUT or PATCH request to a web service
{: .no_toc}

```lua
network.post(url, body, { headers=nil, callback=nil })
network.put(url, body, { headers=nil, callback=nil })
network.patch(url, body, { headers=nil, callback=nil })
```

{: .note-title }

> Parameters
>
> - `url` - **string** - The full address, with the same rules as [`network.get()`](#send-a-get-or-delete-request-to-a-web-service)
> - `body` - **string** - The request body, sent unchanged. At most 4096 bytes

{: .note-title }

> Optional parameters
>
> - `headers` - **table** - The request headers, with the same rules as [`network.get()`](#send-a-get-or-delete-request-to-a-web-service)
> - `callback` - **function** - Called with `response` and `error` when the request finishes

{: .note-title }

> Returns
>
> - `response` and `error` - The same as [`network.get()`](#send-a-get-or-delete-request-to-a-web-service)

{: .note }

> The URL and headers fit in about 980 bytes beside a 4096-byte body. A longer request raises the error `url and headers are too long`.

{: .note-title }

> Example
>
> ```lua
> -- Send a reading as JSON without waiting for the answer
> network.post("https://example.com/api/readings", json.encode{ temperature=21.5 }, {
>     headers={ ["Content-Type"]="application/json" },
>     callback=function(response, err)
>         print(err or response.status)
>     end,
> })
> ```

---

#### Assign an event handler for messages
{: .no_toc}

```lua
network.assign_message_event(handler)
```

{: .note-title }

> Parameters
>
> - `handler` - **function** - The function to call when a message arrives from your application through Superstack. Called with one argument:
>     - `content` - **string** - The message exactly as your application sent it

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> A message that arrives while no handler is assigned, or while the code is stopped, is discarded. [How a message reaches a device](/pages/superstack/api#how-a-message-reaches-a-device) describes when messages arrive and how many the device holds.

{: .note-title }

> Example
>
> ```lua
> -- Switch an output from a JSON message such as {"led":true}
> network.assign_message_event(function(content)
>     device.digital.set_output("B1", json.decode(content).led)
> end)
> ```

---

#### Disable the message event handler
{: .no_toc}

```lua
network.unassign_message_event()
```

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Stop handling messages. Later messages are discarded
> network.unassign_message_event()
> ```

---

#### Check if the network is connected
{: .no_toc}

```lua
network.connected()
```

{: .note-title }

> Returns
>
> - **boolean** - `true` if the LTE network is connected, `false` otherwise

{: .note-title }

> Example
>
> ```lua
> if network.connected() then
>     print("Network is up")
> end
> ```

---

#### Set low power mode
{: .no_toc}

```lua
network.low_power_mode(enabled)
```

{: .note-title }

> Parameters
>
> - `enabled` - **boolean** - `true` to enable PSM (Power Saving Mode), `false` to disable it

{: .note-title }

> Returns
>
> - **nil**

{: .warning }

> Enabling PSM introduces up to **15 minutes of latency** for code updates from Superstack. To return to real-time updates, call `network.low_power_mode(false)` and wait up to 15 minutes for the modem to re-register.
>
> PSM stays on after the code ends, crashes or is stopped, until code turns it off or the S2 restarts.

{: .note-title }

> Example
>
> ```lua
> -- Enable low power mode when the network is not needed
> network.low_power_mode(true)
> ```

---

### Location (GPS)

#### Enable GPS
{: .no_toc}

```lua
location.enable{ accuracy="HIGH", power_saving="OFF", tracking_interval=1 }
```

{: .note-title }

> Optional parameters
>
> The table itself is required. Pass `{}` to use every default
>
> - `accuracy` - **string** - The accuracy of the fix. `"LOW"` requires three satellites, `"HIGH"` requires four satellites
> - `power_saving` - **string** - The power saving level. Can be `"OFF"`, `"MEDIUM"`, or `"MAX"`. Higher power saving reduces accuracy and increases time to fix
> - `tracking_interval` - **integer** - The period to poll for new location updates. `1` for continuous 1-second updates, or a value between `10` and `65535` seconds for slower updates to save power

{: .note-title }

> Returns
>
> - **nil**

{: .warning }

> `location.enable()` automatically activates PSM to allow the modem to share hardware with the GPS. This introduces up to **15 minutes of latency** for code updates from Superstack. To return to real-time updates, call `location.disable()` followed by `network.low_power_mode(false)`, then wait up to 15 minutes.
>
> GPS and PSM stay on after the code ends, crashes or is stopped, until code turns them off or the S2 restarts.

{: .note-title }

> Example
>
> ```lua
> -- Start GPS with default settings
> location.enable{}
>
> -- Start GPS with low accuracy to save power
> location.enable{ accuracy="LOW", power_saving="MAX" }
> ```

---

#### Get the latest GPS data
{: .no_toc}

```lua
location.get_latest()
```

{: .note-title }

> Returns
>
> - **table** - A table of key-value pairs:
>     - `valid` - **boolean** - `true` if the latest fix is valid. If `false`, the location and speed values are from the last valid fix, or `0` before the first. GPS keeps running after the code ends, so a fix from an earlier run of the code counts until the device restarts
>     - `latitude` - **number** - The latitude in degrees
>     - `longitude` - **number** - The longitude in degrees
>     - `altitude` - **number** - The altitude in meters
>     - `accuracy` - **number** - The location accuracy in meters
>     - `speed` - **number** - The horizontal speed in meters per second
>     - `speed_accuracy` - **number** - The speed accuracy in meters per second
>     - `satellites` - **table** - A table of key-value pairs:
>         - `tracked` - **integer** - The number of satellites currently being tracked
>         - `in_fix` - **integer** - The number of satellites currently being used for measurement
>         - `unhealthy` - **integer** - The number of satellites that could not be used for measurement

{: .note-title }

> Example
>
> ```lua
> -- GPS must be enabled before getting a location fix
> location.enable{}
>
> -- Avoid network activity while waiting for a fix. It competes
> -- for the modem hardware and delays acquisition
> device.sleep(60)
>
> local fix = location.get_latest()
>
> if fix.valid then
>     print(string.format("%.5f, %.5f", fix.latitude, fix.longitude))
> else
>     print("No fix yet. Tracking " .. fix.satellites.tracked .. " satellites")
> end
> ```

---

#### Disable GPS
{: .no_toc}

```lua
location.disable()
```

{: .note-title }

> Returns
>
> - **nil**

{: .warning }

> Disabling GPS alone does **not** restore real-time code updates. PSM remains active until `network.low_power_mode(false)` is called. After calling it, wait up to 15 minutes for the modem to re-register before code updates arrive in real time.

{: .note-title }

> Example
>
> ```lua
> -- Stop GPS and restore real-time connectivity
> location.disable()
> network.low_power_mode(false)
> ```

---

## System libraries

### Logging

#### Post log to Superstack
{: .no_toc}

```lua
print(...)
```

{: .note-title }

> Parameters
>
> - `...` - **any** - One or more values to print. They are converted to strings and joined with tabs into one log

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Simple print
> print("hello world")
>
> -- Print several values in one log, separated by tabs
> print("count", 4 + 3)
>
> -- C printf style formatted prints
> print(string.format("pi = %.4f", math.pi))
> ```

{: .note }

> `print` never waits for the network. Logs wait on the device in a 2048-byte buffer until they are sent, and a log that does not fit is dropped. [When a fleet runs out of credit](/pages/superstack/credit#when-a-fleet-runs-out-of-credit), the device discards logs instead of sending them.

---

### Sleep

#### Sleep for a duration
{: .no_toc}

```lua
device.sleep(time)
```

{: .note-title }

> Parameters
>
> - `time` - **number** - The duration to sleep in seconds. E.g. `1.5`

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> Assigned event handlers continue to fire during sleep. See [assign an event handler](#assign-an-event-handler-for-a-pin-input-change).

{: .note-title }

> Example
>
> ```lua
> -- Sleep for 1.5 seconds
> device.sleep(1.5)
> ```

---

#### Sleep for a short duration
{: .no_toc}

```lua
device.sleep_ms(time)
```

{: .note-title }

> Parameters
>
> - `time` - **integer** - The duration to sleep in milliseconds. From `0` to `1000`

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> Event handlers do not fire during `device.sleep_ms()`, and stopping the code waits for it to return. Use `device.sleep()` for anything longer.

{: .note-title }

> Example
>
> ```lua
> -- Pulse pin B1 high for 5 milliseconds
> device.digital.set_output("B1", true)
> device.sleep_ms(5)
> device.digital.set_output("B1", false)
> ```

---

### Power

#### Configure the battery charger
{: .no_toc}

```lua
device.power.battery.set_charger_cv_cc(voltage, current)
```

{: .note-title }

> Parameters
>
> - `voltage` - **number** - The termination voltage. Can be `3.50`, `3.55`, `3.60`, `3.65`, `4.00`, `4.05`, `4.10`, `4.15`, `4.20`, `4.25`, `4.30`, `4.35`, `4.40`, or `4.45`
> - `current` - **integer** - The constant charge current in mA. Must be between `32` and `800` in steps of `2`

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> This setting reverts to the firmware default (**3.50V** termination, **32mA** charge current) at reboot. Configure the charger near the top of your code so that it is reapplied whenever the code restarts.

{: .note-title }

> Example
>
> ```lua
> -- Configure the battery charger for a 4.2V 200mAh rated Li-Po cell
> device.power.battery.set_charger_cv_cc(4.2, 200)
> ```

---

#### Get the battery voltage
{: .no_toc}

```lua
device.power.battery.get_voltage()
```

{: .note-title }

> Returns
>
> - **number** - The voltage of the cell in volts

{: .note-title }

> Example
>
> ```lua
> local voltage = device.power.battery.get_voltage()
> print("Battery voltage is "..tostring(voltage).."V")
> ```

---

#### Get the battery charging status
{: .no_toc}

```lua
device.power.battery.get_charging_status()
```

{: .note-title }

> Returns
>
> - **string** - The charging status: `"charging"`, `"charged"`, or `"discharging"` if a battery is connected, or `"external_power"` if no battery is installed or the battery has a fault

{: .note-title }

> Example
>
> ```lua
> local status = device.power.battery.get_charging_status()
>
> if status ~= "external_power" then
>     print("Battery is "..status)
> else
>     print("Battery not connected. On external power")
> end
> ```

---

#### Set the IO voltage for all ports
{: .no_toc}

```lua
device.power.set_vout(voltage)
```

{: .note-title }

> Parameters
>
> - `voltage` - **number** - The IO voltage of `PORTA` - `PORTF`. Can be between `1.8` and `3.3` in steps of `0.1`, or `0` to switch the port power outputs off entirely

{: .note-title }

> Returns
>
> - **nil**

{: .note }

> At boot, the port rails default to **1.8V**. If a connected sensor requires a higher IO voltage, call this function before communicating with it.

{: .note-title }

> Example
>
> ```lua
> -- Set the voltage of Vout to 3.3V
> device.power.set_vout(3.3)
> ```

---

### Code files

#### Run another code file
{: .no_toc}

```lua
require(name)
```

{: .note-title }

> Parameters
>
> - `name` - **string** - The path of a code file in the bundle, without `.lua`. E.g. `"sensors"` for `sensors.lua`, or `"lib/sensors"` for `lib/sensors.lua`

{: .note-title }

> Returns
>
> - **any** - The value the file returns

{: .note }

> Each call runs the file again, so call `require` once per file and keep the result. Files can require other files up to 8 levels deep.

{: .note-title }

> Example
>
> ```lua
> -- sensors.lua returns a table of functions
> local sensors = require("sensors")
> print(sensors.read_temperature())
> ```

---

### Temporary files

{: .note }

> A temporary file is created by `storage.open()` and reached only through the handle it returns. Closing the handle deletes the file, and every temporary file is deleted when the code starts, ends, crashes, stops or restarts. Temporary files share storage with the code files in the bundle. The storage is **96KB**, and the file system uses part of it.

#### Open a temporary file
{: .no_toc}

```lua
storage.open()
```

{: .note-title }

> Returns
>
> - **handle** - A new, empty temporary file. Call `write`, `append`, `read` and `close` on it using the `:` syntax

{: .note-title }

> Example
>
> ```lua
> -- Buffer readings in a temporary file while the network is down
> local readings = storage.open()
>
> while not network.connected() do
>     readings:append(device.power.battery.get_voltage() .. "\n")
>     device.sleep(60)
> end
>
> -- Send the buffered readings once the network returns
> network.post("https://example.com/api/readings", readings:read{ length=4096 })
> readings:close()
> ```

{: .note }

> Every method raises an error once the handle is closed. A handle dropped without closing is closed when the garbage collector reclaims it, so close a file as soon as it is no longer needed to free its space.

---

#### Write data to a temporary file
{: .no_toc}

```lua
handle:write(data)
```

{: .note-title }

> Parameters
>
> - `data` - **string** - The data to write. Replaces the whole content of the file

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Write data to the file, then replace it
> local file = storage.open()
> file:write("Hello world")
> file:write("Goodbye world")
>
> -- Prints "Goodbye world"
> print(file:read())
> ```

{: .note }

> If the data does not fit in the remaining space, the write raises an error and leaves the file unchanged.

---

#### Append data to a temporary file
{: .no_toc}

```lua
handle:append(data)
```

{: .note-title }

> Parameters
>
> - `data` - **string** - The data to append to the end of the file

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Append more data to the file
> file:append("\nThis is another line of text")
> file:append("\nAnd this is a final line of text")
> ```

{: .note }

> If the data does not fit in the remaining space, the append raises an error and leaves the file unchanged.

---

#### Read data from a temporary file
{: .no_toc}

```lua
handle:read{ line=1, length=nil, offset=0 }
```

{: .note-title }

> Optional parameters
>
> - `line` - **integer** - The line index to return. `1` is the first line, `2` the second, etc. Negative values index from the end: `-1` is the last line, `-2` the second to last, etc. Cannot be `0`, and cannot be combined with `length` or `offset`
> - `length` - **integer** - The number of bytes to read. Cannot be used with `line`. If longer than the file, a shorter result is returned
> - `offset` - **integer** - Read from this byte offset within the file. Requires `length`

{: .note-title }

> Returns
>
> - **string** - The contents read. A line is returned without its newline. `nil` if the line does not exist

{: .note-title }

> Example
>
> ```lua
> -- Read the first line of the file
> print(file:read())
>
> -- Print the last line from the file
> print(file:read{ line=-1 })
>
> -- Read 16 bytes starting from the 8th byte
> print(file:read{ length=16, offset=8 })
> ```

---

#### Close a temporary file
{: .no_toc}

```lua
handle:close()
```

{: .note-title }

> Returns
>
> - **nil**

{: .note-title }

> Example
>
> ```lua
> -- Close the file. This deletes it and frees its space
> file:close()
> ```

{: .note }

> Any use of the handle after closing raises an error. Use `pcall` if the code cannot guarantee the handle is still open.

---

### Timekeeping

#### Get the current Unix timestamp
{: .no_toc}

```lua
time.get_unix_time()
```

{: .note-title }

> Returns
>
> - **integer** - The current Unix timestamp (i.e the number of non-leap milliseconds that have elapsed since 00:00:00 UTC on 1 January 1970), or if the time is not yet known, returns the uptime of the device in milliseconds

{: .note-title }

> Example
>
> ```lua
> -- Repeat something for 30 seconds
> local t = time.get_unix_time()
>
> while t + 30000 > time.get_unix_time() do
>     print("waiting")
>     device.sleep(5)
> end
> ```
>
> Note: the returned value is in **milliseconds**, so 30 seconds is `30000`

---

#### Get the current time and date
{: .no_toc}

```lua
time.get_time_date({ unix_epoch=nil, timezone="+00:00" })
```

{: .note-title }

> Optional parameters
>
> - `unix_epoch` - **integer** - A Unix timestamp in milliseconds to convert, as returned by `time.get_unix_time()`. If `nil`, the current time is used, and an error is raised if the time is not yet known
> - `timezone` - **string** - The timezone offset, from `"-12:00"` to `"+14:00"`. E.g. `"+02:00"` or `"-07:30"`

{: .note-title }

> Returns
>
> - **table** - A table of key-value pairs:
>     - `year` - **integer** - The current year
>     - `month` - **integer** - The current month
>     - `day` - **integer** - The current day
>     - `yearday` - **integer** - The days since 1 January. `0` on 1 January
>     - `weekday` - **integer** - The days since Sunday. `0` on Sunday
>     - `hour` - **integer** - The current hour
>     - `minute` - **integer** - The current minute
>     - `second` - **integer** - The current second

{: .note-title }

> Example
>
> ```lua
> -- Print the current time and date
> local now = time.get_time_date()
>
> print(string.format("The current time is: %02d:%02d", now.hour, now.minute))
> print(string.format("The current date is: %d/%d/%d", now.year, now.month, now.day))
> ```

---

### Device information

#### Hardware version constant
{: .no_toc}

```lua
device.HARDWARE_VERSION
```

{: .note-title }

> Returns
>
> - **string** - Always `"s2-module"`

{: .note-title }

> Example
>
> ```lua
> print(device.HARDWARE_VERSION)
> ```

---

#### Firmware version constant
{: .no_toc}

```lua
device.FIRMWARE_VERSION
```

{: .note-title }

> Returns
>
> - **string** - A string representing the current firmware version. E.g. `"3.0.0"`

{: .note-title }

> Example
>
> ```lua
> print(device.FIRMWARE_VERSION)
> ```

---

### JSON

#### Encode a value as JSON
{: .no_toc}

```lua
json.encode(value)
```

{: .note-title }

> Parameters
>
> - `value` - **any** - A table, string, number, boolean or `json.null`. A table whose keys are all whole numbers from 1 up becomes an array, with `null` for each missing key. E.g. `{[1]=1, [3]=3}` becomes `[1,null,3]`. Any other table becomes an object. An empty table becomes `{}`

{: .note-title }

> Returns
>
> - **string** - The JSON text

{: .note }

> Tables can nest up to 16 levels deep. A value that JSON cannot hold, such as a function, raises an error.
>
> An array table whose highest key is above 10 and more than twice its number of keys, such as `{[20]=1}`, raises the error `excessively sparse array`.
>
> An integer is written exactly. Any other number is written to 14 significant digits. A `/` in a string is written as `\/`, so `"https://example.com"` becomes `"https:\/\/example.com"`, which any JSON parser reads back as the same string.

{: .note-title }

> Example
>
> ```lua
> -- Prints {"temperature":21.5,"readings":[1,2,3]}, with the keys in any order
> print(json.encode{ temperature=21.5, readings={1, 2, 3} })
> ```

---

#### Decode JSON text
{: .no_toc}

```lua
json.decode(text)
```

{: .note-title }

> Parameters
>
> - `text` - **string** - The JSON text

{: .note-title }

> Returns
>
> - **any** - The decoded value. Objects and arrays become tables, and `null` becomes `json.null`

{: .note }

> Text that is not valid JSON, or that nests more than 16 levels deep, raises an error. Use `pcall` to handle text that might be invalid.

{: .note-title }

> Example
>
> ```lua
> local ok, message = pcall(json.decode, '{"led":true,"level":null}')
>
> if ok and message.level == json.null then
>     print("No level given")
> end
> ```
