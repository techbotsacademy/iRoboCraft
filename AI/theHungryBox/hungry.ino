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
if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    int y = command.toInt();

    if (y == 1) {
        myGate.write(openAngle);
        Serial.write("open"); // Echo the byte back to HTML
    }
    else if (y == 0) {
        Serial.println("Closing");
        myGate.write(closeAngle);
        Serial.write("close"); // Echo the byte back to HTML
    }
}
}