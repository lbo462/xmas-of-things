#include <MKRWAN.h>

#define FRAME_LENGTH 1
#define APP_EUI "0000000000000000"
#define APP_KEY "C185BE8D31DDFA226F074201D1D2CCB9"
#include "notes.h"

LoRaModem modem;

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

  Serial.begin(115200);  // USB connection
  Serial1.begin(9600);   // UART connection
  //while (!Serial);       // Wait for the Serial Monitor to open
  Serial.println("MKR WAN is ready!");

  //while (!Serial);

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
    
    triggerAction(actionId);
  }

  // Jouer la chanson actuelle si demandé
  if (PlaySong) {
    playCurrentSong();
  }

  delay(1000);
}

void triggerAction(int actionId) {
  switch(actionId) {
    case 20:
      Serial.println("Merry Christmas song");
      currentSong = 11;
      PlaySong = true;
      break;

    case 21:
      Serial.println("Jingle Bells song");
      currentSong = 12;
      PlaySong = true;
      break;

    case 22:
      Serial.println("Santa song");
      currentSong = 13;
      PlaySong = true;
      break;

    case 23:
      Serial.println("Stop song");
      PlaySong = false;
      noTone(buzzerPin);
      break;

    case 40:
      Serial.println("Message : Merry Xmas");
      sendMessageToLcd(1);
      break;

    case 41:
      Serial.println("Message : Feliz Navidad");
      sendMessageToLcd(2);
      break;

    case 42:
      Serial.println("No message");
      sendMessageToLcd(0);
      break;

    case 43:
      Serial.println("Message : Freezing Cold");
      sendMessageToLcd(3);
      break;
    
    case 44:
      Serial.println("Message : Too Hot");
      sendMessageToLcd(4);
      break;

    default:
      Serial.print("Unsupported action: ");
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
    case 3:
      text = "Freezing cold *";
      break;
    case 4:
      text = "Too hot !!";
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