---
title: Lua Library Reference
parent: Superstack Platform
description: Lua scripting and library reference for Superstack IoT devices including the S2 Module
image: /assets/images/superstack-annotated-masthead.png
nav_order: 1
---

# Superstack Lua Library Reference
{: .no_toc }

---

Superstack devices such as the S2 Module run Lua—an incredibly lightweight, efficient and simple to learn language.

The built-in Lua libraries provide complete hardware and network level functionality to **read sensors**, **report data**, **compute on-device algorithms** and take actions such as **driving IO** automatically.

The Lua engine is almost as performant as writing native C firmware as it's a lightweight wrapper around native C functions built into the Superstack firmware.

Compared to writing firmware, the Superstack Lua engine allows for remote and realtime development of IoT code without the need for compiler tools, hardware debuggers or physical access to the device. There's also no risk of bricking devices as Lua runs in a container, and is always updatable and isolated from sensitive internal functions such as network management.

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Coding principles and notation

The functions described in this reference typically represent single, atomic operations. For example `device.digital.set_output()` will output a high, or low voltage on a specified pin. Unlike most hardware level programming, a separate configuration step isn't needed. All configuration is optional and is passed directly into this function if desired.

The functions may accept a combination of **positional** and **named** arguments. Positional arguments always come first, with the named arguments provided at the end as a Lua table of key-value pairs.

Most of the named arguments will take on a default value if not provided. These are marked as *optional*.

```lua
-- Calling a function with only positional arguments
device.digital.set_output("A0", true)

-- Calling a function with both positional and named arguments
device.i2c.write(0x12, 0x4F, "\x01", { scl_pin="B0", sda_pin="B1"})

-- Calling a function with only named arguments. Note how the () can be omitted
network.send_data{ sensor_value=31.5 }
```

---

## Standard libraries

Almost all of the standard Lua libraries that you would find on the desktop installation of Lua are included:

