---
title: Superstack API
parent: "S2 & Superstack"
description: API reference for sending messages from your own application to one S2 Module, several, or a whole fleet through Superstack.
image: /assets/images/superstack-annotated-masthead.png
nav_order: 4
---

# Superstack API reference
{: .no_toc }

---

Your application sends data to S2 Modules with an HTTP `POST` to Superstack. Each request carries one message of up to 4096 bytes, such as a command, a setting or a JSON document. Superstack holds the message until each device collects it, and the Lua on the device receives it through [`network.assign_message_event`](/pages/superstack/lua#assign-an-event-handler-for-messages).

To manage fleets, devices and code, use the [Superstack CLI](/pages/superstack/cli).

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Create a fleet key

A fleet key lets your application send messages to the devices in one fleet. The owner and any member of the fleet can create one.

1. Find the id of your fleet:

    ```sh
    superstack fleet list
    ```

1. Create a fleet key, with a label that names the application that will use it:

    ```sh
    superstack key create <fleet_id> greenhouse-controller
    ```

    The CLI prints the fleet key once. Store it where your application can read it, because anyone who holds it can send messages to every device in the fleet.

A fleet key reaches only its own fleet. It works until you revoke it or delete the fleet. To revoke one, find its id with `superstack key list`, then run `superstack key revoke <key_id>`.

---

## Send a message

```
POST https://supernext.siliconwitchery.com/fleets/{fleet_id}/messages
```

{: .note-title }
> Authentication
> - Send the fleet key in the `Authorization` header as `Bearer <fleet_key>`
> - The fleet key must belong to the fleet in the path

{: .note-title }
> Query parameters
> - `imei` - optional - The 15-digit IMEI of a device paired with the fleet. Repeat it to send the message to several devices. Leave it out to send the message to every device paired with the fleet
> - `expires_in` - optional - How many seconds Superstack keeps the message for a device that has not collected it. From `30` to `1209600` (14 days). Defaults to `3600` (1 hour)

{: .note-title }
> Request body
>
> The message, at most 4096 bytes. It can be text or binary, such as JSON or a packed struct. Lua receives exactly these bytes as a string. Superstack ignores `Content-Type`.

{: .note-title }
> Response (202 Accepted)
>
> The body is empty. Superstack has queued the message for every device the request names, but no device has received it yet.

Send `on` to one device:

```sh
curl -X POST "https://supernext.siliconwitchery.com/fleets/<fleet_id>/messages?imei=<imei>" \
    -H "Authorization: Bearer <fleet_key>" \
    --data-binary "on"
```

Send a JSON document to two devices, and keep it for a day:

```sh
curl -X POST "https://supernext.siliconwitchery.com/fleets/<fleet_id>/messages?imei=<imei>&imei=<imei>&expires_in=86400" \
    -H "Authorization: Bearer <fleet_key>" \
    --data-binary '{"interval":60,"led":true}'
```

Send a file to every device in the fleet:

```sh
curl -X POST "https://supernext.siliconwitchery.com/fleets/<fleet_id>/messages" \
    -H "Authorization: Bearer <fleet_key>" \
    --data-binary @settings.json
```

Use `--data-binary` rather than `--data`, because `--data` removes the newlines from a file.

---

## How a message reaches a device

When Superstack accepts a request, it queues one copy of the message for each device the request names. A device paired with the fleet later does not receive it.

Superstack then asks each device to collect its messages straight away. A device in power-saving mode collects them at its next check-in, which is at most 15 minutes away.

Each device receives its messages in the order your application sent them. Superstack removes a message from the queue when the device confirms that it received it. A message the device does not confirm stays queued, and Superstack tries again at the next check-in.

The device confirms a message even when nothing receives it in Lua:

- If the code is stopped, the device discards the message.
- If the code has not assigned a handler with `network.assign_message_event`, the device discards the message.

If the device's confirmation is lost on the network, Superstack sends the message again, so Lua can receive the same message twice. Write a message that has the same effect when it arrives twice, such as `{"led":true}` rather than `toggle`.

The device has room for one 4096-byte message, or several shorter ones, that Lua has not handled yet. Each message takes 2 bytes more than its length. When a message does not fit, the device refuses it, and the message stays queued until a later check-in.

Superstack discards a message without delivering it in these cases:

- The device has not confirmed it before `expires_in` runs out.
- The device is unpaired from the fleet. Its queued messages are discarded, so a device paired with another fleet never receives them.

---

## Receive a message in Lua

Assign a handler before the messages arrive, and keep the code running, because the device discards messages while the code is stopped:

```lua
network.assign_message_event(function(content)
    local settings = json.decode(content)
    device.digital.set_output("B1", settings.led)
    print("Interval is now " .. settings.interval)
end)

while true do
    device.sleep(1)
end
```

The [Lua reference](/pages/superstack/lua#assign-an-event-handler-for-messages) describes `network.assign_message_event` and `network.unassign_message_event`.

---

## Errors

Superstack refuses the whole request when any part of it fails, and queues nothing. The response body is a plain-text sentence that says what went wrong.

| Status | Cause |
| --- | --- |
| `400 Bad Request` | An `imei` is not 15 digits, an `imei` names a device that is not paired with the fleet, or `expires_in` is outside 30 to 1209600 |
| `401 Unauthorized` | The request has no fleet key, or the fleet key has been revoked or its fleet deleted |
| `403 Forbidden` | The fleet key belongs to another fleet |
| `404 Not Found` | The fleet id in the path is not a number |
| `413 Content Too Large` | The message is longer than 4096 bytes |
| `429 Too Many Requests` | A device the request names already has 100 messages queued. Try again after it collects some |
| `503 Service Unavailable` | Superstack could not queue the message. Try again |
