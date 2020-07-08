---
layout: default
title: Reset Database
nav_order: 5
parent: API Reference
grand_parent: SuperStack RTOS
---

# `"reset": {}`
{: .d-inline-block }
Stable
{: .label .label-green }

Clears all user configured information from the device and appends default settings for `power`, `fpga` and `security`.

Takes no arguments. Simply issue:
```json
"reset":{}
```

## Returns:
{: .no_toc }

- `"reset":"okay"` - Reset has completed successfully