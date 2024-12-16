# City Town Hall Documentation

## Overview
This document outlines the data requirements for the Christmas city engines, lights, speakers and every other actionable.\
For detail task information and status we made a [Trello](https://trello.com/b/3zekwBi3/iot-central-hall).

## Actions

### Lights

**Christmas Tree and its garland** lights up when it’s dark in the room (uses brightness sensor).

### Engines

- **Ferris Wheel** spins as part of the village decoration when activated.

```c++
#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "A8610A3335266B07"
#define APP_KEY "7C12482597E9435CB1C96BD36EB1CFA4"
#include <Servo.h>

Servo servoMotor; // Crée un objet servo

LoRaModem modem;
bool wheelRunning = false; // Variable pour contrôler l'état de la roue
int currentAngle = 0; // Angle actuel du servo
int angleIncrement = 1; // Incrément pour faire tourner la roue

void setup() {
  Serial.begin(115200);

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
  servoMotor.write(90); // Position neutre du servo
}

void loop() {
  // Envoi d'un paquet vide pour ouvrir la fenêtre RX
  modem.beginPacket();
  modem.print(0);
  modem.endPacket();

  // Vérification de la fenêtre RX
  if (modem.available()) {
    // Lecture de la trame complète
    char rcv[FRAME_LENGTH];
    int i = 0;
    while (modem.available()) {
      rcv[i++] = (char)modem.read();
    }
    
    // Analyse de la trame et déclenchement des actions
    int actionId = rcv[0];
    triggerAction(actionId);
  }

  // Appeler la rotation de la roue de manière non bloquante
  if (wheelRunning) {
    rotateWheel();
  }

  delay(10); // Petit délai pour éviter une boucle trop rapide
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {
    case 10:
      Serial.println("wheel starting");
      wheelRunning = true; // Activer la rotation de la roue
      break;

    case 11:
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
  // Faire tourner la roue progressivement
  currentAngle += angleIncrement;
  
  // Inverser la direction si l'angle atteint les limites
  if (currentAngle >= 180 || currentAngle <= 0) {
    angleIncrement = -angleIncrement;
  }

  servoMotor.write(currentAngle); // Bouge le servo vers l'angle actuel
  // delay(15); // Pause pour un mouvement fluide
}

```

- **Carousel** spins as part of the village decoration when activated.

```c++
#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "A8610A3434448A12"
#define APP_KEY "057B115899F35FC1003987BCF81652B8"
#include <Servo.h>

Servo servoMotor; // Crée un objet servo

LoRaModem modem;
bool wheelRunning = false; // Variable pour contrôler l'état de la roue
int currentAngle = 0; // Angle actuel du servo
int angleIncrement = 1; // Incrément pour faire tourner la roue

void setup() {
  Serial.begin(115200);

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
  servoMotor.write(90); // Position neutre du servo
}

void loop() {
  // Envoi d'un paquet vide pour ouvrir la fenêtre RX
  modem.beginPacket();
  modem.print(0);
  modem.endPacket();

  // Vérification de la fenêtre RX
  if (modem.available()) {
    // Lecture de la trame complète
    char rcv[FRAME_LENGTH];
    int i = 0;
    while (modem.available()) {
      rcv[i++] = (char)modem.read();
    }
    
    // Analyse de la trame et déclenchement des actions
    int actionId = rcv[0];
    triggerAction(actionId);
  }

  // Appeler la rotation de la roue de manière non bloquante
  if (wheelRunning) {
    rotateWheel();
  }

  delay(10); // Petit délai pour éviter une boucle trop rapide
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {
    case 0:
      Serial.println("manege starting");
      wheelRunning = true; // Activer la rotation de la roue
      break;

    case 1:
      Serial.println("manege stopping");
      wheelRunning = false; // Désactiver la rotation de la roue
      break;

    default:
      Serial.print("Unknown action: ");
      Serial.println(actionId);
      break;
  }
}

void rotateWheel() {
  // Faire tourner la roue progressivement
  currentAngle += angleIncrement;
  
  // Inverser la direction si l'angle atteint les limites
  if (currentAngle >= 180 || currentAngle <= 0) {
    angleIncrement = -angleIncrement;
  }

  servoMotor.write(currentAngle); // Bouge le servo vers l'angle actuel
  delay(15); // Pause pour un mouvement fluide
}

```

### Play songs using buzzer and display messages using LCD module

- Refer to the repository LCD_Buzzer

## Data Requirements

### Input Data
- **Billboard Message**
  - ID of the message to be displayed.
- **Song Selection**
  - Default, action-specific (with the ID of the song to play).
- **Control Commands**
  - On/Off states for lights, ferris wheel and carousel.

### Sensor Data
- **Brightness Level**
  - Controls Christmas tree and starlights.
- **Temperature Level**
  - Triggers a message on the billboard.
  