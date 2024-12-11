# Sensors Documentation

The objective of the sensors team is to read data from multiple sensors and send this to TTN.

Below is a simple script that read the value of temperature and humidity and send both to TTN.

This script requires:
- [MKRWAN](https://downloads.arduino.cc/libraries/github.com/arduino-libraries/MKRWAN-1.1.0.zip)
- [DHT](https://perso.citi.insa-lyon.fr/oiova/docs/arduino-DHT-master.zip)

To respect TTN standards, please check the [TTN documentation](../TTN/README.md).

```c++
#include <MKRWAN.h>
#include <DHT.h>

#define APP_EUI "0000000000000000"
#define APP_KEY "AC6DC50997CF1761BC19C1E32D8E9CCE"

LoRaModem modem;
DHT my_dht;

const int photoresistorPin = A0; 

void setup() {
  Serial.begin(115200);
  while (!Serial);

  my_dht.setup(A1);

  if (!modem.begin(EU868)) {
    Serial.println("Failed to start module");
    while (1) {}
  };

  Serial.print("Your module version is: ");
  Serial.println(modem.version());

  Serial.print("Your device EUI is: ");
  Serial.println(modem.deviceEUI());

  if (!modem.joinOTAA(APP_EUI, APP_KEY)) {
    Serial.println("Something went wrong; are you indoor? Move near a window and retry");
    while (1) {}
  }
}

void loop() {
  while (modem.available()) {
    Serial.write(modem.read());
  }
  modem.poll();

  // read light sensor
  int photoresistorValue = analogRead(photoresistorPin);
  Serial.print("Photoresistor value: ");
  Serial.println(photoresistorValue);

  // read temperature
  int temperature = my_dht.getTemperature();
  Serial.print("Temperature value: ");
  Serial.println(temperature);

  // send data to TTN
  modem.setPort(3);
  modem.beginPacket();

  // create data package
  modem.write(temperature);               
  modem.write(photoresistorValue);   
  modem.endPacket();

  delay(2000);
}
```
