---
layout: default
title: Remove Object
nav_order: 3
parent: API Reference
grand_parent: SuperStack RTOS
---

# `"remove": [...]`
{: .d-inline-block }
Stable
{: .label .label-green }

Removes **Objects** given in the array.

## Returns:
{: .no_toc }

- `"removed": ["object", ... ]` if the object was successfully removed
- `"not-found": ["object", ... ]` if the object was not found in the Database
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

## Example:
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

2. Issue a **Remove Command**:
```json
{
    "remove": ["sensor 1"]
}
```

The SuperStack Database no longer contains the `"sensor 1"` Object.
