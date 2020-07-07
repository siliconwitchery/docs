---
layout: default
title: API Reference
nav_order: 1
parent: SuperStack
---

# API Contents
{: .no_toc }
1. TOC
{:toc}

## Things to know before using this API

These rules describe everything there is to know about about communicating with the SuperStack API.

- The SuperStack API interface uses the [JSON Schema](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON).

- **Commands** are top level instructions to work with **Objects**.

- **Objects** take the form:
```json
"some object": {
    "parameter 1": "some value",
    "parameter 2": "another value"
}
```

- **Objects** can contain parameters of the following data types:
```json
"some object": {
    "string": "Hello this is a string. It can be quite long",
    "integer": 42,
    "float": 3.14159,
    "exponent": 10e+100,
    "boolean": true,
    "null": null,
    "array": [1 ,"two" , 3.0],
    "nested object": {
        "more":"stuff"
    }
}
```

- **Objects** cannot be directly modified, they must be issued inside the relevant **Command** for the required operation. To read the `"device"` **Object**, the `"request"` **Command** must be used:
```json
{
    "request": ["device"]
}
```

- Some **Commands** may only take the **Object Name** in an array as shown above. But some may take the entire **Object** with **Parameters**:
```json
"init": {
    "sensor 1": {
        "chip": "BME280",
        "return": ["temperature","pressure"]
    }
}
```

- **Commands** will trigger a **Response** to be sent back from the device. These can be an array of **Object Names** denoting the current operation, or an **Object** itself with returnable parameters:
```json
"added": [
    "sensor 1",
    "sensor 2"
],
"network": {
    "connected": true,
    "address": "12-23-34-AB-BA-CD"
}
```

- Multiple **Commands** and **Objects** may be issued at the same time:
```json
"init": {
    "sensor 2": {
        "chip": "BME280",
        "return": ["temperature","pressure"]
    },
    "sensor 3": {
        "chip": "MPU6050",
        "return": ["Xaccel","Yaccel"]
    }
},
"remove": ["sensor 1"],
"request": ["device", "sensor 4", "sensor 5"]
}
```

- The internal SuperStack Database is limited in size. Care must be taken to keep **Object** and **Parameter** names short to save space, but understandable enough for convenience in development. It's recomended that un-needed Objects are removed with the `"remove"` command once no longer needed. The `"reset"` command can also be used to clear the databse of all user content if needed.

# API Reference
{: .no_toc }

## Adding Objects `"add":{...}`
{: .d-inline-block }
Command
{: .label .label-green }

Initialises **Objects** with the parameters given, fully removing any **Objects** of the same name if they already exist in the Database.

### Returns:
{: .no_toc }

- `"added": ["object name", ... ]` if the object didn't exist but was successfully added
- `"re-added": ["object name", ... ]` if the object existed and was successfully re-added
- `"no-space": ["object name", ... ]` if there isn't enough space in the database to store the object
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

### Example:
{: .no_toc }

1. Assume The SuperStack Database does **not** already contain an Object named `"sensor 1"`.

2. Issue an **Add Command**:
```json
"add":{
    "sensor 1":{
        "chip": "BME280",
        "return": ["temperature","pressure"],
        "change.morethan": 10.5 
    }
}
```

3. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
"sensor 1":{
    "chip": "BME280",
    "return": ["temperature","pressure"],
    "change.morethan": 10.5 
}
```

4. Issue another **Add Command**:
```json
"add":{
    "sensor 1":{
        "chip": "BME280",
        "return": ["humidity"],
        "period.sec": 30
    }
}
```

5. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
"sensor 1":{
    "chip": "BME280",
    "return": ["humidity"],
    "period.sec": 30
}
```

Note that the `"change.morethan"` parameter was removed. This is because the `"add"` Command always overwrites all entries in the Object.

## Appending Objects `"append":{...}`
{: .d-inline-block }
Command
{: .label .label-green }

Updates **Objects** with the parameters given, but keeps existing parameters unchanged.

### Returns:
{: .no_toc }

- `"appended": ["object name", ... ]` if the object existed and was successfully appended
- `"not-found": ["object name", ... ]` if the object was not found in the Database
- `"no-space": ["object name", ... ]` if there isn't enough space in the database to store the object
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

### Example:
{: .no_toc }

1. The SuperStack Database already contains an Object named `"sensor 1"`.
```json
{
    "sensor 1": {
        "chip": "BME280",
        "return": ["temperature","pressure"],
        "change.morethan": 10.5 
    }
}
```

