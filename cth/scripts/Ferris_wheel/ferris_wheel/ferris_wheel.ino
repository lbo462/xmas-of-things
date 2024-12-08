#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "A8610A3335266B07" //to change
#define APP_KEY "7C12482597E9435CB1C96BD36EB1CFA4" //to change
#include <Servo.h>

Servo servoMotor; // Crée un objet servo

LoRaModem modem;
bool wheelRunning = false; // Variable pour contrôler l'état de la roue


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

  servoMotor.attach(2); // Connecté à la broche ~2
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
    case 30:
      Serial.println("wheel starting");
      wheelRunning = true; // Activer la rotation de la roue
      rotateWheel();
      break;

    case 31:
      Serial.println("wheel stopping");
      wheelRunning = false; // Désactiver la rotation de la roue
      break;

    default:
      Serial.print("Unknown action: ");
      Serial.println(actionId);
      break;

  }
}


void rotateWheel() {
  while (wheelRunning) {
    for (int angle = 0; angle <= 180 && wheelRunning; angle++) {
      servoMotor.write(angle); // Bouge le servo vers l'angle
      delay(15);               // Attends pour un mouvement fluide
    }
    for (int angle = 180; angle >= 0 && wheelRunning; angle--) {
      servoMotor.write(angle); // Retour à l'angle initial
      delay(15);
    }
  }
  // Assurez-vous que le servo est à une position neutre lorsqu'il s'arrête
  servoMotor.write(90); // Position centrale ou neutre
}