- ✅ [Basic functions](https://www.lua.org/manual/5.4/manual.html#6.1)
- ✅ [Math functions](https://www.lua.org/manual/5.4/manual.html#6.7)
- ✅ [String manipulation](https://www.lua.org/manual/5.4/manual.html#6.4)
- ✅ [Table manipulation](https://www.lua.org/manual/5.4/manual.html#6.6)
- ✅ [UTF-8 support](https://www.lua.org/manual/5.4/manual.html#6.5)
- ✅ [Coroutine manipulation](https://www.lua.org/manual/5.4/manual.html#6.2)
- ✅ [Debug library](https://www.lua.org/manual/5.4/manual.html#6.10)

Only two standard libraries are not included, as they are superseded by similar functionality provided by the device specific libraries:

- ❎ File IO functions - Replaced by the [non-volatile memory](#non-volatile-memory-file-system) library
- ❎ Operating system functions - Replaced by the [timekeeping ](#timekeeping-functions) and [Device](#miscellaneous-functions) libraries

---

## Hardware libraries

### Digital IO

#### Set or clear a digital output on a pin
{: .no_toc}

```lua
device.digital.set_output(pin, value)
```

{: .note-title }
> Parameters:
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `value` - **boolean** - The level to set. `true` for high, `false` for low

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
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
> Parameters:
> - `pin` - **string** - The pin name. E.g. `"A0"`

{: .note-title }
> Optional parameters:
> - `pull` - **string** - The pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **boolean** - `true` if the pin is high, `false` if low

{: .note-title } 
> Example:
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
> Parameters:
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `handler` - **function** - The function to call when the pin value changes. Called with two arguments:
>   - `pin` - **string** - The pin name that generated the event. E.g. `"A0"`
>   - `state` - **boolean** - The pin value when the event occurred. `true` if high, `false` if low

{: .note-title }
> Optional parameters:
> - `pull` - **string** - The pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
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
> Parameters:
> - `pin` - **string** - The pin name. E.g. `"A0"`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Disable the event and detach the pin from the handler
> device.digital.unassign_input_event("C3")
> ```

---

### Analog input

#### Read the analog value on a pin
{: .no_toc}

```lua
device.analog.get_input(pin, { acquisition_time=40 })
```

{: .note-title }
> Parameters:
> - `pin` - **string** - The pin name. Must be an analog capable pin. E.g. `"D0"`

{: .note-title }
> Optional parameters:
> - `acquisition_time` - **integer** - The measurement time in microseconds. Can be `3`, `5`, `10`, `15`, `20`, or `40`. Higher values support greater source resistances (10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ, 800kΩ respectively)

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `voltage` - **number** - The voltage present on the pin
>   - `percentage` - **number** - The voltage as a percentage of the full scale

{: .note-title } 
> Example:
> ```lua
> -- Read the analog value on pin D0 and print both the percentage and voltage values
> local val = device.analog.get_input("D0")
> print(val.percentage)
> print(val.voltage)
> ```

---

#### Read the differential analog value across two pins
{: .no_toc}

```lua
device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40 })
```

{: .note-title }
> Parameters:
> - `positive_pin` - **string** - The pin name of the positive pin. Must be an analog capable pin. E.g. "D0"
> - `negative_pin` - **string** - The pin name of the negative pin. Must be an analog capable pin. E.g. "D1"

{: .note-title }
> Optional parameters:
> - `acquisition_time` - **integer** - The measurement time in microseconds. Can be `3`, `5`, `10`, `15`, `20`, or `40`. Higher values support greater source resistances (10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ, 800kΩ respectively)

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `voltage` - **number** - The voltage present across the pins
>   - `percentage` - **number** - The voltage as a percentage of the full scale

{: .note-title } 
> Example:
> ```lua
> -- Read the differential analog value across pins D0 and D1
> local val = device.analog.get_differential_input("D0", "D1")
> print(val.voltage)
> ```

---

### PWM output (analog output)

#### Set a PWM duty cycle on a pin
{: .no_toc}

```lua
device.analog.set_output(pin, percentage, { frequency=1 })
```

{: .note-title }
> Parameters:
> - `pin` - **string** - The pin name. E.g. `"A0"`
> - `percentage` - **number** - The duty cycle as a percentage

{: .note-title }
> Optional parameters:
> - `frequency` - **number** - The PWM frequency in Hz

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Set pin E1 to a 25% duty cycle at the default PWM frequency
> device.analog.set_output("E1", 25)
> ```

---

### I2C communication

#### Read bytes from an I2C device
{: .no_toc}

```lua
device.i2c.read(address, length, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400 })
```

{: .note-title }
> Parameters:
> - `address` - **integer** - The 7-bit address of the I2C device
> - `length` - **integer** - The number of bytes to read

{: .note-title }
> Optional parameters:
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`. Assumes [Stemma QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma)/[Qwiic](https://www.sparkfun.com/qwiic) pinout. For a different pin order, use `scl_pin` and `sda_pin` instead
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`. Must be used with `sda_pin`. Cannot be used with `port`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`. Must be used with `scl_pin`. Cannot be used with `port`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **boolean** - `true` if the transaction was successful, `false` otherwise
>   - `data` - **string** - The bytes read. Always of size `length` as specified in the function call
>   - `value` - **integer** - The first data byte, useful if only one byte was requested

{: .note-title } 
> Example:
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
device.i2c.write(address, data, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400 })
```

{: .note-title }
> Parameters:
> - `address` - **integer** - The 7-bit address of the I2C device
> - `data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`

{: .note-title }
> Optional parameters:
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **boolean** - `true` if the transaction was successful, `false` otherwise

{: .note-title } 
> Example:
> ```lua
> -- Write 0x1234 to the register 0xF9
> device.i2c.write(0x23, "\xF9\x12\x34")
> ```

---

#### Write then read bytes from an I2C device
{: .no_toc}

```lua
device.i2c.write_read(address, write_data, read_length, { port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400 })
```

{: .note-title }
> Parameters:
> - `address` - **integer** - The 7-bit address of the I2C device
> - `write_data` - **string** - The data to write to the device. Can be a hexadecimal string containing zeros. E.g. `"\x1A\x50\x00\xF1"`
> - `read_length` - **integer** - The number of bytes to read

{: .note-title }
> Optional parameters:
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **boolean** - `true` if the transaction was successful, `false` otherwise
>   - `data` - **string** - The bytes read. Always of size `read_length` as specified in the function call
>   - `value` - **integer** - The first data byte, useful if only one byte was requested

{: .note-title } 
> Example:
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
device.i2c.scan({ port="PORTA", scl_pin="A0", sda_pin="A1", frequency=400 })
```

{: .note-title }
> Optional parameters:
> - `port` - **string** - The 4-pin port the I2C device is connected to. Can be `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name for the SCL signal. E.g. `"C3"`
> - `sda_pin` - **string** - The pin name for the SDA signal. E.g. `"C4"`
> - `frequency` - **integer** - The I2C frequency in kHz. Can be `100`, `250`, or `400`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Scan a port for devices
> device.i2c.scan({ port="PORTF" })
> ```

---

### SPI communication

#### Write then read bytes from an SPI device
{: .no_toc}

```lua
device.spi.write_read(write_data, read_length, { sclk_pin="C0", mosi_pin="C1", miso_pin="C2", cs_pin="C3", mode=0, frequency=4000, bit_order="MSB_FIRST", hold_cs=false, cs_active_high=false, miso_pull="NO_PULL" })
```

{: .note-title }
> Parameters:
> - `write_data` - **string** - The data to write to the device
> - `read_length` - **integer** - The number of bytes to read from the device

{: .note-title }
> Optional parameters:
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
> Returns:
> - **string** - The bytes read. Always of size `read_length`

{: .note-title } 
> Example:
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
> Parameters:
> - `data` - **string** - The data to write to the device

{: .note-title }
> Optional parameters:
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
> Returns:
> - **nil**

{: .note-title } 
> Example:
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
> Parameters:
> - `length` - **integer** - The number of bytes to read from the device

{: .note-title }
> Optional parameters:
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
> Returns:
> - **string** - The bytes read. Always of size `length`

{: .note-title } 
> Example:
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
> Parameters:
> - `write_data` - **string** - The data to write to the device
> - `read_length` - **integer** - The number of bytes to read from the device

{: .note-title }
> Optional parameters:
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
> Returns:
> - **string** - The bytes read. Always of size `read_length` as specified in the function call

{: .note-title } 
> Example:
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
device.uart.write(data, { baudrate=9600, tx_pin="B1", cts_pin=nil, parity=false, stop_bits=1 })
```

{: .note-title }
> Parameters:
> - `data` - **string** - The data to send

{: .note-title }
> Optional parameters:
> - `baudrate` - **integer** - The baudrate in bits-per-second. Can be `1200`, `2400`, `4800`, `9600`, `14400`, `19200`, `28800`, `31250`, `38400`, `56000`, `57600`, `76800`, `115200`, `230400`, `250000`, `460800`, `921600`, or `1000000`
> - `tx_pin` - **string** - The pin name for the transmit signal. E.g. `"C1"`
> - `cts_pin` - **string** - The pin name for the clear-to-send signal. E.g. `"C3"`. If `nil`, the signal isn't used
> - `parity` - **boolean** - If `true`, enables the parity bit
> - `stop_bits` - **integer** - The number of stop bits. Can be `1` or `2`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Send UART data
> device.uart.write("Hello there. This is some data\n", { baudrate=19200 })
> ```

---

#### Assign an event handler for UART data
{: .no_toc}

```lua
device.uart.assign_read_event(terminator, handler, { baudrate=9600, rx_pin="B0", tx_pin="B1", rts_pin=nil, cts_pin=nil, parity=false, stop_bits=1 })
```

{: .note-title }
> Parameters:
> - `terminator` - **string** - The character to wait for before triggering the event. If `nil`, the event triggers for every character received
> - `handler` - **function** - The function to call when data is received. Called with one argument:
>   - `data` - **string** - All buffered bytes since the last event or since the event was enabled

{: .note-title }
> Optional parameters:
> - `baudrate` - **integer** - The baudrate in bits-per-second
> - `rx_pin` - **string** - The pin name for the receive signal. E.g. `"C0"`
> - `rts_pin` - **string** - The pin name for the ready-to-send signal. E.g. `"C2"`. If `nil`, the signal isn't used
> - `parity` - **boolean** - If `true`, enables the parity bit

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Create a handler for receiving UART data
> function my_receive_handler(data)
>     print("Got a new line: "..data)
> end
> 
> device.uart.assign_read_event("\n", my_receive_handler, { baudrate=19200 })
> ```

---

#### Disable a UART read event handler
{: .no_toc}

```lua
device.uart.unassign_read_event(rx_pin)
```

{: .note-title }
> Parameters:
> - `rx_pin` - **string** - The pin name of the receive signal. E.g. `"C0"`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Disable the event and detach the pin from the handler if no longer needed
> device.uart.unassign_read_event("B0")
> ```

---

### PDM microphone input

#### Record audio from a PDM microphone
{: .no_toc}

```lua
device.audio.record(length, handler, { data_pin="E0", clock_pin="E1", sample_rate=8000, bit_depth=8 })
```

{: .note-title }
> Parameters:
> - `length` - **number** - The duration to record in seconds. The maximum allowable time depends on the RAM currently used on the device. Using a lower `sample_rate` and `bit_depth` allows for longer recordings at reduced quality
> - `handler` - **function** - The function to call when data is ready. Called with one argument:
>   - `data` - **string** - Audio data as 1-byte-per-sample for `bit_depth=8`, or 2-bytes-per-sample for `bit_depth=16`. Samples are signed values. This function must complete within `length` time to avoid buffer overflow

{: .note-title }
> Optional parameters:
> - `data_pin` - **string** - The pin name for the data input. E.g. `"F0"`
> - `clock_pin` - **string** - The pin name for the clock input. E.g. `"F1"`
> - `sample_rate` - **integer** - The sample rate in samples per second. Can be `8000` or `16000`
> - `bit_depth` - **integer** - The dynamic range of samples. Can be `8` or `16`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Create a handler for receiving and processing audio samples
> function my_microphone_handler(data)
>     for i = 1, #data do
>         local value = string.sub(data, i, i)
>         
>         if value > 128 or value < -128 then
>             print("Loud noise detected")
>         end
>     end
> end
> 
> -- Will capture 1s worth of audio at a time
> device.audio.record(1, my_microphone_handler)
> ```

---

#### Stop recording audio
{: .no_toc}

```lua
device.audio.stop(data_pin)
```

{: .note-title }
> Parameters:
> - `data_pin` - **string** - The pin name of the data input. E.g. `"F0"`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Recording can be stopped at any time
> device.audio.stop("E0")
> ```

---

## Networking libraries

### Networking (LTE)

#### Send data to Superstack
{: .no_toc}

```lua
network.send_data{ data }
```

{: .note-title }
> Parameters:
> - `data` - **table** - A table of key-value pairs. Converted to JSON when sent to Superstack. Use descriptive key names (e.g. `temperature_celsius = 43.5`) to help AI tools infer meaning

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- A simple sensor value
> my_sensor_value = 23.5
> 
> network.send_data{ temperature=my_sensor_value }
> 
> -- Network send can contain any arbitrary data
> network.send_data{ 
>     my_int = -42, 
>     my_float = 23.1,
>     my_string = "my string",
>     my_array = {1, 2, 3, 4},
>     my_table = {
>         my_other_int = 54,
>         my_other_string = "another string"
>     }
> }
> ```

---

### Location (GPS)

#### Get the latest GPS data
{: .no_toc}

```lua
location.get_latest()
```

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `valid` - **boolean** - `true` if the GPS data is valid, or `false` otherwise
>   - `latitude` - **number** - The current latitude
>   - `longitude` - **number** - The current longitude
>   - `altitude` - **number** - The current altitude
>   - `accuracy` - **number** - The location and altitude accuracy
>   - `speed` - **number** - The current speed
>   - `speed_accuracy` - **number** - The speed accuracy
>   - `satellites` - **table** - A table of key-value pairs:
>     - `tracked` - **integer** - The number of satellites currently being tracked
>     - `in_fix` - **integer** - The number of satellites currently being used for measurement
>     - `unhealthy` - **integer** - The number of satellites that could not be used for measurement

{: .note-title } 
> Example:
> ```lua
> local l = location.get_latest()
> 
> print("valid: " .. tostring(l["valid"]))
> print("latitude: " .. tostring(l["latitude"]))
> print("longitude: " .. tostring(l["longitude"]))
> print("altitude: " .. tostring(l["altitude"]))
> print("accuracy: " .. tostring(l["accuracy"]))
> print("speed: " .. tostring(l["speed"]))
> print("speed_accuracy: " .. tostring(l["speed_accuracy"]))
> 
> print("satellites tracked: " .. tostring(l["satellites"]["tracked"]))
> print("satellites in fix: " .. tostring(l["satellites"]["in_fix"]))
> print("satellites unhealthy: " .. tostring(l["satellites"]["unhealthy"]))
> ```

---

#### Set GPS options
{: .no_toc}

```lua
location.set_options({ accuracy="HIGH", power_saving="MEDIUM", tracking_interval=1 })
```

{: .note-title }
> Optional parameters:
> - `accuracy` - **string** - The accuracy of the fix. `"LOW"` requires three satellites, `"HIGH"` requires four satellites
> - `power_saving` - **string** - The power saving level. Can be `"OFF"`, `"MEDIUM"`, or `"MAX"`. Higher power saving reduces accuracy and increases time to fix
> - `tracking_interval` - **integer** - The period to poll for new location updates. `1` for continuous 1-second updates, or a value between `10` and `65535` seconds for slower updates to save power

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> location.set_options({ accuracy = "LOW" })
> ```

---

## System libraries

### Logging

#### Post log to Superstack
{: .no_toc}

```lua
print(log)
```

{: .note-title }
> Parameters:
> - `log` - **string** - String to print

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Simple print
> print("hello world")
>
> -- Print variables
> local my_num = 4 + 3
> print(my_num)
>
> -- C printf style formatted prints
> print(string.format("pi = %.4f", math.pi))
> ```

---

### Sleep

#### Sleep for a duration
{: .no_toc}

```lua
device.sleep(time)
```

{: .note-title }
> Parameters:
> - `time` - **number** - The duration to sleep in seconds. E.g. `1.5`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Sleep for 1.5 seconds
> device.sleep(1.5)
> ```

---

### Power

#### Configure the battery charger
{: .no_toc}

```lua
device.power.battery.set_charger_cv_cc(voltage, current)
```

{: .note-title }
> Parameters:
> - `voltage` - **number** - The termination voltage. Can be `3.50`, `3.55`, `3.60`, `3.65`, `4.00`, `4.05`, `4.10`, `4.15`, `4.20`, `4.25`, `4.30`, `4.35`, `4.40`, or `4.45`
> - `current` - **number** - The constant charge current in mA. Must be between `32` and `800` in steps of `2`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
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
> Returns:
> - **number** - The voltage of the cell in volts

{: .note-title } 
> Example:
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
> Returns:
> - **string** - The charging status: `"charging"`, `"charged"`, or `"discharging"` if a battery is connected, or `"external_power"` if no battery is installed or the battery has a fault

{: .note-title } 
> Example:
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
> Parameters:
> - `voltage` - **number** - The IO voltage of `PORTA` - `PORTF`. Can be between `1.8` and `3.3` in steps of `0.1`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Set the voltage of Vout to 3.3V
> device.power.set_vout(3.3)
> ```

---

### File storage

#### Write data to a file
{: .no_toc}

```lua
storage.write(filename, data)
```

{: .note-title }
> Parameters:
> - `filename` - **string** - The name of the file
> - `data` - **string** - The data to save to the file

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Create a file and write data to it
> storage.write("my_file.txt", "Hello world")
> ```

---

#### Append data to a file
{: .no_toc}

```lua
storage.append(filename, data)
```

{: .note-title }
> Parameters:
> - `filename` - **string** - The name of the file
> - `data` - **string** - The data to append to the file

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Append more data to the file
> storage.append("my_file.txt", "\nThis is another line of text")
> storage.append("my_file.txt", "\nAnd this is a final line of text")
> ```

---

#### Read data from a file
{: .no_toc}

```lua
storage.read(filename, { line=-1, length=nil, offset=0 })
```

{: .note-title }
> Parameters:
> - `filename` - **string** - The name of the file

{: .note-title }
> Optional parameters:
> - `line` - **integer** - The line index to return. `1` is the first line, `2` the second, etc. Negative values index from the end: `-1` is the last line, `-2` the second to last, etc. When specified, `length` and `offset` are ignored
> - `length` - **integer** - The number of bytes to read. Cannot be used with `line`. If longer than the file, a shorter result is returned
> - `offset` - **integer** - When `length` is specified, read from this byte offset within the file

{: .note-title } 
> Returns:
> - **string** - The contents read

{: .note-title } 
> Example:
> ```lua
> -- Read the entire file
> print(storage.read("my_file.txt"))
> 
> -- Print the last line from the file
> print(storage.read("my_file.txt", { line=-1 }))
> ```

---

#### Delete a file
{: .no_toc}

```lua
storage.delete(filename)
```

{: .note-title }
> Parameters:
> - `filename` - **string** - The name of the file

{: .note-title } 
> Returns:
> - **boolean** - `true` if the file was found and deleted, `false` otherwise

{: .note-title } 
> Example:
> ```lua
> -- Delete the file
> storage.delete("my_file.txt")
> ```

---

#### List all files
{: .no_toc}

```lua
storage.list()
```

{: .note-title } 
> Returns:
> - **table** - A table of tables:
>   - **table** - A table of key-value pairs:
>     - `name` - **string** - The name of the file
>     - `size` - **integer** - The size of the file in bytes

{: .note-title } 
> Example:
> ```lua
> -- List all files on the device
> local files = storage.list()
> for i, file in ipairs(files) do
>     print(file.name .. " - " .. file.size .. " bytes")
> end
> ```

---

### Timekeeping

#### Get the current Unix timestamp
{: .no_toc}

```lua
time.get_unix_time()
```

{: .note-title } 
> Returns:
> - **integer** - The current Unix timestamp (i.e the number of non-leap milliseconds that have elapsed since 00:00:00 UTC on 1 January 1970), or if the time is not yet known, returns the uptime of the device in milliseconds

{: .note-title } 
> Example:
> ```lua
> -- Repeat something for 30 seconds
> local t = time.get_unix_time()
> 
> while t + 30 > time.get_unix_time() do
>     print("waiting")
>     device.sleep(5)
> end
> ```

---

#### Get the current time and date
{: .no_toc}

```lua
time.get_time_date({ unix_epoch, timezone })
```

{: .note-title }
> Optional parameters:
> - `unix_epoch` - **number** - A Unix timestamp to convert to a time and date
> - `timezone` - **string** - The timezone offset. E.g. `"+02:00"` or `"-07:30"`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `year` - **integer** - The current year
>   - `month` - **integer** - The current month
>   - `day` - **integer** - The current day
>   - `yearday` - **integer** - The current day of the year
>   - `weekday` - **integer** - The current day of the week since Sunday
>   - `hour` - **integer** - The current hour
>   - `minute` - **integer** - The current minute
>   - `second` - **integer** - The current second

{: .note-title } 
> Example:
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
> Returns:
> - **string** - Always `"s2-module"`

{: .note-title } 
> Example:
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
> Returns:
> - **string** - A string representing the current firmware version. E.g. `"0.1.0+0"`

{: .note-title } 
> Example:
> ```lua
> print(device.FIRMWARE_VERSION)
> ```
