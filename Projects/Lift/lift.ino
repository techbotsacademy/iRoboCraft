char cmd;

int IN1 = 8;
int IN2 = 9;

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  if (Serial.available()) {
    cmd = Serial.read();

    if (cmd == 'U') {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
    }
    else if (cmd == 'D') {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, HIGH);
    }
    else if (cmd == 'S') {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
    }
  }
}