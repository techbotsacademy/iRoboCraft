// C++ code
//
#include <Servo.h>

Servo myGate;
int openAngle = 45;   // Angle to open the Gate
int closeAngle = 0;   // Angle to close the Gate

void setup()
{
  Serial.begin(9600);
  myGate.attach(6, 500, 2500);
  myGate.write(closeAngle);
}

void loop()
{
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n'); // Read full line
    int y = command.toInt(); // Convert to number 

    if (y == 1) {
      myGate.write(openAngle);
    } 
    else if (y == 0) {
      myGate.write(closeAngle);
    }
  }
}