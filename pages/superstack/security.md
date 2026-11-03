---
title: Security
parent: "S2 & Superstack"
description: Security information for the S2 Module and Superstack. Who to contact, how updates install, the support period, risks to know about, and how to remove your data.
image: /assets/images/superstack-annotated-masthead.png
nav_order: 6
---

# Security
{: .no_toc }

This page holds the security information that the EU Cyber Resilience Act requires for the S2 Module and Superstack.

---

## Contents
{: .no_toc }

1. TOC
{:toc}

---

## Manufacturer and contact

Silicon Witchery AB makes the S2 Module and Superstack.

- **Address:** Sankt Paulsgatan 25, 11848 Stockholm, Sweden
- **Email:** info@siliconwitchery.com
- **Website:** [siliconwitchery.com](https://www.siliconwitchery.com)

Report a security vulnerability to security@siliconwitchery.com, as the [security and vulnerability disclosure policy](https://www.siliconwitchery.com/security) describes.

## EU declaration of conformity

The [EU declaration of conformity](/assets/files/s2-module-eu-declaration-of-conformity.pdf) covers the S2 Module, its firmware and Superstack.

## Products this page covers

| Product | How to identify it |
| --- | --- |
| S2 Module, part numbers `S2-MODULE` and `S2-MODULE-EXT-ANT` | The IMEI on its [label](/pages/s2-module#labeling) |
| S2 Module firmware | Released by Silicon Witchery and installed automatically |
| Superstack, the service that carries code to the S2 and its data back | `supernext.siliconwitchery.com` |
| Superstack CLI | `superstack version` |

## Intended purpose

The S2 Module is a cellular module that puts a maker's own project online. It runs Lua code that its user writes. Superstack carries that code to the S2, and carries its logs and data back. The S2 can't be used without Superstack.

## Security properties

- Each S2 has its own device key. None has a default password.
- The S2 talks only to Superstack, over DTLS 1.2 with AES-128 encryption. The CLI and your own project talk to Superstack over HTTPS.
- The S2 accepts new firmware only from Superstack, over its encrypted connection. It checks each image for damage before it runs it, and returns to the firmware before it if the new image can't reconnect.
- Pairing needs the IMEI and a press of the [pairing button](/pages/s2-module#status-leds--button).
- Lua on the S2 reaches the internet only through Superstack, which refuses requests to private network addresses.
- A fleet key reaches only its own fleet, and you can revoke it.

## Risks to know about

- **A fleet key lets anyone who holds it send messages to every device in its fleet.** Keep it where only your project can read it. If it leaks, revoke it with `superstack key revoke <key_id>`.
- **A member of a fleet can do everything to its devices**, including uploading code and unpairing them. The [owners and members](/pages/superstack/cli#owners-and-members) table lists what each can do.
- **Your login stays on your computer** until you run `superstack logout`.
- **Anyone who holds an unpaired S2 can pair it with their own fleet**, because the IMEI is printed on its label.
- **A Lua request to an `http://` address travels unencrypted** between Superstack and the service it calls. Use `https://` addresses.
- **Your code decides what the S2 sends and where.**

## Set up and use the S2 securely

1. Set up the S2 with the [getting started guide](/pages/s2-superstack).
1. Keep fleet keys secret.
1. Check who can reach a fleet with `superstack member list <fleet_id>` and `superstack key list <fleet_id>`, and remove anyone or any key you no longer need.
1. Use `https://` addresses in Lua [network requests](/pages/superstack/lua#networking-libraries).

Each of these changes who can reach your devices and data:

- `superstack member add` gives a person every device action in the fleet.
- `superstack key create` gives a project the right to send messages to every device in the fleet.
- `superstack fleet transfer` hands the fleet and its devices to a new owner.
- `superstack upload` replaces the code that handles your data on the device.

## Security updates

The S2 Module receives security updates until **December 2032**, free of charge.

| Product | How updates install |
| --- | --- |
| S2 Module firmware | Automatically, as [automatic firmware updates](/pages/s2-module#automatic-firmware-updates) describes. They can't be turned off |
| Superstack | Silicon Witchery updates it |
| Superstack CLI | Install the newest release, as the [install instructions](https://github.com/siliconwitchery/superstack-cli#install) describe |

## Stop using the S2 and remove your data

To stop using an S2, unpair it:

```sh
superstack device unpair <imei>
```

The S2 deletes all your code files, restarts Lua and waits to be paired again. Superstack deletes the code, logs and waiting messages it held for the S2. `superstack fleet delete <fleet_id>` unpairs every device in the fleet and deletes the fleet.

To delete your account, first delete each fleet you own or hand it over with `superstack fleet transfer`. Then run:

```sh
superstack account delete
```

The [privacy policy](https://www.siliconwitchery.com/privacy) lists what Superstack keeps after that, and for how long.

## Build the S2 into your own product

A product that contains an S2 gets the security properties and security updates on this page. Your Lua code, your fleets and fleet keys, and the services your code and project reach are yours to secure.
