---
layout: default
title: API Reference
nav_order: 1
parent: SuperStack
---

## Commands, Objects, Parameters and Responses
{: .no_toc }

- The SuperStack API interface uses the [JSON Schema](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON).
- **Commands** are top level instructions to work with **Objects**.
- **Objects** take the form:
```json
"some object": {
    "parameter 1": "some value",
    "parameter 2": "another value"
}
```
- Objects can contain parameters of the following data types:
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
- **Objects** cannot be directly modified, they must be issued inside the relevant **Command** for the required operation. To read the `"device"` **Object**, the `"request"` **Command** must be used.
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
- **Commands** will trigger a **Response** to be sent back from the device. These can be an array of **Object Names** denoting the current operation, or an **Object** itself with returnable parameters.
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

## API Reference
{: .no_toc }
1. TOC
{:toc}

### Initialise Object `"init":{...}`
{: .d-inline-block }
Command
{: .label .label-green }

- Initialises an **Object** with new values, fully removing any **Objects** of the same name if they previously existed.
- Multiple **Objects** may be initialised at the same time
### Example:
{: .no_toc }

1. Assume The SuperStack Database does **not** already contain an Object named `"sensor 1"`.
2. Issue an **Initialise Command**:
```json
"init":{
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
4. Issue another **Initialise Command**:
```json
"init":{
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
Note that the `"change.morethan"` parameter was removed. This is because the Initialise Command always overwrites all entries in the Object.

### Append Objects `"append":{...}`
{: .d-inline-block }

Command
{: .label .label-green }

Updates an **Object** with the parameters given, but keeps existing parameters unchanged.

### Example:
{: .no_toc }

1. The SuperStack Database already contains an Object named `"sensor 1"`.
```json
{
    "sensor 1":{
        "chip":"BME280",
        "return": ["temperature","pressure"],
        "change.morethan": 10.5 
    }
}
```
2. Issue an **Append Command**:
```json
{
    "append":{
        "sensor 1":{
            "return": ["humidity"],
            "period.sec": 30
        }
    }
}
```
3. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
{
    "sensor 1":{
        "chip":"BME280",
        "return": ["humidity"],
        "change.morethan": 10.5,
        "period.sec": 30
    }
}
```
The `"period.sec"` parameter was added to the Object and the `"return"` parameter was appended. All other parameters remain unchanged.
Note that indavidual parameters are still fully overwritten. In this case `"return": ["temperature","pressure"]` → `"return": ["humidity"]`. It is not possible to append the content within a parameter. It must be fully overwritten.



### Remove Objects `"remove":[...]`
{: .d-inline-block }

Command
{: .label .label-green }


### Request Objects `"request":[...]`
{: .d-inline-block }

Command
{: .label .label-green }


### Reset Device `"reset":{...}`
{: .d-inline-block }

Command
{: .label .label-green }


### Device Info `"device":{...} `
{: .d-inline-block }

Object
{: .label .label-yellow }


### Network Info `"network":{...}`
{: .d-inline-block }

Object
{: .label .label-yellow }


### Power Info & Configuration `"power":{...}`
{: .d-inline-block }

Object
{: .label .label-yellow }


### FPGA Configuration `"fpga":{...}`
{: .d-inline-block }

Object
{: .label .label-yellow }


### Security Configuration `"security":{...}`
{: .d-inline-block }

Object
{: .label .label-yellow }


### Sensor Info & Configuration `"_YOUR_SENSOR_":{...}`
{: .d-inline-block }

Object
{: .label .label-yellow }