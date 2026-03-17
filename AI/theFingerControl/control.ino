int ledPins[] = {2, 4, 5,7};
int ledCount = 4;
int lastValue = -1;

void setup() {
  Serial.begin(9600);

  for (int i = 0; i < ledCount; i++) {
    pinMode(ledPins[i], OUTPUT);
  }
}

void loop() {

  if (Serial.available()) {

    int fingerCount = Serial.parseInt();
    Serial.read();

    if (fingerCount != lastValue && fingerCount >= 0 && fingerCount <= 4) {

      for (int i = 0; i < ledCount; i++) {

        if (i < fingerCount)
          digitalWrite(ledPins[i], HIGH);
        else
          digitalWrite(ledPins[i], LOW);
      }

      lastValue = fingerCount;
    }
  }
}