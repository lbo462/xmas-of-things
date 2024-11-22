# City Town Hall Documentation

## Overview
This document outlines the data requirements for the Christmas city engines, lights, speakers and every other actionable.\
For detail task information and status we made a [Trello](https://trello.com/b/3zekwBi3/iot-central-hall).

## Actions

### Lights
- **Christmas Tree**
  - Lights up when it’s dark in the room (uses brightness sensor).
- **Star on Christmas Tree**
  - Lights up based on the Christmas tree’s logic or when Santa is nearby (proximity sensor).
- **Village Lights**
  - Blink in response to clapping or noise above a certain threshold.
- **LEDs on Santa’s Track**
  - Light up when Santa is detected as approaching.

### Engines
- **Santa Claus**
  - Motorized movement for Santa’s sleigh.
- **Christmas Tree**
  - Rotates for a dynamic effect.
- **Ferris Wheel**
  - Spins as part of the village decoration.
- **Snow Spray**
  - Activates when the temperature falls below a defined value.

### Speakers
- **City Song**
  - Plays a default Christmas tune when Santa arrives.
  - Optional: Select specific songs or upload custom tracks via the website.
  - Triggers based on actions (e.g., Santa's arrival).

### Display
- **City Billboard**
  - Displays messages when Santa arrives or based on custom input from the website.
  - Supports festive or user-defined text.

## Data Requirements

### Input Data
- **Billboard Message**
  - Custom text from the web interface.
- **Song Selection**
  - Default, action-specific, or custom songs.
- **Control Commands**
  - On/Off states for lights, Christmas tree movement, and ferris wheel.

### Sensor Data
- **Noise Level**
  - Determines if village lights should blink.
- **Brightness Level**
  - Controls Christmas tree and star lights.
- **Temperature Level**
  - Triggers the snow spray engine.
- **Santa’s Presence**
  - Activates lights, songs, and billboard messages.

## Things we need to buy
- Screen 
- Snow spray
- LEDs