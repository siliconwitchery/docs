---
title: "Getting Started with the S2-Superstack"
parent: Blog
nav_order: 1
carousels:
  - images: 
    - image: /assets/images/blog/getting-started-with-s2-superstack-agent-tab.png
      description: "Interact with your device data and insights using the agent interface."
    - image: /assets/images/blog/getting-started-with-s2-superstack-devices-tab.png
      description: "Monitor device status and seamlessly onboard new devices to your deployment."
    - image: /assets/images/blog/getting-started-with-s2-superstack-code-tab.png
      description: "Develop, edit, and deploy Lua scripts directly from the integrated web editor."
    - image: /assets/images/blog/getting-started-with-s2-superstack-data-tab.png
      description: "Access and analyze real-time data streams from your connected devices."
    - image: /assets/images/blog/getting-started-with-s2-superstack-logs-tab.png
      description: "Review and filter device logs efficiently with live updates."
    - image: /assets/images/blog/getting-started-with-s2-superstack-settings-tab.png
      description: "Configure deployments and manage platform settings with ease."
    - image: /assets/images/blog/getting-started-with-s2-superstack-signin-page.png
      description: "Sign in securely using your Google or GitHub account for instant access."
---

# **Getting Started with the S2-Superstack**

Rohit N, Embedded Engineer \| 24 July 2025
{: .float-left	.fs-2 }
---
The [S2 Superstack](https://www.siliconwitchery.com/s2-superstack) platform streamlines the deployment, management, and scaling of IoT and embedded systems. It offers a unified environment for onboarding devices, configuring deployments, managing code, and analyzing data. Designed for both newcomers and experienced developers, Superstack integrates device management, data collection, and analytics through an intuitive agent interface.

<div style="text-align: center;"><iframe width="640" height="360" src="https://www.youtube.com/embed/3L_OU-fMW_w" frameborder="0" allowfullscreen></iframe></div>

---

## Platform Overview

{% include vstack-carousel.html height="100" unit="%" number="1" %}

---

## Managing Deployments and Devices

### Creating a Deployment

- Click the current deployment name in the top bar.
- Click the `+` button to create a new deployment.
- To edit deployment settings, go to the [Settings tab](#platform-overview){:data-carousel-target="0f"}.

### Adding Devices

- Open the [Devices tab](#platform-overview){:data-carousel-target="0b"} and click `Add device`.
- Enter the device IMEI and confirm.
- Power on the module. When the LED is solid, press the pair button to complete setup.
- Detailed information available in the [documentation]({{ site.baseurl }}/pages/superstack/#connecting-your-first-module) page.

### Removing Devices or Deployments

- To remove a device, select it in the [Devices tab](#platform-overview){:data-carousel-target="0b"} and click `remove device`. This only removes it from the deployment; data remains intact. Re-adding requires physical access to the device.
- To delete a deployment, go to the [Settings tab](#platform-overview){:data-carousel-target="0f"} and click `delete deployment`. **Warning:** This deletes all associated data and resets all devices in the deployment.

---

## Deploying and Managing Code

- Go to the [Code tab](#platform-overview){:data-carousel-target="0c"} to access the web editor and [Lua API]({{ site.baseurl }}/pages/superstack/).
- Select the target device at the top left. Click `save` to upload your Lua script, or use `upload` to push code to multiple devices.
- Control device execution with `stop` and `restart` as needed.
- View real-time logs from `print()` statements in the lower section.
- Persist data by saving Lua tables with [`network.send{ }`]({{ site.baseurl }}/pages/superstack/#networking-lte). Device IMEI and timestamps are automatically included.

---

## Data Access and Analysis

### Using the Agent Interface

- In the [Agent tab](#platform-overview){:data-carousel-target="0a"}, enter queries in the chat box. The agent retrieves, filters, and analyzes data, returning concise summaries.
- See the [documentation]({{ site.baseurl }}/pages/superstack/#ai-agent) for technical details.

### Data API Integration

- Generate an API key in the [Settings tab](#platform-overview){:data-carousel-target="0f"} to access the data API.
- The API supports reading, deleting device data, and programmatic agent queries. Refer to the [documentation]({{ site.baseurl }}/pages/superstack/#data-api) for usage examples.

---

## Pricing

Choose the plan that fits your requirements:

|                         | Starter | Maker | Professional | Enterprise |
| :---------------------- | :-----: | :---: | :----------: | :--------: |
| **Max Devices**         |    2    |  10   |     100      | 1,000,000  |
| **Data Allowance (MB)** |    2    |  10   |     100      |   1,000    |
| **AI Tokens**           |  1000   | 1000  |     1000     |   1,000    |
| **Price (USD/month)**   |    0    |  15   |     500      |   2,500    |

---

## Learn More

- [Product page](https://www.siliconwitchery.com/s2-superstack)
- [Documentation]({{ site.baseurl }}/pages/superstack/)

## Need Assistance?

For support or questions, [email our engineering team](mailto:projects@siliconwitchery.com?subject=IoT Project Support - Superstack&amp;body=Hi Silicon Witchery team,%0D%0A%0D%0AI'm interested in implementation support for:%0D%0A%0D%0A- Project type:%0D%0A- Timeline:%0D%0A- Company:%0D%0A%0D%0ABest regards,) for a free consultation.