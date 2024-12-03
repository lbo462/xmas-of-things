void setup() {
  Serial.begin(9600);    // USB connection
  Serial1.begin(9600);   // UART connection
  while (!Serial);       // Wait for the Serial Monitor to open
  Serial.println("MKR WAN is ready!");
}

void loop() {
  Serial1.println("Hello IoT Project");
  Serial.println("Sent: Hello IoT Project"); // Debug message to the Serial Monitor
  delay(1000);
}
