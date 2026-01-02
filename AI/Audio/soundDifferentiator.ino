void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    char c = Serial.read();

    if (c == 'A') {
      // Ambulance logic
    }
    else if (c == 'H') {
      // Horn logic
    }
    else if (c == 'B') {
      // Background logic
    }
  }
}
