int relayPin = 7;

void setup() {
  Serial.begin(9600);
  pinMode(relayPin, OUTPUT);
}

void loop() {
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');

    if (command == "ON") {
      digitalWrite(relayPin, HIGH);
    }
    else if (command == "OFF") {
      digitalWrite(relayPin, LOW);
    }
  }
}