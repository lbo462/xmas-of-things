# City Town Hall Documentation

## Overview
This document outlines the data requirements for the Christmas city engines, lights, speakers and every other actionable.\
For detail task information and status we made a [Trello](https://trello.com/b/3zekwBi3/iot-central-hall).

## Actions

### Lights

**Christmas Tree and its garland** lights up when it’s dark in the room (uses brightness sensor).

```c++

#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "A8610A3339426210"
#define APP_KEY "F3352D51007EA676161D3BEC5E4DB111"

LoRaModem modem;
int r = 4; // Red pin
int v = 3; // Green pin
int b = 2; // Blue pin

int LED1=11;
int LED2=12;
int LED3=13;
int LED4=14;

bool lightsTransitionDone = false; // Flag to track if intermittent lights have run
int finalColor = 3; // 0 = Red, 1 = Green, 2 = Blue, 3 = violet

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

  pinMode(r, OUTPUT);
  pinMode(v, OUTPUT);
  pinMode(b, OUTPUT);

  // Turn off all LEDs initially
  digitalWrite(r, LOW);
  digitalWrite(v, LOW);
  digitalWrite(b, LOW);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);

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

  delay(10);
}

void triggerAction(int actionId) {
  Serial.print("Proceed to action: ");
  Serial.println(actionId, HEX);

  switch(actionId) {

    case 30:
      Serial.println("XMAS_TREE_STAR_ON");
      // if (!lightsTransitionDone) {
    // intermittent_light();
    // delay(5000);
    // lightsTransitionDone = true;
     // }
    star_light_on(); // Keep the final color on
      break;

    case 31:
      Serial.println("XMAS_TREE_STAR_OFF");
      star_light_off();
      break;

    case 32:
      Serial.println("VILLAGE_LED_ON");
      turnOnLights();
      break;

    case 33:
      Serial.println("VILLAGE_LED_OFF");
      turnOffLights();
      break;

    default:
      Serial.print("Unknown action: ");
      Serial.println(actionId);
      break;

  }
}
void intermittent_light() {
  // Fade green and blue LEDs
  for (int i = 0; i <= 255; i++) {
    analogWrite(v, i);
    analogWrite(b, i);
    delay(50);
  }
  for (int i = 255; i >= 0; i--) {
    analogWrite(v, i);
    analogWrite(b, i);
    delay(50);
  }
}

void star_light_on() {
  // Turn off all LEDs
  analogWrite(r, 0);
  analogWrite(v, 0);
  analogWrite(b, 0);
  pinMode(r, OUTPUT);
  pinMode(v, OUTPUT);
  pinMode(b, OUTPUT);
  digitalWrite(r, LOW);
  digitalWrite(v, LOW);
  digitalWrite(b, LOW);

  // Turn on the selected final color
  if (finalColor == 0) {
    digitalWrite(r, HIGH); // Red
  } else if (finalColor == 1) {
    digitalWrite(v, HIGH); // Green
  } else if (finalColor == 2) {
    digitalWrite(b, HIGH); // Blue
  }
  else if(finalColor== 3){
    digitalWrite(r, HIGH);
    digitalWrite(b, HIGH);
  }
}

void star_light_off() {
  // Turn off all LEDs
  analogWrite(r, 0);
  analogWrite(v, 0);
  analogWrite(b, 0);
  pinMode(r, OUTPUT);
  pinMode(v, OUTPUT);
  pinMode(b, OUTPUT);
  digitalWrite(r, LOW);
  digitalWrite(v, LOW);
  digitalWrite(b, LOW);
}

void turnOnLights() {
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
  digitalWrite(LED3, HIGH);
  digitalWrite(LED4, HIGH);
}

void turnOffLights() {
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
  digitalWrite(LED3, LOW);
  digitalWrite(LED4, LOW);
}

void turnOnInOrder() {
  digitalWrite(LED1, HIGH);
  delay(300);
  digitalWrite(LED2, HIGH);
  delay(800);
  digitalWrite(LED3, HIGH);
  delay(300);
  digitalWrite(LED4, HIGH);
}

void handleCityLights() {
  turnOnInOrder();
  delay(300);
  digitalWrite(LED1, LOW);
  delay(300);
  digitalWrite(LED2, LOW);
  delay(1000);
  digitalWrite(LED3, LOW);
  delay(300);
  digitalWrite(LED4, LOW);
  delay(300);

  turnOnLights();
  delay(300);
  turnOffLights();
  delay(300);
  turnOnLights();
  delay(300);
  turnOffLights();
  delay(300);

  turnOnInOrder();
}
```

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
  