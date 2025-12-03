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

Superstack Devices such as the S2 Module run Lua. An incredibly lightweight, efficient and simple to learn language.

The builtin Lua libraries provide Users complete hardware and network level functionality to **read sensors**, **report data**, **compute on-device algorithms** and take actions such as **driving IO** automatically.

The Lua engine is almost as performant as writing native C firmware as it's a lightweight wrapper around naive C functions built into the Superstack firmware.

Compared to writing firmware, the Superstack Lua engine allows for remote, and realtime development of IoT code without the need for compiler tools, hardware debuggers or physical access to the device. There's also no risk of bricking devices, as Lua runs in a container, and is always updatable and firewalled from sensitive internal functions such as network management.

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Coding principals and notation

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
> - `pin` - **string** - The pin name. E.g. `A0`
> - `value` - **boolean** - The level to set on the pin. `true` for high, or `false` for low

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
> - `pin` - **string** - The pin name. E.g. `A0`

{: .note-title }
> Optional parameters:
> - `pull` - **string** - Selects the pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **boolean** - `true` if the pin is high, or `false` if it's low

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
> - `pin` - **string** - The pin name. E.g. `A0`
> - `handler` - **function** - The function to call whenever the pin value changes. This function will be called with two arguments:
>   - `pin` - **string** - The pin name that generated the event. E.g. `A0`
>   - `state` - **boolean** - The value on the pin when the event occurred. `true` if the pin was high, or `false` if the pin was low

{: .note-title }
> Optional parameters:
> - `pull` - **string** - Selects the pull mode on the pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Assign a function that triggers whenever the input value of C3 changes
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
> - `pin` - **string** - The pin name. E.g. `A0`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Disable the event and detach the pin from the handler if no longer needed
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
> - `pin` - **string** - The pin name. E.g. `A0`

{: .note-title }
> Optional parameters:
> - `acquisition_time` - **integer** - A time in microseconds across which to make the measurement. Can be either `3`, `5`, `10`, `15`, `20`, or `40`. Higher values allow for accurate measurement of greater source resistances. Those maximum resistances being 10kΩ, 40kΩ, 100kΩ, 200kΩ, 400kΩ and 800kΩ respectively

{: .note-title } 
> Returns:
> - **number** - The voltage present on the pin

{: .note-title } 
> Example:
> ```lua
> -- Read the analog value on pin D1 and print both the percentage and voltage values
> local d0_val = device.analog.get_input("D1")
> print(d0_val.percentage)
> print(d0_val.voltage)
> ```

---

#### Read the differential analog value across two pins
{: .no_toc}

```lua
device.analog.get_differential_input(positive_pin, negative_pin, { acquisition_time=40 })
```

{: .note-title }
> Parameters:
> - `positive_pin` - **string** - The pin name of the positive pin
> - `negative_pin` - **string** - The pin name of the negative pin

{: .note-title }
> Optional parameters:
> - `acquisition_time` - **integer** - A time in microseconds across which to make the measurement. Can be either `3`, `5`, `10`, `15`, `20`, or `40`. Higher values allow for accurate measurement of greater source resistances

{: .note-title } 
> Returns:
> - **number** - The voltage present across the pins

