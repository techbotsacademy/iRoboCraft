#include <Servo.h>

// Create servo objects
Servo baseServo;
Servo shoulderServo;
Servo elbowServo;
Servo clawServo;

// Servo signal pins
const int BASE_PIN = 3;
const int SHOULDER_PIN = 5;
const int ELBOW_PIN = 7;
const int CLAW_PIN = 9;

void setup() {
  // Attach servos to Arduino pins
  baseServo.attach(BASE_PIN);
  shoulderServo.attach(SHOULDER_PIN);
  elbowServo.attach(ELBOW_PIN);
  clawServo.attach(CLAW_PIN);

  // Move all servos to starting positions
  baseServo.write(90);
  shoulderServo.write(90);
  elbowServo.write(90);
  clawServo.write(90);

  delay(1000);
}

void loop() {
  // Move base left to right
  for (int pos = 60; pos <= 120; pos++) {
    baseServo.write(pos);
    delay(20);
  }

  for (int pos = 120; pos >= 60; pos--) {
    baseServo.write(pos);
    delay(20);
  }

  // Move shoulder up and down
  for (int pos = 60; pos <= 120; pos++) {
    shoulderServo.write(pos);
    delay(20);
  }

  for (int pos = 120; pos >= 60; pos--) {
    shoulderServo.write(pos);
    delay(20);
  }

  // Move elbow forward and backward
  for (int pos = 60; pos <= 120; pos++) {
    elbowServo.write(pos);
    delay(20);
  }

  for (int pos = 120; pos >= 60; pos--) {
    elbowServo.write(pos);
    delay(20);
  }

  // Open and close claw
  clawServo.write(40);
  delay(1000);

  clawServo.write(90);
  delay(1000);
}