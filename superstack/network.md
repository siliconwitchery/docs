---
layout: default
title: Get Network Info
nav_order: 7
parent: API Reference
---

# Getting Network Info Object `"network":{...}`
{: .d-inline-block }
Object
{: .label .label-yellow }

The `network` Object is a persistant object with **read-only** Parameters containing network status.

## Returns:
{: .no_toc }

- `"network": {...}` network Object with **Parameters** shown below.
- `"read-only": ["network"]` if the user attempts to **Remove** or **Append** the read only Parameters.

## Read Only Parameters:
{: .no_toc }

- `"connected": bool` - Connected state of the device. `true` if connected.
- `"address": string` - Network 48bit MAC address of the device. Format: `"01-23-45-67-89-AB"`
- `"buffer-size": integer` - Maximum buffer size for single transfers.
- `"tx-pending: bool"` - Flag to indicate that a **Response** is pending. `true` if pending.