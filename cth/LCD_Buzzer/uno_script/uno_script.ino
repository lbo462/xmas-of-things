#include <LiquidCrystal_I2C.h>
#include <Wire.h>

// Initialize the LCD
LiquidCrystal_I2C lcd(0x3F, 16, 2);

void setup() {
  lcd.init(); // Initialize the LCD
  lcd.backlight(); // Turn on the backlight
  lcd.begin(16, 2);
  Serial.begin(9600); // Start serial communication
}

void loop() {
  if (Serial.available() > 0) { // Check if there's data available
    String message = Serial.readStringUntil('\n'); // Read data until newline character
    message.trim(); // Remove any extra whitespace or newline characters
    lcd.clear(); // Clear the LCD
    lcd.setCursor(0, 0); // Set cursor to the beginning
    lcd.print(message); // Display the message on the LCD
    
  }
}