{: .note-title } 
> Example:
> ```lua
> -- Read the differential analog value across pins A0 and A1
> local diff_val = device.analog.get_differential_input("A0", "A1")
> print(diff_val)
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
> - `pin` - **string** - The pin name. E.g. `A0`
> - `percentage` - **number** - The duty cycle to output on the pin as a percentage

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
> - `port` - **string** - The 4-pin port which the I2C device is connected to. I.e. `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`. Using this parameter will assume the SCL and SDA pin order to match the [Stemma QT](https://learn.adafruit.com/introducing-adafruit-stemma-qt/what-is-stemma) and [Qwiic](https://www.sparkfun.com/qwiic) pinout. If a different pin order is required, the `scl_pin` and `sda_pin` parameters should be provided instead
> - `scl_pin` - **string** - The pin name to use for the SCL signal. E.g `"C3"`. Must be used in conjunction with `sda_pin` and cannot be used if the `port` parameter is already specified
> - `sda_pin` - **string** - The pin name to use for the SDA signal. E.g `"C4"`. Must be used in conjunction with `scl_pin` and cannot be used if the `port` parameter is already specified
> - `frequency` - **integer** - The frequency to use for I2C communications in kHz. Can be either `100`, `250` or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **string** - `true` if the transaction was a success, or `false` otherwise
>   - `data` - **string** - The bytes read. Always of size `length` as specified in the function call
>   - `value` - **string** - The first data value, useful if only one byte was requested

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
> - `port` - **string** - The 4-pin port which the I2C device is connected to. I.e. `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name to use for the SCL signal. E.g `"C3"`
> - `sda_pin` - **string** - The pin name to use for the SDA signal. E.g `"C4"`
> - `frequency` - **integer** - The frequency to use for I2C communications in kHz. Can be either `100`, `250` or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **string** - `true` if the transaction was a success, or `false` otherwise

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
> - `port` - **string** - The 4-pin port which the I2C device is connected to. I.e. `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name to use for the SCL signal. E.g `"C3"`
> - `sda_pin` - **string** - The pin name to use for the SDA signal. E.g `"C4"`
> - `frequency` - **integer** - The frequency to use for I2C communications in kHz. Can be either `100`, `250` or `400`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `success` - **string** - `true` if the transaction was a success, or `false` otherwise
>   - `data` - **string** - The bytes read. Always of size `read_length` as specified in the function call
>   - `value` - **string** - The first data value, useful if only one byte was requested

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
> - `port` - **string** - The 4-pin port which the I2C device is connected to. I.e. `"PORTA"`, `"PORTB"`, `"PORTE"`, or `"PORTF"`
> - `scl_pin` - **string** - The pin name to use for the SCL signal. E.g `"C3"`
> - `sda_pin` - **string** - The pin name to use for the SDA signal. E.g `"C4"`
> - `frequency` - **integer** - The frequency to use for I2C communications in kHz. Can be either `100`, `250` or `400`

{: .note-title } 
> Returns:
> - **nil**

{: .note-title } 
> Example:
> ```lua
> -- Scan a port for devices
> device.i2c.scan({port="PORTF"})
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
> - `sclk_pin` - **string** - The pin name to use for the SCK signal. E.g `"D0"`
> - `mosi_pin` - **string** - The pin name to use for the MOSI signal. E.g `"D1"`
> - `miso_pin` - **string** - The pin name to use for the MISO signal. E.g `"D2"`
> - `cs_pin` - **string** - The pin name to use for the CS signal. E.g `"D3"`
> - `mode` - **integer** - The SPI mode. Can be either `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The frequency to use for SPI transactions in kHz. Can be either `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for the bytes transacted. Can be either `"MSB_FIRST"`, or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If set to `true`, the CS pin will continue to be held after the transaction is completed. This can be useful if the transaction needs to be broken up into multiple steps. Any subsequent call to `device.spi.transaction` with `hold_cs` set to false will then return the CS pin to the unselected value
> - `cs_active_high` - **boolean** - If set to `true`, the CS pin will be set to high during the transaction, and then low once completed
> - `miso_pull` - **string** - Selects the pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **string** - The bytes read. Always of size `read_length` as specified in the function call

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
> - `sclk_pin` - **string** - The pin name to use for the SCK signal. E.g `"D0"`
> - `mosi_pin` - **string** - The pin name to use for the MOSI signal. E.g `"D1"`
> - `miso_pin` - **string** - The pin name to use for the MISO signal. E.g `"D2"`
> - `cs_pin` - **string** - The pin name to use for the CS signal. E.g `"D3"`
> - `mode` - **integer** - The SPI mode. Can be either `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The frequency to use for SPI transactions in kHz. Can be either `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for the bytes transacted. Can be either `"MSB_FIRST"`, or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If set to `true`, the CS pin will continue to be held after the transaction is completed
> - `cs_active_high` - **boolean** - If set to `true`, the CS pin will be set to high during the transaction, and then low once completed
> - `miso_pull` - **string** - Selects the pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

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
> - `sclk_pin` - **string** - The pin name to use for the SCK signal. E.g `"D0"`
> - `mosi_pin` - **string** - The pin name to use for the MOSI signal. E.g `"D1"`
> - `miso_pin` - **string** - The pin name to use for the MISO signal. E.g `"D2"`
> - `cs_pin` - **string** - The pin name to use for the CS signal. E.g `"D3"`
> - `mode` - **integer** - The SPI mode. Can be either `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The frequency to use for SPI transactions in kHz. Can be either `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for the bytes transacted. Can be either `"MSB_FIRST"`, or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If set to `true`, the CS pin will continue to be held after the transaction is completed
> - `cs_active_high` - **boolean** - If set to `true`, the CS pin will be set to high during the transaction, and then low once completed
> - `miso_pull` - **string** - Selects the pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

