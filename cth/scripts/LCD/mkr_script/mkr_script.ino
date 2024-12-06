#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "0000000000000000"
#define APP_KEY "C185BE8D31DDFA226F074201D1D2CCB9"

LoRaModem modem;

int LED = 10;

void setup() {

  Serial.begin(115200);  // USB connection
  Serial1.begin(9600);   // UART connection
  while (!Serial);       // Wait for the Serial Monitor to open
  Serial.println("MKR WAN is ready!");

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
  Serial.println("Successfully connected");
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
    Serial.print("Action ID: ");
      Serial.println(actionId);
    if (actionId == 20 || actionId == 21 || actionId == 22) {
      triggerAction(actionId);
    } else {
      // Optional: Handle unsupported action IDs
      Serial.print("Unsupported action: ");
      Serial.println(actionId);
    }
  }

  delay(1000);
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {
    case 20:
      Serial.println("No message");
      sendMessageToLcd(0);
      break;

    case 21:
      Serial.println("Message : Merry Xmas");
      sendMessageToLcd(1);
      break;

    case 22:
      Serial.println("Message : Feliz Navidad");
      sendMessageToLcd(2);
      break;

    default:
      Serial.println("Message : Welcome to IoT");
      sendMessageToLcd(100);
      break;

  }
}

void sendMessageToLcd(int messageId) {
  const char* text; // Declare a pointer for the text message
  
  // Assign text based on messageId
  switch (messageId) {
    case 0:
      text = "";
      break;
    case 1:
      text = "Merry Xmas";
      break;
    case 2:
      text = "Feliz Navidad";
      break;
    case 100:
      text = "Welcome to IoT";
      break;
    default:
      text = "";
      break;
  }

  Serial1.println(text);
  Serial.println(text); // Debug message to the Serial Monitor
  delay(1000);
}
