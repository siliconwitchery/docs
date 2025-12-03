---
title: API Reference
parent: Superstack Platform
description: 
image: /assets/images/superstack-annotated-masthead.png
nav_order: 2
---

# Superstack API Reference
{: .no_toc }

---

Superstack exposes all functionality featured in the web-app as REST APIs. This allows for tight integration of Superstack with your own applications. 

<!-- TODO explain these in a couple paragraphs -->
- Pull data dynamically into your own apps as and when needed
- Expose natural language interfaces for different types of users
- Monitor logs from your own dashboards
- Monitor and manage devices alongside existing IoT infrastructure
- React to events and trigger actions on devices

---

## Contents
{: .no_toc}

1. TOC
{:toc}

---

## Authentication

### Deployment ID

The **Deployment ID** is used for accessing all data within a deployment. This ID can be found on the **Settings Tab**:

![Superstack deployment ID](/assets/images/superstack-deployment-id.png)

The API signatures shown below include placeholders for the Deployment ID shown as `{deploymentId}`. Wherever you see this, simply replace it with the real Deployment ID.

```
https://super.siliconwitchery.com/api/{deploymentId}/logs
# becomes
https://super.siliconwitchery.com/api/c309cd39-e9fc-4f49-b4ed-6a5c57c8a515/logs
```

### API Key

Many of the APIs require authentication via an **API Key**. To generate an API Key, navigate to the **API Keys** section of the **Settings Tab**, and click **Create**.

Give the API Key a **Name** and desired **Permissions**. Permissions are granular, allowing specific keys to only access specific information.

![Superstack API Keys](/assets/images/superstack-api-key.png)

Once an API Key has been created, add it to the `X-Api-Key` header when making a request:

```sh
curl https://super.siliconwitchery.com/api/{deploymentId}/logs \
    -H 'X-Api-Key: <Your newly created API key>'
```

{: .warning-title }
> Treat API Keys as secrets
>
> To prevent unauthorized access to your data, keep API Keys securely stored, and do not expose keys in client-side code.

---

## Deployments

---

## Devices

---

## Code

---

## Logs

#### Retrieve logs

```
GET https://super.siliconwitchery.com/api/{deploymentId}/logs?filters=
```

{: .note-title }
> Authentication & Permissions
>
> - API key is not required if the deployment is public
> - API key requires **read logs** permission

{: .note-title }
> Optional query parameters
> - `filters` - **json string** - JSON-encoded filter object
> ```jsonc
> {
>     "bookmarked": true,                  // Filter for bookmarked logs if true
>     "groups": ["greenhouse", "outside"], // Filter by device groups
>     "devices": ["tomatoes", "kale"],     // Filter by specific devices
>     
>     "startTime": "2024-01-15T07:00:00Z", // Start of time range
>     "endTime": "2024-01-15T11:30:00Z",   // End of time range
>     // or
>     "id": 41231,                         // Reference log ID for pagination
>     "count": -10                         // Number of logs to fetch, negative = older, positive = newer
> }
> ```

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "logs": [
>         {
>             "id": 12345,                         // Log ID. Can be used for next pagination
>             "timestamp": "2024-01-15T10:30:00Z", // Timestamp the log was created
>             "device": "tomatoes",                // Device the log originated from
>             "group": "greenhouse",               // Group that the device belongs to
>             "message": "Log message content",    // Log content
>             "level": "info"                      // Log level
>         }
>     ],
>     "newerAvailable": true,                      // True if new logs are available
>     "olderAvailable": false                      // True if older logs are available
> }
> ```

---

#### Delete a single log

---

## Data

---

## Agent