{: .note-title } 
> Returns:
> - **string** - The bytes read. Always of size `length` as specified in the function call

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
> - `sclk_pin` - **string** - The pin name to use for the SCK signal. E.g `"D0"`
> - `mosi_pin` - **string** - The pin name to use for the MOSI signal. E.g `"D1"`
> - `miso_pin` - **string** - The pin name to use for the MISO signal. E.g `"D2"`
> - `cs_pin` - **string** - The pin name to use for the CS signal. E.g `"D3"`
> - `mode` - **integer** - The SPI mode. Can be either `0`, `1`, `2`, or `3`
> - `frequency` - **integer** - The frequency to use for SPI transactions in kHz. Can be either `125`, `250`, `500`, `1000`, `2000`, `4000`, or `8000`
> - `bit_order` - **string** - The bit order for the bytes transacted. Can be either `"MSB_FIRST"`, or `"LSB_FIRST"`
> - `hold_cs` - **boolean** - If set to `true`, the CS pin will continue to be held after the transaction is completed
> - `cs_active_high` - **boolean** - If set to `true`, the CS pin will be set to high during the transaction, and then low once completed
> - `miso_pull` - **string** - Selects the pull mode on the MISO pin. Can be `"PULL_UP"`, `"PULL_DOWN"`, or `"NO_PULL"`

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
> - `baudrate` - **integer** - The baudrate in bits-per-second at which to send the data. Can be `1200`, `2400`, `4800`, `9600`, `14400`, `19200`, `28800`, `31250`, `38400`, `56000`, `57600`, `76800`, `115200`, `230400`, `250000`, `460800`, `921600`, or `1000000`
> - `tx_pin` - **string** - The pin name to use for the transmit signal. E.g `"C1"`
> - `cts_pin` - **string** - The pin name to use for the clear-to-send signal. E.g `"C3"`. If `nil` is given, the signal isn't used
> - `parity` - **boolean** - Enables the parity bit if set to `true`
> - `stop_bits` - **integer** - Sets the number of stop bits. Can be either `1` or `2`

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
> - `terminator` - **string** - The character to wait for until triggering the event. If set to `nil`, the event is triggered for every new character received
> - `handler` - **function** - The function to call whenever data is received. This function will be called with one argument:
>   - `data` - **string** - All the buffered bytes since the last event was triggered, or the event was enabled

{: .note-title }
> Optional parameters:
> - `baudrate` - **integer** - The baudrate in bits-per-second at which to receive the data
> - `rx_pin` - **string** - The pin name to use for the receive signal. E.g `"C0"`
> - `rts_pin` - **string** - The pin name to use for the ready-to-send signal. E.g `"C2"`. If `nil` is given, the signal isn't used
> - `parity` - **boolean** - Enables the parity bit if set to `true`

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
> - `rx_pin` - **string** - The pin name of the receive signal. E.g `"C0"`

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
> - `length` - **float** - The length to record in seconds. The maximum allowable time will depend on the RAM currently used on the device. Using a lower `sample_rate` and `bit_depth` will allow for longer recordings but at reduced quality
> - `handler` - **function** - The function to call whenever data is ready to be processed. The function will be called with one argument:
>   - `data` - **string** - Audio data as 1-byte-per-sample in the case of `bit_depth=8`, or 2-bytes-per-sample in the case of `bit_depth=16`. The samples will be signed values. This function should not spend longer than `length` time to process the data and exit, otherwise the internal buffer will overflow and cause glitches in the final audio

