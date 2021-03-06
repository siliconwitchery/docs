---
layout: default
title: Get Device Info
nav_order: 6
parent: API Reference
grand_parent: SuperStack RTOS
published: false
---

# `"device": {...} `
{: .d-inline-block }
Stable
{: .label .label-green }

The `device` Object is a persistant object with **read-only** Parameters containing device information.

## Returns:
{: .no_toc }

- `"device": {...}` device Object with **Parameters** shown below
- `"read-only": ["device"]` if the user attempts to **Remove** or **Append** the read only Parameters.

## Read Only Parameters:
{: .no_toc }

- `"model": string` - Model name of the device. e.g. `"Silicon Witchery S1 Module"`
- `"fw-version": string` - Firmware version stamp of the device. Format: `"YYYYMMDD.HHMM"`
