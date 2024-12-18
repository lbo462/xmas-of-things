# Getting started

The project was divided into several teams, a described in the README.
For each team, here's what needs to be set-up to build the project:

## SEN (Sensors)

### Requirements

A single MKRWAN board plugged with:
- A LoRa antenna
- A photoreceptor
- A temperature sensor

Pins wiring is described in [SEN/README.md](SEN/README.md).

### Setup

1. On TTN, create the device with the Device EUI of the picked board.

2. Copy-paste the program given in [SEN/README.md](SEN/README.md) into the board, but replace with the correct APP_EUI and APP_KEY variables.

3. On TTN, change the uplink payload decoder for the end device with the one given in [TTN/README.md](TTN/README.md).

### Verification

On TTN live data for the end device should appear real time sensor data, as described in the TTN documentation.

## API (Dashboard)

### Requirements

Any sort of computer able to run Python 3.10.

### Setup

Check [API/README.md](API/README.md).

### Verification

The dashboard should be accessible from the browser, and should read the sensors datas.

For now, no actions can be sent as engines are not setup yet.

_Note :_ The name given to the sensor device on TTN discussed earlier should match the one in [API/src/pyxmas/topics.py](API/src/pyxmas/topics.py) (`device_id` of `sensors_topic`).

## CTH (Actual engines)

### Requirements

- 4 MKRWAN boards with LoRa antennas
- 1 regular UNO board
- 2 servos
- 1 RGB LED and 4 single colored LEDs
- 3 buzzers
- 1 LCD screen
- a bunch of cables

### Setup

For each of the MKRWAN boards, one should create the device on TTN, as did previously for the sensors.

The downlink encoder of each of these devices should match the one in [TTN/README.md](TTN/README.md).

The setups and wiring are described in [CTH/README.md](CTH/README.md)

### Verification

Every MKRWAN board should periodically send probes to TTN live data.

_Note :_ Same as before, the device names on TTN should match the `device_id` in the topics of [API/src/pyxmas/topics.py](API/src/pyxmas/topics.py).

The engines should respond to the downlink sent on their topic, either using TTN scheduler, or the API Dashboard.

# Overall verification

These verification are sorted.
If one fail, all the others below will too.

1. The sensor MKRWAN board should periodically send data to TTN, and is correctly displayed on live data.
2. The API dashboard should read correctly these sensors values and display real-time graphs.
3. Sending actions with the dashboard should schedule visible downlink on the CTH MKRWAN boards topics (TTN live data).
4. When a downlink is scheduled on any CTH topic, the corresponding device should react accordingly.
5. On top of that, when activated through the API dashboard, the logic map should automatically send actions.