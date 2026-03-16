#include <Servo.h>

Servo myServo;

int flexPin = A0;     // Flex sensor connected to A0
int flexValue = 0;

void setup() {
  Serial.begin(9600);
  myServo.attach(9);   // Servo signal pin connected to pin 9
}

void loop() {

  flexValue = analogRead(flexPin);   // Read flex sensor value
  Serial.println(flexValue);

  if (flexValue > 500) {
    myServo.write(135);   // Rotate servo to 45 degrees
  } 
  else {
    myServo.write(0);    // Rotate servo to 0 degrees
  }

}