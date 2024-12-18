# Logic map

The logic map is a python script that transforms sensors data into actions.

Here's how it works:
- Read uplink of a device on TTN
- Apply some business rules to determine actions to do
- Sends these actions as payload on the downlink topic of the device waiting these actions

## Rules

Below are defined the rules for the logic map.

1. If __brightness > 200__, then lights up __tree star__ AND __village LEDs__
2. If __brightness < 200__, then turn off __tree star__ AND __village LEDs__
3. If __temperature >= 25__, display the message __"Too hot !"__ on the LCD screen 
4. If __temperature <= 20__, display the message __"Freezing cold !"__ on the LCD screen

These rules are defined in [logic_map.py](src/pyxmas/logic_map.py), in the method `_map()` of the `LogicMap` class.