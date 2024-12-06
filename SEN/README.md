# Sensors Documentation

## General discussion
The objective of the sensors team is to read data from multiple sensors and send this to TTN.

Below is a simple script that read the value of temperature and humidity and send both to TTN.

This script requires:
- [MKRWAN](https://downloads.arduino.cc/libraries/github.com/arduino-libraries/MKRWAN-1.1.0.zip)
- [DHT](https://perso.citi.insa-lyon.fr/oiova/docs/arduino-DHT-master.zip)

To respect TTN standards, please check the [TTN documentation](../TTN/README.md).


## Electrical Mapping

Brightness Sensor : Pin A0 
Temperature Sensor : Pin A1 
Sound Sensor : Pin A2 & Pin D-3
