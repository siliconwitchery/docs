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

Run `superstack help` to list every command, and `superstack help <command>` to explain one, such as `superstack help upload` or `superstack help device pair`. The help comes from the CLI itself, so it always matches the version you have installed. These tables copy it.

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
| `superstack download <imei> <path>` | Download the code last uploaded to a device into `<path>` |
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

---

## Options and login

| Option | What it does |
| --- | --- |
| `--json` | Print the list as one line of JSON instead of a table. `fleet list`, `device list`, `member list`, `key list` and `account balance` take it |
| `-h`, `--help` | Show the help, the same as `superstack help` |
| `-v`, `--version` | Show the version, the same as `superstack version` |
| `--server <url>` | Use another Superstack server. Without it, the CLI uses `https://supernext.siliconwitchery.com` |

`superstack login` saves your login on the computer until you run `superstack logout` or `superstack account delete`. On Linux it is in `~/.local/state/superstack/key`, or `$XDG_STATE_HOME/superstack/key` when that is set. On macOS and Windows it is in `superstack/key` in your user config folder.

Every command that fails prints `superstack:` and the reason, such as `superstack: no such device`, and exits with status 1.

Commands that delete or hand over something ask `[y/N]` first: `fleet transfer`, `fleet delete`, `device unpair`, `member remove`, `key revoke`, `account delete`, and `download` when it would replace a file.

---

## What an upload sends

`superstack upload` and `superstack dev` replace all the code on the device, or on every device in the fleet, with the files you name:

- A file goes to the top level of the device, under its own name.
- A folder's contents go to the top level, and the folders inside it keep their names. Names that start with a dot are skipped.
- The files must include `main.lua`, which the device runs.

For example, `superstack upload <imei> .` in a folder that holds `main.lua` and `lib/sensors.lua` puts both on the device, and `require("lib/sensors")` loads the second.

The device receives the code at its next check-in, then starts it. Superstack asks the device to check in straight away after an upload, a `device start`, `stop` or `restart`, or a message, so the device usually acts within seconds. A device in [low power mode](/pages/superstack/lua#set-low-power-mode) acts at its regular check-in, up to 15 minutes later.

The CLI or Superstack refuses the upload with one of these messages:

| The CLI prints | Cause |
| --- | --- |
| `the upload must include main.lua` | No file is named `main.lua` |
| `<name> would be uploaded twice, from <path> and <path>` | Two files you named land on the same path on the device |
| `a file and a directory cannot share the name <name>` | A file has the same path as a folder |
| `a file path cannot be used on the device` | A path is longer than 255 bytes, contains a control character, or has an empty, `.` or `..` part |
| `tmp/ is reserved for the device` | A path is `tmp` or starts with `tmp/`, where the device keeps [temporary files](/pages/superstack/lua#temporary-files) |
| `the files are too large to upload` | The files are far larger than the device's storage |
| `the files need <n> KiB of storage, but the device has <n> KiB` | The files don't fit the device's storage |
| `the files need <n> KiB of storage, but device <imei> has <n> KiB` | The files don't fit a device in the fleet. The message names the smallest |
| `the fleet has no credit, run account topup <fleet_id> to add some` | The fleet has no [credit](/pages/superstack/credit) |

A fleet upload is refused whole when any part of it fails.

---

## Device states

`superstack device list` shows each device's IMEI, name, fleet, state, storage and when it was last seen. Last seen is the last time the device reached Superstack, such as `just now` or `5 min ago`. It does not show whether the device is online now.

| State | Meaning |
| --- | --- |
| `running` | The code is running |
| `stopped` | The code ended, or `device stop` stopped it |
| `crashed` | The code raised an error or reset the device. The log shows which |
| `no code` | No code has been uploaded since the device was paired |
| `updating` | New code waits for the device's next check-in |
| `starting`, `stopping`, `restarting` | A `device start`, `stop` or `restart` waits for the device's next check-in |
| `no credit` | New code waits, and the fleet has no [credit](/pages/superstack/credit) to send it |
| `updating firmware` | The device is installing a [firmware update](/pages/s2-module#automatic-firmware-updates) |
| `no space` | The code doesn't fit the device's storage. Upload less |
| `rejected` | The device could not use the code. Upload it again |
| `failed` | Three attempts to send the code failed. Upload it again |
| `-` | The device hasn't reported its state yet |

`superstack device start` and `superstack device restart` refuse a device in `no code`, `no space`, `rejected` or `failed`. Upload code first.

Storage shows the space the code and temporary files use, out of the 96 KiB the device has. The device stores files in 4 KiB blocks. A file of up to 512 bytes shares a block with others, but a larger one takes at least a whole block, so a 600-byte file uses 4 KiB. The file system uses part of the storage too, so it never shows zero.

---

## Logs

`superstack tail <fleet_id>` prints the fleet's newest 100 logs, then follows new ones until you press Ctrl-C. `superstack dev` follows only the logs that arrive after it starts. Each line shows when the log arrived in your local time, the IMEI, the kind of log, the device's name and the text:

```
2026-10-27T14:02:11+01:00 350457790012345 print [bench] hello world
```

| Kind | Text |
| --- | --- |
| `print` | The output of `print()` in the code |
| `state` | `Code started`, `Code ended` or `Code stopped` |
| `error` | `Code crashed:` and the error, or `Code crashed the device, so it was not started again` |

Superstack keeps each log for 14 days. Unpairing a device deletes its logs. You can follow logs in up to 8 places at once.

---

## Owners and members

Every fleet has one owner. The owner can add members with `superstack member add`, and the person must have logged in to Superstack once first.

| Action | Owner | Member |
| --- | :---: | :---: |
| Pair, rename, unpair, start, stop and restart devices | ✅ | ✅ |
| Upload and download code, and read logs | ✅ | ✅ |
| Create, list and revoke fleet keys | ✅ | ✅ |
| See the balance and top up | ✅ | ✅ |
| Rename, transfer and delete the fleet | ✅ | - |
| Add and remove members | ✅ | - |

A user can own up to 100 fleets. A fleet name, device name or fleet key label is at most 100 characters. To delete your account, first transfer or delete every fleet you own.

