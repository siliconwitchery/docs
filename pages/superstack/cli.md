---
title: Superstack CLI
parent: "S2 & Superstack"
description: The Superstack CLI. Log in, pair an S2 Module with a fleet, upload Lua, stream its log and manage credit from the terminal.
image: /assets/images/superstack-annotated-masthead.png
nav_order: 3
---

# Superstack CLI
{: .no_toc }

---

`superstack` is the command line interface to Superstack. It logs you in, pairs S2 Modules with fleets, uploads Lua to them, streams their logs and manages credit. It is a single static binary.

[Install instructions](https://github.com/siliconwitchery/superstack-cli#install){: .btn .btn-purple}
[Releases](https://github.com/siliconwitchery/superstack-cli/releases){: .btn}

---

## Commands

Run `superstack help` to list every command, and `superstack help <command>` to explain one, such as `superstack help upload`. The help comes from the CLI itself, so it always matches the version you have installed. These tables copy it.

### Getting started

| Command | What it does |
| --- | --- |
| <code>superstack login &lt;github&#124;gitlab&gt;</code> | Log in with the selected provider |
| `superstack logout` | Log out of your account |

### Fleets

| Command | What it does |
| --- | --- |
| `superstack fleet create <name>` | Create a fleet |
| `superstack fleet list [--json]` | List the fleets you can reach |
| `superstack fleet rename <fleet_id> <new_name>` | Rename a fleet |
| `superstack fleet transfer <fleet_id> <email>` | Hand a fleet to a new owner |
| `superstack fleet delete <fleet_id>` | Delete a fleet and unpair its devices |

### Devices

| Command | What it does |
| --- | --- |
| `superstack device pair <imei> <fleet_id> [name]` | Pair a device with a fleet |
| `superstack device list [fleet_id] [--json]` | List devices and when they were last seen |
| `superstack device rename <imei> <new_name>` | Rename a device |
| `superstack device unpair <imei>` | Remove a device from its fleet |
| `superstack device start <imei>` | Start the code on a device |
| `superstack device stop <imei>` | Stop the code on a device |
| `superstack device restart <imei>` | Restart the code on a device |

### Files

| Command | What it does |
| --- | --- |
| <code>superstack upload &lt;imei&#124;fleet_id&gt; &lt;file&gt; ...</code> | Upload files or directories to a device or fleet |
| `superstack download <imei> <path>` | Download the code last uploaded to a device into <path> |
| <code>superstack dev &lt;imei&#124;fleet_id&gt; &lt;file&gt; ...</code> | Upload on every change, and follow the log from the first upload |

### Logs

| Command | What it does |
| --- | --- |
| `superstack tail <fleet_id> [imei ...] [-n num [-o num]]` | Follow a fleet's log as it arrives, or print a window of its past logs with -n |

### People

| Command | What it does |
| --- | --- |
| `superstack member add <email> <fleet_id>` | Add a member to a fleet |
| `superstack member list <fleet_id> [--json]` | List a fleet's owner and members |
| `superstack member remove <email> <fleet_id>` | Remove a member from a fleet |

### Fleet keys

| Command | What it does |
| --- | --- |
| `superstack key create <fleet_id> <label>` | Create a fleet key for sending data to a fleet |
| `superstack key list [fleet_id] [--json]` | List the fleet keys that can reach your fleets |
| `superstack key revoke <key_id>` | Stop a fleet key from reaching its fleet |

### Account

| Command | What it does |
| --- | --- |
| `superstack account balance [fleet_id] [--json]` | Show the credit left on your fleets |
| `superstack account topup <fleet_id>` | Add credit to a fleet |
| `superstack account delete` | Delete your account entirely |

### Superstack

| Command | What it does |
| --- | --- |
| `superstack version` | Show the version |
| `superstack help [command]` | Show this help, or help for one command |
