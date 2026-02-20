#include <Servo.h>

Servo myGate;  

// --- Settings ---
int openAngle = 90;   // Angle to open the Gate
int closeAngle = 0;   // Angle to close the Gate
int servoPin = 9;     // For servo's digital output

void setup() {
  Serial.begin(9600);    // Baud rate 9600
  myGate.attach(servoPin); // Attaching the servo connects it to arduino
  myGate.write(closeAngle); // Close the gate at the start
}

void loop() {
  // Check if there is any command
  if (Serial.available() > 0) {
    char command = Serial.read(); // Read the command when available
    Serial.println(command);

    if (command == '1') {
      // The HTML sends 1 when AI detects a car
      myGate.write(openAngle);
    } 
    else if (command == '0') {
      // The HTML sends 0 when AI detects anything other than the car
      myGate.write(closeAngle);
    }
  }
}
