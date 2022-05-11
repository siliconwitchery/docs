---
title: machine.PMIC
description: PMIC class
image: images/s1-micropython.png
nav_order: 7
parent: MicroPython
last_modified_date: May 10th 2022, 06:27 PM
---

# `machine.PMIC` – Functions to control the power management IC

---

The `machine.PMIC` class contains all of the functions to configure the S1 voltage rails, and configure the battery charger. Import it with

```python
from machine import PMIC
```

To see what's contained inside the class you can use the `help()` command

```python
help(PMIC)
```

---

## Functions

`PMIC.charge_config(v, i)`

- Configures the battery charger. If no arguments are given, the current setting is printed as a *tuple*

- If voltage, and/or current arguments are provided, the values will be set accordingly

- Voltage `v` can be set between 3.6V and 4.3V (in 50mV steps)

- Current `i` can be set between 7.5mA and 300mA (in 7.5mA steps). **Note** Value should be written as a *float* in mA, not A

    ```python
    PMIC.charge_config(v=4.21, i=100)

    PMIC.charge_config() # Read the set parameters
    # Note the difference due to the resolution that can be set
    (4.2, 97.5) 
    ```

`PMIC.battery_level(enable)`

- Displays the current battery voltage as a *float*

- Before reading the value, the voltage monitoring must be enabled

    ```python
    PMIC.battery_level(True) # Enable monitoring
    PMIC.battery_level() # Read the battery level
    3.46

    PMIC.battery_level(False) # The monitoring can be disabled to save a small amount of power if not needed
    ```

`PMIC.fpga_power(enable)`

- Enables or disables the FPGA core power rail

- Setting this to `False` will automatically disable the Vio rail to avoid damaging the FPGA. Vio will need to be reconfigured manually after reenabling the FPGA core power rail

    ```python
    PMIC.fpga_power() # Read the current state of the rail
    True

    PMIC.fpga_power(False) # Shuts down the FPGA core power rail

    PMIC.vio_config() # Read the Vio rail value
    # Will be set to 0V whenever the FPGA is shut down
    0

    PMIC.fpga_power(True) # Power on the FPGA again
    PMIC.vio_config(1.8) # You'll need to set the Vio rail again
    ```

`PMIC.vaux_config(voltage)`

- Configures the buck-boost convertor of the Vaux rail

- If no arguments are given, the current setting will be printed as a *float*

- Can be set to 0V which turns off the rail, or between 0.8V and 5.5V

    ```python
    PMIC.vaux_config(3.3) # Set the Vaux rail to 3.3V

    # Read the current setting
    PMIC.vaux_config()
    3.3
    ```

- If Vio is set to be in load switch mode, the Vaux rail will be limited to 3.45V

`PMIC.vio_config(voltage, lsw=False)`

- Configures the FPGA IO rail voltage, either in LDO mode, or load switch mode

- If no arguments are given, the current setting will be printed

    - If Vio is configured as an LDO, the voltage setting will be returned as a *float*

    - If Vio is configured as a load switch, the state will be returned as a *string*. Either `LOAD_SWITCH_ON` or `LOAD_SWITCH_OFF`

- Can be set to 0V which turns off the rail, regardless of the mode

    ```python
    PMIC.vio_config(0) # Shuts down the rail
    ```

- Can be set between 0.8V or 3.45V in LDO mode

    ```python
    PMIC.vio_config(3.3, lsw=False) # Set Vio to regulate 3.3V in LDO mode

    PMIC.vio_config(3.3) # The same as above. lsw=False by default
    ```

- Vio can also be configured as a load switch. In this mode the Vaux voltage is passed through directly to Vio. In this case, Vaux must not exceed 3.45V

    ```python
    PMIC.vio_config(True, lsw=True) # Turn on the load switch (pass Vaux to Vio)
    
    PMIC.vio_config(False, lsw=True) # Turn off the load switch
    ```