---
layout: default
title: API Reference
nav_order: 1
parent: SuperStack RTOS
has_children: true
---

# API General Rules 

- The SuperStack API interface uses the [JSON Schema](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Objects/JSON).

- **Commands** are top level instructions to work with **Objects**.

- **Objects** take the form:
```json
"some object": {
    "parameter 1": "some value",
    "parameter 2": "another value"
}
```

- **Objects** can contain **Parameters** of the following data types:
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

- **Objects** cannot be directly modified, they must be issued inside the relevant **Command** for the required operation. To read the `device` **Object**, the `request` **Command** must be used:
```json
"request": ["device"]
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

- **Commands** will trigger a **Response** to be sent back from the device. These can be an array of **Object Names** denoting the current operation, or an **Object** itself with returnable parameters:
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

- Multiple **Commands** and **Objects** may be issued at the same time:
```json
"init": {
    "sensor 2": {
        "chip": "BME280",
        "return": ["temperature","pressure"]
    },
    "sensor 3": {
        "chip": "MPU6050",
        "return": ["Xaccel","Yaccel"]
    }
},
"remove": ["sensor 1"],
"request": ["device", "sensor 4", "sensor 5"]
}
```

- The internal SuperStack Database is limited in size. Care must be taken to keep **Object** and **Parameter** names short to save space, but understandable enough for convenience in development. It's recomended that un-needed Objects are removed with the `remove` command once no longer needed. The `reset` command can also be used to clear the databse of all user content if needed.

# API Reference