{: .note-title }
> Optional parameters:
> - `data_pin` - **string** - The pin name to use for the data input. E.g `"F0"`
> - `clock_pin` - **string** - The pin name to use for the clock input. E.g `"F1"`
> - `sample_rate` - **integer** - The sample rate to record in samples per second. Can be either `8000` or `16000`
> - `bit_depth` - **integer** - The dynamic range of the samples recorded. Can be either `8` or `16`

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
> - `data_pin` - **string** - The pin name of the data input. E.g `"F0"`

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
> - `data` - **table** - A table representing any data as key-value pairs. Will be converted to an equivalent JSON once it reaches Superstack. It's recommended to name keys in a full and clear way as that will be how the AI tools of Superstack will infer the meaning of the data. E.g. `temperature_celsius = 43.5` will help the AI understand that `43.5` represents temperature in Celsius units

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
>     some_int = -42, 
>     some_float = 23.1,
>     some_string = "test",
>     some_array = {1, 2, 3, 4},
>     some_nested_thing = {
>         another_int = 54,
>         another_string = "test again"
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
> - `accuracy` - **string** - The accuracy of the reading to acquire. Can either be `"LOW"` where only three satellites are required to attain a fix, or `"HIGH"` where four satellites are required to attain a fix
> - `power_saving` - **string** - The level of power saving that the GPS aim to achieve. Can either be `"OFF"`, `"MEDIUM"`, `"MAX"`. A higher level of power saving will result in less accuracy and a slower time to attain a fix
> - `tracking_interval` - **integer** - The period to poll for new location updates. Can either be `1` for continuous 1-second updates, or a value in seconds between `10` and `65535` for slower updates which can save power

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
> - `line` - **integer** - The index of the line to return. `1` being the first line, `2` being the second line, etc. Likewise, the lines can also be indexed from the end of the file. `-1` returns the last line of the file, `-2` the second to last, etc. `length` and `offset` are ignored when `line` is specified
> - `length` - **integer** - The number of bytes to read from the file. Cannot be used with the `line` option. If `length` is longer than the data present in the file, then a shorter result will be returned
> - `offset` - **integer** - When `length` is specified, this option allows reading from some arbitrary offset from within the file

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
> - `unix_epoch` - **number** - A Unix timestamp that should be converted to a real time and date
> - `timezone` - **string** - The timezone to observe when returning the time and date. Can be given as a standard timezone offset such as `"+02:00"` or `"-07:30"`

{: .note-title } 
> Returns:
> - **table** - A table of key-value pairs:
>   - `year` - **integer** - The current year
>   - `month` - **integer** - The current month
>   - `day` - **integer** - The current day
>   - `yearday` - **string** - The current day of the year
>   - `weekday` - **string** - The current weekday since Sunday
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

### Sleep, power & system info

#### Sleep for a duration
{: .no_toc}

```lua
device.sleep(time)
```

{: .note-title }
> Parameters:
> - `time` - **number** - The time to sleep in seconds. E.g. `1.5`

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

#### Configure the battery charger
{: .no_toc}

```lua
device.power.battery.set_charger_cv_cc(voltage, current)
```

{: .note-title }
> Parameters:
> - `voltage` - **number** - The termination voltage of the cell. Can be either `3.50`, `3.55`, `3.60`, `3.65`, `4.00`, `4.05`, `4.10`, `4.15`, `4.20`, `4.25`, `4.30`, `4.35`, `4.40`, or `4.45`
> - `current` - **number** - The constant current to charge the cell at. Must be between `32` and `800` in steps of `2`

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
> - **string** - The current charging status. Either `charging`, `charged` or `discharging` if the battery is connected, or `external_power` if either no battery is installed, or the battery has a fault

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

#### Set the output voltage
{: .no_toc}

```lua
device.power.set_vout(voltage)
```

{: .note-title }
> Parameters:
> - `voltage` - **number** - The voltage to set. Can be between `1.8` and `3.3` in steps of `0.1`

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
