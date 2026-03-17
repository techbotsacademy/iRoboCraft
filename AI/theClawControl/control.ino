#include <Servo.h>

Servo myServo;
int angle = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(9); // Servo connected to pin 9
}

void loop() {
  if (Serial.available() > 0) {
    angle = Serial.parseInt();   // Read angle from serial
    if (angle >= 0 && angle <= 180) {
      myServo.write(angle);      // Rotate servo
    }
  }
}