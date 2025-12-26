const int tiltPin = 2;

void setup() {
  Serial.begin(9600);
  pinMode(tiltPin, INPUT_PULLUP);
}

void loop() {
  int state = digitalRead(tiltPin);

  if (state == LOW) {
    Serial.println("U");   // Tilt → Jump
  } else {
    Serial.println("D");   // Flat → Crouch
  }

  delay(200);  // avoid flooding serial
}
