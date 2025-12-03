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

The **Deployment ID** is required for accessing all data within a deployment. This ID can be found on the **Settings Tab**:

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

#### Retrieve deployment info

```
GET https://super.siliconwitchery.com/api/{deploymentId}/info
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read deployment info** permission

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "created": "2024-10-28T10:30:00Z",                                   // When deployment was created
>     "name": "Greenhouse Demo",                                           // Deployment name
>     "description": "A plant growth monitoring system for a greenhouse",  // Deployment description
>     "plan": "Professional",                                              // Current subscription plan
>     "public": true                                                       // Deployment visibility
> }
> ```

---

#### Update deployment info

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/info
```

{: .note-title }
> Authentication & Permissions
> - API key is required
> - API key requires **write deployment info** permission

{: .note-title }
> Request body
> ```jsonc
> {
>     "name": "Greenhouse Demo",                                          // Max 50 characters, cannot be blank
>     "description": "A plant growth monitoring system for a greenhouse"  // Max 300 characters
> }
> ```

{: .note-title }
> Response (200 OK)
> 

---

## Devices

#### Retrieve all devices

```
GET https://super.siliconwitchery.com/api/{deploymentId}/devices
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "devices": [
>         {
>             "id": 1,                              // Device ID
>             "name": "Tomatoes",                   // Device friendly name
>             "group": "greenhouse",                // Group the device belongs to
>             "bookmarked": false,                  // True if device is bookmarked
>             "online": true,                       // True if device is currently online
>             "codeState": "running",               // Code state: "running", "stopped", "error"
>             "bytesUp": 12345,                     // Bytes sent since billing period
>             "bytesDown": 67890,                   // Bytes received since billing period
>             "powerState": "battery",              // Power state: "battery", "charging", "usb"
>             "batteryLevel": 85,                   // Battery level percentage
>             "signalStrength": 75,                 // Signal strength percentage
>             "gpsCoordinates": "51.5074,-0.1278"   // GPS coordinates (latitude,longitude)
>         }
>     ]
> }
> ```

---

#### Retrieve device groups

```
GET https://super.siliconwitchery.com/api/{deploymentId}/devices/groups
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "groups": ["greenhouse", "outside"]  // List of all device groups in the deployment
> }
> ```

---

#### Retrieve online device history

```
GET https://super.siliconwitchery.com/api/{deploymentId}/devices/online?days=
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Optional query parameters
> - `days` - **integer** - Number of days of history to retrieve

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "allowance": 100,                           // Maximum devices allowed by plan
>     "devices": {
>         "2024-01-15T00:00:00Z": {
>             "total": 10,                        // Total number of devices at this time
>             "online": 8                         // Number of online devices at this time
>         },
>         "2024-01-16T00:00:00Z": {
>             "total": 10,
>             "online": 9
>         }
>     }
> }
> ```

---

#### Retrieve data usage

```
GET https://super.siliconwitchery.com/api/{deploymentId}/devices/usage?days=
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Optional query parameters
> - `days` - **integer** - Number of days of history to retrieve

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "allowance": 500000000,                     // Data allowance in bytes for billing period
>     "billingDay": 23,                           // Day of month when billing period resets
>     "sent": 123456,                             // Total bytes sent in billing period
>     "received": 234567,                         // Total bytes received in billing period
>     "total": 358023,                            // Total bytes (sent + received)
>     "usage": {
>         "2024-01-15T00:00:00Z": {
>             "sent": 12345,                      // Bytes sent on this day
>             "received": 23456,                  // Bytes received on this day
>             "total": 35801                      // Total bytes on this day
>         }
>     }
> }
> ```

---

#### Retrieve device locations

```
GET https://super.siliconwitchery.com/api/{deploymentId}/devices/location
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "locations": [
>         {
>             "deviceId": 1,                      // Device ID
>             "latitude": 51.5074,                // Latitude coordinate
>             "longitude": -0.1278                // Longitude coordinate
>         }
>     ]
> }
> ```

---

#### Retrieve device info

```
GET https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/info
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "id": 1,                                    // Device ID
>     "imei": "578949671258131",                  // Device IMEI
>     "model": "sw-demo-device",                  // Hardware model
>     "added": "2024-01-15T10:30:00Z",            // Timestamp when device was added
>     "name": "Tomatoes",                         // Device friendly name
>     "group": "greenhouse",                      // Group the device belongs to
>     "bookmarked": false,                        // True if device is bookmarked
>     "role": "I monitor Roma tomato plants...",  // AI role description
>     "online": true,                             // True if device is currently online
>     "uptime": 24681,                            // Device uptime in seconds
>     "codeState": "running",                     // Code state: "running", "stopped", "error"
>     "firmwareVersion": "1.0.0",                 // Current firmware version
>     "storageUsed": 47293,                       // Storage used in bytes
>     "storageTotal": 1048576,                    // Total storage in bytes
>     "bytesUp": 12345,                           // Bytes sent since billing period
>     "bytesDown": 67890,                         // Bytes received since billing period
>     "powerState": "battery",                    // Power state: "battery", "charging", "usb"
>     "batteryLevel": 85,                         // Battery level percentage 
>     "signalStrength": 75,                       // Signal strength percentage
>     "gpsCoordinates": "51.5074,-0.1278"         // GPS coordinates (latitude,longitude)
> }
> ```

---

#### Update device info

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/info
```

