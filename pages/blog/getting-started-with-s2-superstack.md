---
title: "Getting Started with S2 & Superstack"
parent: IoT Business Solutions Blog
nav_order: 1
---

# **Getting Started with the S2 Module and Superstack**

Rohit Nareshkumar, Solutions Architect & Embedded Applications Engineer \| 24 July 2025
{: .float-left	.fs-2 }
---
The [S2 Superstack](https://www.siliconwitchery.com/s2-superstack) platform streamlines the deployment, management, and scaling of IoT and embedded systems. It provides a unified environment for onboarding devices, configuring deployments, managing code, and analyzing data. Designed for both newcomers and experienced developers, Superstack integrates device management, data collection, and analytics through an intuitive agent interface.

<div style="text-align: center;"><iframe width="640" height="360" src="https://www.youtube.com/embed/3L_OU-fMW_w" frameborder="0" allowfullscreen></iframe></div>

---

### Step 1: Creating an Account

Click the account icon in the top right corner.
![Agent tab showing the location of account button](/assets/images/blog/getting-started-with-s2-superstack-account-button.png)

In the modal, choose to sign up for a new account or sign in to an existing one.
![Account modal with sign-up and sign-in buttons](/assets/images/blog/getting-started-with-s2-superstack-account-modal.png)

Authenticate using Github or Google OAuth.
![Sign-in with Github or Google](/assets/images/blog/getting-started-with-s2-superstack-sign-in.png)

### Step 2: Creating a Deployment

Click the current deployment name in the top bar to open the deployments menu.
![Agent tab showing the current deployment button](/assets/images/blog/getting-started-with-s2-superstack-deployments-button.png)

Click the `+` button to create a new deployment.
![Deployments modal showing the add deployment button](/assets/images/blog/getting-started-with-s2-superstack-step-add-deployment.png)

A new default deployment will be created. To edit its details, go to the Settings Tab.
![Settings tab showing deployment settings](/assets/images/blog/getting-started-with-s2-superstack-new-deployment.png)

Here, you can change the name and description of your deployment for easier identification.
![Settings tab showing deployment settings](/assets/images/blog/getting-started-with-s2-superstack-edit-deployment.png)

### Step 3: Adding Devices

Open the Devices tab and click `Add device`.
![Devices tab](/assets/images/blog/getting-started-with-s2-superstack-devices-tab.png)

Enter the IMEI of your device and optionally assign a name for easy reference.
![Add device modal](/assets/images/blog/getting-started-with-s2-superstack-add-device.png)

Power on the module. When the LED is solid, press the pair button to complete setup. For more details, refer to the [documentation](/pages/superstack/#connecting-your-first-module).

![Devices tab showing the new device](/assets/images/blog/getting-started-with-s2-superstack-added-to-deployment.png)

### Step 4: Deploy Code

Go to the Code tab to access the web editor. Refer to [Lua API](/pages/superstack/) for details.

Start with a simple "hello world" program. Paste this into your code editor to try it out:
```lua
print("hello world!")
while true
do
    device.sleep(3)
    print("hi again!")
end
```

Select the target device at the top left. Click `save` to upload your Lua script, or use `upload` to push code to multiple devices.

You can control device execution with `stop` and `restart` as needed.

View real-time logs from `print()` statements in the lower section of the editor.
![Code tab showing the sample script and logs](/assets/images/blog/getting-started-with-s2-superstack-code-tab.png)

---

## Learn More

- [Product page](https://www.siliconwitchery.com/s2-superstack)
- [Documentation](/pages/superstack/)

## Need Assistance?

For support or questions, [email our engineering team](mailto:projects@siliconwitchery.com?subject=IoT Project Support - Superstack&amp;body=Hi Silicon Witchery team,%0D%0A%0D%0AI'm interested in implementation support for:%0D%0A%0D%0A- Project type:%0D%0A- Timeline:%0D%0A- Company:%0D%0A%0D%0ABest regards,) for a free consultation.