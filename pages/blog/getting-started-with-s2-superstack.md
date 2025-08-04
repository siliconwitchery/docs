---
title: "Getting Started with S2 & Superstack"
parent: IoT Business Solutions Blog
nav_order: 1
---

# **Getting Started with the S2 Module and Superstack**

Rohit Nareshkumar, Solutions Architect & Embedded Applications Engineer \| July 24, 2025
{: .float-left .fs-2 }

---

The [S2 Module and Superstack platform](https://www.siliconwitchery.com/s2-superstack) streamlines deployment, management, and scaling of IoT sensing systems. It provides a unified environment for onboarding devices, managing code, and analyzing data. 

> Superstack is designed for both newcomers to the IoT realm and experienced developers. It allows you to quickly get up and running without the hassle of building complex infrastructure, databases, or device firmware.

---

### Step 1: Unbox your new S2 Module

The S2 Module is available from DigiKey, with many orders often qualifying for free local and international shipping.

Begin by powering your S2 Module using a 5V USB-C power supply. For alternative power options such as Lithium batteries, check the [detailed documentation](/pages/s2-module#power--battery-interface).

![S2 Module being powered from USB-C](/assets/images/blog/getting-started-with-s2-superstack-s2-power-input.jpg)

### Step 2: Create a Superstack account

Navigate to [super.siliconwitchery.com](https://super.siliconwitchery.com) and click the **account** icon in the top right corner:

![Agent tab showing the location of account button](/assets/images/blog/getting-started-with-s2-superstack-account-button.png)

From the account pane, click **Sign up**, or **Sign in**:

![Account modal with sign-up and sign-in buttons](/assets/images/blog/getting-started-with-s2-superstack-account-modal.png)

Log in securely using OAuth with **Github** or **Google**:

> Superstack does not gain access to any sensitive customer information, passwords, or access tokens. Only your email is used to reference your account.

![Sign-in with Github or Google](/assets/images/blog/getting-started-with-s2-superstack-sign-in.png)

### Step 3: Create a new deployment

Click the **deployment name** in the top bar to open the deployment selection menu:

![Agent tab showing the current deployment button](/assets/images/blog/getting-started-with-s2-superstack-deployments-button.png)

Click on **New deployment**:

![Deployments modal showing the add deployment button](/assets/images/blog/getting-started-with-s2-superstack-step-add-deployment.png)

An empty deployment will be created:

> You can edit the name and description from the **Settings Tab**, as well as add additional users if desired.

![Settings tab showing deployment settings](/assets/images/blog/getting-started-with-s2-superstack-edit-deployment.png)

### Step 4: Adding Devices

To add your S2 Module, navigate to the **Devices** tab and click **Add device**:

![Devices tab](/assets/images/blog/getting-started-with-s2-superstack-devices-tab.png)

Enter the IMEI of your device and optionally assign a name for easy reference. 

Then wait for the **net** LED on the S2 Module to go solid, and then click **Add device**:

{: .note }
If the **net** LED does not go solid after 5 minutes of being powered on, try to relocate the device for better cell coverage, and then re-power the device.

![Add device modal](/assets/images/blog/getting-started-with-s2-superstack-add-device.png)

Superstack will then direct you to press the button to complete pairing. **Click the button** on the S2 Module to connect:

![Pairing the S2 Module via the button](/assets/images/blog/getting-started-with-s2-superstack-s2-clicking-button.jpg)

The paired module will then be shown in the **Devices** tab:

![Devices tab showing the new device](/assets/images/blog/getting-started-with-s2-superstack-added-to-deployment.png)

### Step 5: Edit the Code

Navigate to the **Code** tab to access the code editor. 

> A complete [API reference](/pages/superstack/) is available for accessing the hardware features of the S2 Module.

The S2 Module runs Lua and is easily reprogrammable with a single click while the device has cellular connection. If the device loses connection for any reason or is powered off, it will automatically download the latest code on re-connection and run it right away.

> Lua is an extremely small, efficient, and stable scripting language that has been around for over 30 years. It runs incredibly well on the modern ARM Cortex-M33 processor of the S2 Module, and allows for a workflow where changing and rerunning code takes a matter of seconds. No compilation or programming tools required.

Paste the following code and click the **save icon**:

```lua
print("My first S2 Lua app")

while true do
    print("Generating a random number between 15 and 30")
    local r = math.random(15, 30)
    
    print("Sending data to Superstack")
    network.send_data{ number=r }
    
    print("Sleeping")
    device.sleep(60)
end
```

![Code tab showing the sample script and logs](/assets/images/blog/getting-started-with-s2-superstack-code-tab.png)

This code generates a random number between 15 and 30 every minute and sends the value to Superstack. Anything logged with a `print()` statement will be visible at the bottom of the page (as well as from the **Logs** tab), and data will be shown on the **Data** tab:

![Data tab showing the returned data](/assets/images/blog/getting-started-with-s2-superstack-data-tab.png)

### Step 6: Analyze data using the AI Agent

Superstack features an advanced AI data agent that can perform deep analysis on aggregated sensor data. Navigate to the **Devices** tab and click on the device we just added:

![Devices tab showing the selectable device](/assets/images/blog/getting-started-with-s2-superstack-selectable-device.png)

Edit the **Device Role** to give the AI agent better context of what the device is intending to monitor or process:

![Editing device details](/assets/images/blog/getting-started-with-s2-superstack-edit-device.png)

Next, navigate to the **Agent** tab and edit the **Agent Role** to tell the agent about the intentions of the overall deployment:

![Editing AI Agent role](/assets/images/blog/getting-started-with-s2-superstack-agent-role.png)

Finally, ask the agent a question about your data:

![Querying the AI Agent around the data](/assets/images/blog/getting-started-with-s2-superstack-agent-usage.png)

As you begin to gather more data from multiple devices, the agentic capabilities will help extract deeper insights and patterns as picked up by your sensors. To learn more about how the agent can be used with real sensors, check out our article on [Easy Air Quality Monitoring](/pages/blog/easy-air-quality-monitoring-with-superstack).

---

## Learn More

- [Product page](https://www.siliconwitchery.com/s2-superstack)
- [Superstack API reference and documentation](/pages/superstack/)
- [S2 Module hardware manual](/pages/s2-module)

## Need Assistance?

For support or questions, [email our engineering team](mailto:projects@siliconwitchery.com?subject=IoT Project Support - Superstack&amp;body=Hi Silicon Witchery team,%0D%0A%0D%0AI'm interested in implementation support for:%0D%0A%0D%0A- Project type:%0D%0A- Timeline:%0D%0A- Company:%0D%0A%0D%0ABest regards,) for a free consultation.