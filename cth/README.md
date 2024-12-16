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
- **Christmas Tree**
  - Rotates for a dynamic effect.
- **Ferris Wheel**
  - Spins as part of the village decoration when activated.
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

- **Carousel**
  - Spins as part of the village decoration when activated.

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

### Speakers
- **City Song**
  - We'll have a set of default songs stored in a SD and we receive the ID of the song to play.

```c++
#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "A8610A32303F7005"
#define APP_KEY "E045F2B331258BF8BCF884A29A4BA70C"

LoRaModem modem;
#include "notes.h"

// Define the buzzer pin
int buzzerPin = 8;

int  melodyMerryChristmas[] = {
  NOTE_B3, 
  NOTE_F4, NOTE_F4, NOTE_G4, NOTE_F4, NOTE_E4,
  NOTE_D4, NOTE_D4, NOTE_D4,
  NOTE_G4, NOTE_G4, NOTE_A4, NOTE_G4, NOTE_F4,
  NOTE_E4, NOTE_E4, NOTE_E4,
  NOTE_A4, NOTE_A4, NOTE_B4, NOTE_A4, NOTE_G4,
  NOTE_F4, NOTE_D4, NOTE_B3, NOTE_B3,
  NOTE_D4, NOTE_G4, NOTE_E4,
  NOTE_F4
};

// Tableau des durées (4 = noire, 8 = croche, etc.)
int  noteDurationsMerryChristmas[] = {
  4,
  4, 8, 8, 8, 8,
  4, 4, 4,
  4, 8, 8, 8, 8,
  4, 4, 4,
  4, 8, 8, 8, 8,
  4, 4, 8, 8,
  4, 4, 4,
  2
};

int melodyJingleBells[] = {
  NOTE_E4, NOTE_E4, NOTE_E4, // "Jingle bells"
  NOTE_E4, NOTE_E4, NOTE_E4, // "Jingle bells"
  NOTE_E4, NOTE_G4, NOTE_C4, NOTE_D4, NOTE_E4, // "Jingle all the way"
  NOTE_F4, NOTE_F4, NOTE_F4, NOTE_F4, NOTE_F4, NOTE_E4, NOTE_E4, NOTE_E4, NOTE_E4, // "Oh what fun it is to ride"
  NOTE_E4, NOTE_D4, NOTE_D4, NOTE_E4, NOTE_D4, NOTE_G4 // "In a one-horse open sleigh"
};

// Tableau des durées (4 = noire, 8 = croche, etc.)
int noteDurationsJingleBells[] = {
  8, 8, 4, 
  8, 8, 4, 
  8, 8, 8, 8, 4, 
  8, 8, 8, 8, 8, 8, 8, 8, 4, 
  8, 8, 8, 8, 8, 4
};

int melodySanta[] = {
  NOTE_G4,
  NOTE_E4,  NOTE_F4, NOTE_G4, NOTE_G4, NOTE_G4,
  NOTE_A4, NOTE_B4, NOTE_C5, NOTE_C5, NOTE_C5,
  NOTE_E4, NOTE_F4, NOTE_G4, NOTE_G4, NOTE_G4,
  NOTE_A4, NOTE_G4, NOTE_F4, NOTE_F4,
  NOTE_E4, NOTE_G4, NOTE_C4, NOTE_E4,
  NOTE_D4, NOTE_F4, NOTE_B3,
  NOTE_C4
};

int  noteDurationsSanta[] = {
  8,
  8, 8, 4, 4, 4,
  8, 8, 4, 4, 4,
  8, 8, 4,  4, 4,
  8, 8, 4, 2,
  4, 4, 4, 4,
  4, 2, 4,
  1
};

volatile bool PlaySong = false;
int currentSong = 0;

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

  // Jouer la chanson actuelle si demandé
  if (PlaySong) {
    playCurrentSong();
  }

  delay(1000);
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {

    case 20:
      Serial.println("Santa song");
      currentSong = 13;
      PlaySong = true;
      break;
    
    case 21:
      Serial.println("Merry Christmas song");
      currentSong = 11;
      PlaySong = true;
      break;

    case 22:
      Serial.println("Jingle Bells song");
      currentSong = 12;
      PlaySong = true;
      break;

    case 23:
      Serial.println("Stop song");
      PlaySong = false;
      noTone(buzzerPin);
      break;

    default:
      Serial.print("Unknown action: ");
      Serial.println(actionId);
      break;

  }
}

void playCurrentSong() {
  switch (currentSong) {
    case 11:
      for (int thisNote = 0; thisNote < sizeof(melodyMerryChristmas) / sizeof(melodyMerryChristmas[0]); thisNote++) {
        playNote(melodyMerryChristmas[thisNote], noteDurationsMerryChristmas[thisNote]);
        if (!PlaySong) break; // Vérifier si on doit arrêter
      }
      break;

    case 12:
      for (int thisNote = 0; thisNote < sizeof(melodyJingleBells) / sizeof(melodyJingleBells[0]); thisNote++) {
        playNote(melodyJingleBells[thisNote], noteDurationsJingleBells[thisNote]);
        if (!PlaySong) break; // Vérifier si on doit arrêter
      }
      break;

    case 13:
      for (int thisNote = 0; thisNote < sizeof(melodySanta) / sizeof(melodySanta[0]); thisNote++) {
        playNote(melodySanta[thisNote], noteDurationsSanta[thisNote]);
        if (!PlaySong) break; // Vérifier si on doit arrêter
      }
      break;

    default:
      break;
  }
}

void playNote(int note, int duration) {
  int noteDuration = 1000 / duration;
  tone(buzzerPin, note, noteDuration);

  int pauseBetweenNotes = noteDuration * 1.30;
  delay(pauseBetweenNotes);

  noTone(buzzerPin);
}
```

### Display
- **City Billboard**
  - Displays messages when Santa arrives or based on custom input from the website.
  - The messages will be a set of default messages and we receive the ID of the message to display.

## Data Requirements

### Input Data
- **Billboard Message**
  - ID of the message to be displayed.
- **Song Selection**
  - Default, action-specific (with the ID of the song to play).
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
  