---
layout: default
title: Append Object
nav_order: 2
parent: API Reference
grand_parent: SuperStack RTOS
---

# `"append": {...}`
{: .d-inline-block }
Command
{: .label .label-green }

Updates **Objects** with the parameters given, but keeps existing parameters unchanged.

## Returns:
{: .no_toc }

- `"appended": ["object", ... ]` if the object existed and was successfully appended
- `"not-found": ["object", ... ]` if the object was not found in the Database
- `"no-space": ["object", ... ]` if there isn't enough space in the database to store the object
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

## Example:
{: .no_toc }

1. The SuperStack Database already contains an Object named `"sensor 1"`.
```json
"sensor 1": {
    "chip": "BME280",
    "return": ["temperature","pressure"],
    "change.morethan": 10.5 
}
```

2. Issue an **Append Command**:
```json
"append": {
    "sensor 1": {
        "return": ["humidity"],
        "period.sec": 30
    }
}
```

3. The SuperStack Database now contains the `"sensor 1"` Object as shown:
```json
"sensor 1": {
    "chip": "BME280",
    "return": ["humidity"],
    "change.morethan": 10.5,
    "period.sec": 30
}
```

The `"period.sec"` parameter was added to the Object and the `"return"` parameter was appended. All other parameters remain unchanged.
Note that indavidual parameters are still fully overwritten. In this case `"return": ["temperature","pressure"]` → `"return": ["humidity"]`. It is not possible to append the content within a parameter. It must be fully overwritten.