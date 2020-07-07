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
{
    "sensor 1":{
        "chip":"BME280",
        "return": ["temperature","pressure"],
        "change.morethan": 10.5 
    }
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

### Modify Objects `"modify":{...}`
{: .d-inline-block }

Command
{: .label .label-green }

Updates an **Object** with the parameters give, but keeps existing parameters unchanged.

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