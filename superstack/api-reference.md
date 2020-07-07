---
layout: default
title: API Reference
nav_order: 1
parent: SuperStack
---

## Commands and Objects
{: .no_toc }

*Commands* are top level instructions to work with *Objects*. *Objects* cannot be modified directly, they must be issued inside the relevant *Command* for the required operation. The example below shows how to request device information. Here the **device** is the *Object*, and **request** is the *command*.

``` JSON
{
    "request":["device"]
}
```

## API Reference
{: .no_toc }
1. TOC
{:toc}

### "initialise":{...}
{: .d-inline-block }
Command {: .label .label-green }


### "modify":{...}
{: .d-inline-block }
Command {: .label .label-green }


### "remove":[...]
{: .d-inline-block }
Command {: .label .label-green }


### "request":[...]
{: .d-inline-block }
Command {: .label .label-green }


### "reset":{...}
{: .d-inline-block }
Command {: .label .label-green }


### "device":{...} 
{: .d-inline-block }
Object {: .label .label-yellow }

### "network":{...}
{: .d-inline-block }
Object {: .label .label-yellow }

### "power":{...} 
{: .d-inline-block }
Object {: .label .label-yellow }

### "fpga":{...}
{: .d-inline-block }
Object {: .label .label-yellow }


### "security":{...}
{: .d-inline-block }
Object {: .label .label-yellow }

### "_YOUR_SENSOR_":{...}
{: .d-inline-block }
Object {: .label .label-yellow }