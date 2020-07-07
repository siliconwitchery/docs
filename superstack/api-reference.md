---
layout: default
title: API Reference
nav_order: 1
parent: SuperStack
---

## Commands and Objects
{: .no_toc }

*Commands* are top level instructions to work with *Objects*. *Objects* cannot be modified directly, they must be issued inside the relevant *Command* for the required operation. The example below shows how to request device information. Here the **device** is the *Object*, and **request** is the *command*.

<div class="code-example" markdown="1">
```json
{
    "request":["device"]
}
```
</div>

## API Reference
{: .no_toc }
1. TOC
{:toc}

### Initialise Objects `"init":{...}`
{: .d-inline-block }
Command
{: .label .label-green }

Initialises an **Object** with new values, fully removing any **Objects** of the same name if they previously existed.

### Example:

1. The SuperStack Database currently does **not** contain an Object named `"sensor 1"`.
2. Issue an **Initialise Command**:
```json
{
    "init":{
        "sensor 1":{
            "chip":"BME280",
            "return": ["temperature","pressure"],
            "change.morethan": 10.5 
        }
    }
}
```
3. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
    "sensor 1":{
        "chip":"BME280",
        "return": ["temperature","pressure"],
        "change.morethan": 10.5 
    }
```
4. Issue another **Initialise Command**:
```json
{
    "init":{
        "sensor 1":{
            "chip":"BME280",
            "return": ["humidity"],
            "period.sec": 30
        }
    }
}
```
5. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
{
    "sensor 1":{
        "chip":"BME280",
        "return": ["humidity"],
        "period.sec": 30
    }
}
```
Note that the `"change.morethan"` parameter was removed. This is because the Initialise Command always overwrites all entries in the Object.

### Append Objects `"append":{...}`
{: .d-inline-block }

Command
{: .label .label-green }

Updates an **Object** with the parameters given, but keeps existing parameters unchanged.

### Example:

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