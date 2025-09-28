// Arduino code to switch light ON/OFF based on commands from JS
// Connect LED or relay to pin 13 (or change pin number as needed)

int lightPin = 13;   // Output pin for LED/Relay
char receivedChar;   // Store incoming serial data

void setup() {
  Serial.begin(9600);     // Match baud rate with JS serial connection
  pinMode(lightPin, OUTPUT);
  digitalWrite(lightPin, LOW); // Light OFF initially
}

void loop() {
  // Check if data is available from JS
  if (Serial.available() > 0) {
    receivedChar = Serial.read();
    Serial.println("HERE");

    if (receivedChar == 'R') {   
      // Wheel detected → Light ON
      digitalWrite(lightPin, HIGH);
      Serial.println("Light ON");
    } 
    else if (receivedChar == 'L') {  
      // Mobile detected → Light OFF
      digitalWrite(lightPin, LOW);
      Serial.println("Light OFF");
    }
  }
}
