---
layout: default
title: Add Object
nav_order: 1
parent: API Reference
grand_parent: SuperStack RTOS
---

# Adding Objects `"add":{...}`

Command
{: .label .label-green }

Initialises **Objects** with the parameters given, fully removing any **Objects** of the same name if they already exist in the Database.

## Returns:
{: .no_toc }

- `"added": ["object", ... ]` if the object didn't exist but was successfully added
- `"re-added": ["object", ... ]` if the object existed and was successfully re-added
- `"no-space": ["object", ... ]` if there isn't enough space in the database to store the object
- `"bad-json": null` if an error was encountered in parsing the provided JSON data

## Example:
{: .no_toc }

1. Assume The SuperStack Database does **not** already contain an Object named `sensor 1`.

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

3. The SuperStack Database now contains the `sensor 1` Object as shown:
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

5. The SuperStack Database now contains the `sensor 1` Object as shown:
```json
"sensor 1":{
    "chip": "BME280",
    "return": ["humidity"],
    "period.sec": 30
}
```

Note that the `change.morethan` parameter was removed. This is because the `add` Command always overwrites all entries in the Object.