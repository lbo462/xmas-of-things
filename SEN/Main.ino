#include <MKRWAN.h>
#include <DHT.h>

#define APP_EUI "0000000000000000"
#define APP_KEY "AC6DC50997CF1761BC19C1E32D8E9CCE"

LoRaModem modem;
DHT my_dht;

const int photoresistorPin = A0; // light sensor pin 
int analog_input = A2; // sound sensor pin
int sound_sent = 0; // Variable to track sound trigger state
unsigned long lastSendTime = 0; // Variable to store the last send time
const unsigned long sendInterval = 2000; // Sending interval (2 seconds)

// Variables to hold fixed sensor values for the current interval
int fixed_temperature = 0; 
int fixed_photoresistorValue = 0;

void setup() {
  Serial.begin(115200);
  while (!Serial);

  my_dht.setup(A1);
  pinMode(analog_input, INPUT); // Sound sensor
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

  // Read light sensor and temperature once per interval
  if (millis() - lastSendTime >= sendInterval) {
    // Fix sensor values for the interval
    fixed_temperature = my_dht.getTemperature();
    fixed_photoresistorValue = analogRead(photoresistorPin);

    Serial.print("Photoresistor value (fixed): ");
    Serial.println(fixed_photoresistorValue);

    Serial.print("Temperature value (fixed): ");
    Serial.println(fixed_temperature);
  }

  // Read sound sensor continuously
  float analog_value = analogRead(analog_input) * (5.0 / 1023.0);

  // If the sound sensor exceeds the threshold, set sound_sent to 1
  if (analog_value > 3.6) {
    sound_sent = 1;
  }

  // Check if it's time to send data
  if (millis() - lastSendTime >= sendInterval) {
    lastSendTime = millis();

    // Send data to TTN
    modem.setPort(3);
    modem.beginPacket();

    // Create data package
    modem.write(fixed_temperature);               
    modem.write(fixed_photoresistorValue);  
    modem.write(sound_sent); 

    modem.endPacket();

    // Reset sound_sent after sending
    sound_sent = 0;
  }

  delay(100);
}