{: .note-title }
> Authentication & Permissions
> - API key is required
> - API key requires **write devices info** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Request body
> ```jsonc
> {
>     "name": "Tomatoes",           // Device friendly name (max 50 characters)
>     "group": "greenhouse",        // Group the device belongs to (max 50 characters)
>     "bookmarked": false,          // True to bookmark the device
>     "role": "I monitor tomatoes"  // AI role description (max 2000 characters)
> }
> ```

{: .note-title }
> Response (200 OK)
>

---

#### Retrieve device telemetry

```
GET https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/telemetry?days=
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read devices info** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Optional query parameters
> - `days` - **integer** - Number of days of history to retrieve

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "telemetry": {
>         "2024-01-15T10:30:00Z": {
>             "bytesSent": 1234,                  // Bytes sent at this time
>             "bytesReceived": 5678,              // Bytes received at this time
>             "bytesTotal": 6912,                 // Total bytes at this time
>             "powerState": "battery",            // Power state at this time
>             "batteryLevel": 85,                 // Battery level percentage at this time
>             "signalStrength": 75 ,              // Signal strength at percentage this time
>             "gpsCoordinates": "51.5074,-0.1278" // GPS coordinates at this time
>         }
>     }
> }
> ```

---

#### Add device to deployment

```
POST https://super.siliconwitchery.com/api/{deploymentId}/device
```

{: .note-title }
> Authentication & Permissions
> - API key is required
> - API key requires **add devices** permission

{: .note-title }
> Request body
> ```jsonc
> {
>     "imei": "578949671258131",    // Device IMEI (required)
>     "name": "Tomatoes",           // Device friendly name (max 50 characters)
>     "group": "greenhouse",        // Group the device belongs to (max 50 characters)
>     "role": "I monitor tomatoes", // AI role description (max 2000 characters)
>     "bookmarked": false           // True to bookmark the device
> }
> ```

{: .warning-title }
API will wait up to 60 seconds for the button to be clicked on the device

{: .note-title }
> Response (200 OK)
>

---

#### Remove device from deployment

```
DELETE https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}
```

{: .note-title }
> Authentication & Permissions
> - API key is required
> - API key requires **delete devices** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Request body
> ```jsonc
> {
>     "confirm": true  // Must be true to confirm deletion
> }
> ```

{: .note-title }
> Response (200 OK)
>

---

## Code

#### Retrieve device code

```
GET https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/code
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read code** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "code": "-- Monitors temperature, light and soil moisture..."  // Lua code
> }
> ```

---

#### Update device code

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/code
```

{: .note-title }
> Authentication & Permissions
> - API key requires **write code** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Request body
> ```jsonc
> {
>     "code": "-- Your Lua code here..."  // Lua code (max 100,000 characters)
> }
> ```

{: .note-title }
> Response (200 OK)
>

---

#### Stop device code

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/code/stop
```

{: .note-title }

> Authentication & Permissions
> - API key requires **write code** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Response (200 OK)
>

---

#### Start device code

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/device/{deviceId}/code/start
```

{: .note-title }
> Authentication & Permissions
> - API key requires **write code** permission

{: .note-title }
> Path parameters
> - `deviceId` - **integer** - ID of the device

{: .note-title }
> Response (200 OK)
>

---

#### Push code to devices

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/code/push
```

{: .note-title }
> Authentication & Permissions
> - API key requires **write code** permission

{: .note-title }
> Request body
> ```jsonc
> {
>     "code": "-- Your Lua code here...",      // Lua code (max 100,000 characters)
>     "groups": ["greenhouse", "outside"],     // Groups to push code to
>     "devices": ["Tomatoes", "Kale"]          // Specific devices to push code to
> }

> ```
> Note: At least one of `groups` or `devices` must be specified

{: .note-title }
> Response (200 OK)
>

---

## Logs

#### Retrieve logs

```
GET https://super.siliconwitchery.com/api/{deploymentId}/logs?filters=
```

{: .note-title }
> Authentication & Permissions
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
>             "id": 12345,                         // Log ID. Can be used for pagination or deletion
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

#### Delete a log

```
DELETE https://super.siliconwitchery.com/api/{deploymentId}/log/{logId}
```

{: .note-title }
> Authentication & Permissions
> - API key requires **delete logs** permission

{: .note-title }
> Path parameters
> - `logId` - **integer** - The ID of the log to delete

