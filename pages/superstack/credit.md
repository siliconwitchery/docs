---
title: Credit
parent: "S2 & Superstack"
description: How Superstack credit pays for S2 Module data. Prices, what spends credit, what stops when a fleet runs out, and how to check and top up a balance.
image: /assets/images/superstack-annotated-masthead.png
nav_order: 5
---

# Credit
{: .no_toc }

---

Every S2 Module has a SIM and a data plan built in. You pay for the data that your code and your application send, with credit that you add to a fleet in advance. There is no subscription or contract.

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Prices

| Item | Price |
|------|-------|
| Starter credit | €10, included with every new S2 |
| Data | €1 per MB, where 1 MB is 1,000,000 bytes |
| Top-up | From €1 to €1,000 at a time, before tax |

The price covers the network overhead around your data, so you can estimate the cost from the size of your own data:

```
cost per day = bytes per day / 1,000,000 × €1
```

Code that sends 200 bytes a minute sends 288,000 bytes a day, which costs about €0.29 a day.

---

## What spends credit

These spend credit, in both directions:

- **Code uploads.** An upload sends each device only the files that differ from the ones it holds. A fleet upload sends them to every device in the fleet.
- **Logs.** The output of `print()`, and the logs that say code started, ended, stopped or crashed.
- **Messages to a device**, from your application or from another device's Lua.
- **Web requests from Lua.** A request counts its URL, headers and body, and the response counts its body.

Data that the network resends on its own spends nothing, and a device that is offline spends nothing. An upload or a message that fails partway, such as over a weak connection, spends credit for the part that arrived, and each retry spends again.

These are free:

- Check-ins between the S2 and Superstack.
- Pairing and unpairing.
- Starting, stopping and restarting code.
- Firmware updates.

---

## When a fleet runs out of credit

A fleet has no credit when its balance is zero or less. Its code keeps running, but no data that spends credit leaves the S2 or Superstack:

- Superstack refuses uploads to the fleet. `superstack upload` says that the fleet has no credit.
- Superstack refuses messages to the fleet with `402 Payment Required`.
- The S2 discards its logs instead of sending them.
- A web request from Lua returns the error `no credit` straight away.
- `superstack device list` shows `no credit` for a device whose code is waiting to be sent.

You can still pair and unpair the S2, and start, stop and restart its code. The S2 still installs firmware updates.

Data already on its way when the credit runs out is still delivered and charged, so the balance can go below zero. The next top-up pays that first.

---

## Check the balance

```sh
superstack account balance
```

The CLI lists each fleet you can reach with its balance. Add a fleet id to show one fleet.

---

## Top up a fleet

1. Run:

    ```sh
    superstack account topup <fleet_id>
    ```

1. Press Enter. Your browser opens the payment page.
1. Choose an amount, and pay.

The credit shows in `superstack account balance` once the payment completes. Each S2 in the fleet starts sending data again at its next check-in.

---

## Credit belongs to a fleet

Credit belongs to a fleet, never to a device:

- A new S2 gives its starter credit to the first fleet it is paired with, and that fleet keeps it.
- Unpairing an S2, or giving it to someone else, moves no credit.
- A second-hand S2 brings no starter credit. Top up its new fleet before you upload code to it.
- Transferring a fleet to a new owner moves its credit with it.
- Deleting a fleet forfeits its remaining credit.

Swedish bookkeeping law requires Silicon Witchery to keep each fleet's record of top-ups and spending, so the record stays after you delete the fleet or your account. It names the fleet, not you.
