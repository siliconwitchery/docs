---
layout: default
title: Request Object
nav_order: 4
parent: API Reference
grand_parent: SuperStack RTOS
---

# `"request": [...]` and `"request": {...}`
{: .d-inline-block }
Command
{: .label .label-green }

Instructs SuperStack to respond with the objects provided. Optionally, individual parameters may be requested within objects.

## Returns:
{: .no_toc }

- `"object": {"parameters", ... }` if the object was found in the Database
- `"not-found": ["object", ... ]` if the object was not found in the Database
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

## Example:
{: .no_toc }

1. The SuperStack Database already contains an Object named `sensor 1`.
```json
"sensor 1": {
    "chip":"BME280",
    "return": ["temperature","pressure"]
}
```

2. Request `sensor 1` and `network` objects
```json
"request":["sensor 1", "network"]
```

3. The two objects will be returned in full
```json
"sensor 1": {
    "chip": "BME280",
    "return": ["temperature","pressure"]
},
"network": {
    "connected": true,
    "address": "12-23-34-AB-BA-CD"
}
```

4. If we only want specific parameters from an object. It's possible to specify the parameters in a list:
```json
"request": {
    "sensor 1":["chip"]
}
```

5. The response will therefore become"
```json
"sensor 1": {
    "chip": "BME280"
}
```