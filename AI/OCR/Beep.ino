// Arduino code to switch light ON/OFF based on commands from JS
// Connect LED or relay to pin 13 (or change pin number as needed)

int buzzerPin = 13;   // Output pin for LED/Relay
char receivedChar;   // Store incoming serial data

void setup() {
  Serial.begin(9600);     // Match baud rate with JS serial connection
  pinMode(buzzerPin, OUTPUT);
}

void loop() {
  // Check if data is available from JS
  if (Serial.available() > 0) {
    receivedChar = Serial.read();

    if (receivedChar == 'D') {   
      // Wheel detected → Light ON
      digitalWrite(buzzerPin, HIGH);
      Serial.println("Danger");
    } 
    else if (receivedChar == 'N') {  
      // Mobile detected → Light OFF
      digitalWrite(buzzerPin, LOW);
      Serial.println("Safe");
    }
  }
}