{: .note-title }
> Request body
> ```jsonc
> {
>     "confirm": true // Must be true to confirm deletion
> }
> ```

{: .note-title }
> Response (200 OK)
> 

---

## Data

#### Retrieve data

```
GET https://super.siliconwitchery.com/api/{deploymentId}/data?filters=
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read data** permission

{: .note-title }
> Optional query parameters
> - `filters` - **json string** - JSON-encoded filter object
> ```jsonc
> {
>     "bookmarked": true,                  // Filter for bookmarked data if true
>     "groups": ["greenhouse", "outside"], // Filter by device groups
>     "devices": ["Tomatoes", "Kale"],     // Filter by specific devices
>     
>     "startTime": "2024-01-15T07:00:00Z", // Start of time range
>     "endTime": "2024-01-15T11:30:00Z",   // End of time range
>     // or
>     "id": 41231,                         // Reference data ID for pagination
>     "count": -10                         // Number of data entries to fetch, negative = older, positive = newer
> }
> ```

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "data": [
>         {
>             "id": 12345,                         // Data ID. Can be used for pagination or deletion
>             "timestamp": "2024-01-15T10:30:00Z", // Timestamp the data was created
>             "device": "Tomatoes",                // Device the data originated from
>             "group": "greenhouse",               // Group that the device belongs to
>             "data": {                            // JSON data payload from the device
>                 "temperature": 23.5,
>                 "light": 850,
>                 "moisure": 45.2
>             }
>         }
>     ],
>     "newerAvailable": true,                      // True if new data is available
>     "olderAvailable": false                      // True if older data is available
> }
> ```

---

#### Delete a data entry

```
DELETE https://super.siliconwitchery.com/api/{deploymentId}/data/{dataId}
```

{: .note-title }
> Authentication & Permissions
> - API key requires **delete data** permission

{: .note-title }
> Path parameters
> - `dataId` - **integer** - The ID of the data entry to delete

{: .note-title }
> Request body
> ```jsonc
> {
>     "confirm": true // Must be true to confirm deletion
> }
> ```

{: .note-title }
> Response (200 OK)
> 

---

## Agent

#### Retrieve agent role

```
GET https://super.siliconwitchery.com/api/{deploymentId}/agent/role
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **read agent role** permission

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "role": "You are an expert gardener. You are responsible for ensuring optimal growth of herbs and vegetables in a greenhouse."
> }
> ```

---

#### Update agent role

```
PUT https://super.siliconwitchery.com/api/{deploymentId}/agent/role
```

{: .note-title }
> Authentication & Permissions
> - API key requires **write agent role** permission

{: .note-title }
> Request body
> ```jsonc
> {
>     "role": "You are an expert gardener. You are responsible for ensuring optimal growth of herbs and vegetables in a greenhouse."
> }
> ```

{: .note-title }
> Response (200 OK)
> 

---

#### Retrieve agent usage

```
GET https://super.siliconwitchery.com/api/{deploymentId}/agent/usage?days=
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **agent usage** permission

{: .note-title }
> Optional query parameters
> - `days` - **integer** - Number of days of usage history to retrieve

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "allowance": 50000,                          // Total token allowance for the billing period
>     "used": 12500,                               // Tokens used in the current billing period
>     "remaining": 37500,                          // Tokens remaining in the current billing period
>     "billingDay": 23,                            // Day of month when billing resets
>     "usage": {                                   // Daily usage breakdown
>         "2024-01-15T00:00:00Z": {
>             "usage": 2500                        // Tokens used on this day
>         },
>         "2024-01-14T00:00:00Z": {
>             "usage": 3200
>         }
>     }
> }
> ```

---

#### Chat with agent

```
POST https://super.siliconwitchery.com/api/{deploymentId}/agent/chat
```

{: .note-title }
> Authentication & Permissions
> - API key is not required if the deployment is public
> - API key requires **agent chat** permission

{: .note-title }
> Request body
> ```jsonc
> {
>     "messages": [
>         {
>             "role": "user",
>             "content": "What is the average temperature in the greenhouse?"
>         }
>     ]
> }
> ```

{: .note-title }
> Response (200 OK)
> ```jsonc
> {
>     "messages": [
>         {
>             "role": "user",                      // Original user message
>             "content": "What is the average temperature in the greenhouse?"
>         },
>         {
>             "role": "assistant",                 // Agent response
>             "content": "The average temperature in the greenhouse is currently 23.5°C. The Tomatoes sensor is reading 24.1°C and the Rosemary & basil sensor is reading 22.9°C.",
>             "answer": "23.5",                    // Raw computed answer
>             "reasoning": {                       // Internal reasoning (for debugging)
>                 "filter": "Filtered to greenhouse devices from the last 6 hours",
>                 "analysis": "Calculated mean temperature from all greenhouse sensors"
>             }
>         }
>     ]
> }
> ```
