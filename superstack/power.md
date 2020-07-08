---
layout: default
title: Get/Configure Power
nav_order: 8
parent: API Reference
grand_parent: SuperStack RTOS
---

# `"power": {...}`
{: .d-inline-block }
Preliminary
{: .label .label-yellow }

The `power` Object is a persistant object with both **writable** as well as **read-only** Parameters containing device power status and configuration.

## Returns:
{: .no_toc }

- `"power": {...}` power Object with **Parameters** shown below.
- `"read-only": ["power"]` if the user attempts to **Remove** or **Append** the read only Parameters.

## Read Only Parameters:
{: .no_toc }

- `"battery": string` - Battery charger state. Values: `"no-battery"`, `"discharging"`, `"charging"`, `"charged"`
- `"level": integer` - Battery level percentage. Values: `0` to `100`
- `"uptime": string` - Time device has been powered. Format in [ISO8601 Duration](https://en.wikipedia.org/wiki/ISO_8601#Durations) e.g. `"P46DT12H30M5S"`

## Writable Parameters:
{: .no_toc }

- `"io1-v": float` - User configurable IO1 voltage (V). Value `0` to `5.0`. Default `0`
- `"io2-v": float` - User configurable IO2 voltage (V). Value `0` to `5.0`. Default `0`
- `"charge-v": float` - Battery charger constant voltage limit (V). Value `4.1` to `4.7`. Default `4.1`
- `"charge-i": float` - Battery charger constant current limit (mA). Value `5` to `250`. Default `5`
- `"charge-enable: bool"` - Enable or disable the battery charger. Default `false`