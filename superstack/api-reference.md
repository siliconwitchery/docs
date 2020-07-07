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

### Initialise Objects `"initialise":{...}`
{: .d-inline-block }

Command
{: .label .label-green }


### Modify Objects `"modify":{...}`
{: .d-inline-block }

Command
{: .label .label-green }


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