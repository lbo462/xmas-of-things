# Read actions sent by the logic map

With the current state of the logic map, and the TTN decoder, here's a sample code that read downlink topic from TTN and triggers dummy function corresponding to functions:

This script requires:
- [MKRWAN](https://downloads.arduino.cc/libraries/github.com/arduino-libraries/MKRWAN-1.1.0.zip)

```c++
#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "xxxxxxxxxxxxxxxx"
#define APP_KEY "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

LoRaModem modem;

void setup() {
  Serial.begin(115200);

  while (!Serial);

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
  // send a dummy packet to trigger the RX window
  modem.beginPacket();
  modem.print(0);
  modem.endPacket();

  // check RX window
  if (modem.available()) {
    // read full frame
    char rcv[FRAME_LENGTH];
    int i = 0;
    while (modem.available()) {
      rcv[i++] = (char)modem.read();
    }
    
    // parse the frame and trigger actions
    int actionId = rcv[0];
    triggerAction(actionId);
  }

  delay(1000);
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {
    case 1:
      Serial.println("XMAS_TREE_LED");
      // call the correct function here ...
      break;

    case 2:
      Serial.println("XMAS_TREE_STAR");
      // call the correct function here ...
      break;

    case 3:
      Serial.println("VILLAGE_LED");
      // call the correct function here ...
      break;

    case 4:
      Serial.println("SANTA_TRACK_LED");
      // call the correct function here ...
      break;

    case 5:
      Serial.println("SNOW_SPRAY");
      // call the correct function here ...
      break;

    default:
      Serial.print("Unknown action: ");
      Serial.println(actionId);
      break;

  }
}
```

## Footnotes

Here's basically how the big picture works:

- The logic map send a JSON payload to TTN.
- This payload is decoded by TTN into a frame (a byte sequence) currently containing only the `action_id`.
- This frame is received by the script above in `rcv`. The first and only byte is then `action_id`.

Find more detail about the TTN processing on the [TTN documentation](../TTN/README.md).