2. Issue an **Append Command**:
```json
{
    "append": {
        "sensor 1": {
            "return": ["humidity"],
            "period.sec": 30
        }
    }
}
```

3. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
{
    "sensor 1": {
        "chip": "BME280",
        "return": ["humidity"],
        "change.morethan": 10.5,
        "period.sec": 30
    }
}
```

The `"period.sec"` parameter was added to the Object and the `"return"` parameter was appended. All other parameters remain unchanged.
Note that indavidual parameters are still fully overwritten. In this case `"return": ["temperature","pressure"]` → `"return": ["humidity"]`. It is not possible to append the content within a parameter. It must be fully overwritten.

## Removing Objects `"remove":[...]`
{: .d-inline-block }
Command
{: .label .label-green }

Removes **Objects** given in the array.

### Returns:
{: .no_toc }

- `"removed": ["object name", ... ]` if the object was successfully removed
- `"not-found": ["object name", ... ]` if the object was not found in the Database
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

### Example:
{: .no_toc }

1. The SuperStack Database already contains an Object named `"sensor 1"`.
```json
{
    "sensor 1": {
        "chip":"BME280",
        "return": ["temperature","pressure"]
    }
}
```

2. Issue aa **Remove Command**:
```json
{
    "remove": ["sensor 1"]
}
```

3. The SuperStack Database no longer contains the `"sensor 1"` Object.

## Requesting Objects `"request":[...]`
{: .d-inline-block }
Command
{: .label .label-green }



## Reseting the Device `"reset":{...}`
{: .d-inline-block }
Command
{: .label .label-green }


## Getting Device Info Object `"device":{...} `
{: .d-inline-block }
Object
{: .label .label-yellow }

The `device` Object is a persistant object with **read-only** Parameters containing device information.

### Returns:
{: .no_toc }

- `"device": {...}` device Object with **Parameters** shown below
- `"read-only": ["device"]` if the user attempts to **Remove** or **Append** the read only Parameters.

### Read Only Parameters:
{: .no_toc }

- `"model": string` - Model name of the device. Format: `"Silicon Witchery S1 Module"`
- `"fw-version": string` - Firmware version stamp of the device. Format: `"YYYYMMDD.HHMM"`

## Getting Network Info Object `"network":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }

The `network` Object is a persistant object with **read-only** Parameters containing network status.

### Returns:
{: .no_toc }

- `"network": {...}` network Object with **Parameters** shown below.
- `"read-only": ["network"]` if the user attempts to **Remove** or **Append** the read only Parameters.

### Read Only Parameters:
{: .no_toc }

- `"connected": bool` - Connected state of the device. `true` if connected.
- `"address": string` - Network 48bit MAC address of the device. Format: `"01-23-45-67-89-AB"`
- `"buffer-size": integer` - Maximum buffer size for single transfers.
- `"tx-pending: bool"` - Flag to indicate that a **Response** is pending. `true` if pending.

## Getting/Configuring Power `"power":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }

The `power` Object is a persistant object with both **writable** as well as **read-only** Parameters containing device power status and configuration.

### Returns:
{: .no_toc }

- `"power": {...}` power Object with **Parameters** shown below.
- `"read-only": ["power"]` if the user attempts to **Remove** or **Append** the read only Parameters.

### Read Only Parameters:
{: .no_toc }

- `"battery": string` - Battery charger state. Values: `"no-battery"`, `"discharging"`, `"charging"`, `"charged"`
- `"level": integer` - Battery level percentage. Values: `0` to `100`
- `"uptime": string` - Time device has been powered. Format in [ISO8601 Duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) `"P46DT12H30M5S"`

### Writable Parameters:
{: .no_toc }

- `"io1-v": float` - User configurable IO1 voltage (V). Value `0` to `5.0`. Default `1.8`
- `"io2-v": float` - User configurable IO2 voltage (V). Value `0` to `5.0`. Default `1.8`
- `"charge-v": float` - Battery charger constant voltage limit (V). Value `4.1` to `4.7`. Default `4.1`
- `"charge-i": float` - Battery charger constant current limit (mA). Value `5` to `250`. Default `5`
- `"charge-enable: bool"` - Enable or disable the battery charger. Default `false`

## Getting/Configuring the FPGA `"fpga":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }


## Getting/Configuring Security `"security":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }


## Sensors & Custom Objects `"_YOUR_SENSOR_":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }