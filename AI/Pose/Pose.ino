int count = 0;
char lastPose = 'N';
char currentPose = 'N';

void setup() {
  Serial.begin(9600);
  pinMode(13, OUTPUT); // Start→End LED
  pinMode(12, OUTPUT); // Count LED
  pinMode(11, OUTPUT); // Invalid
  Serial.println("Exercise Counter Ready");
}

void loop() {
  if (Serial.available() > 0) {
    char incoming = Serial.read();

    // Filter out unwanted characters (\n, \r)
    if (incoming != 'S' && incoming != 'E' && incoming != 'N') return;

    // Ignore repeats
    if (incoming == lastPose) return;

    currentPose = incoming;
    // Start→End
    if (currentPose == 'E') {
      digitalWrite(13, HIGH);
      lastPose = currentPose;
      digitalWrite(12, LOW);
      digitalWrite(11, LOW);

    }
    // End→Start (counts as full repetition)
    else if (currentPose == 'S') {
      digitalWrite(12, HIGH);
      lastPose = currentPose;
      digitalWrite(13, LOW);
      digitalWrite(11, LOW);

    }
    // Neutral pose
    else if (currentPose == 'N') {
      digitalWrite(11, HIGH);
      lastPose = currentPose;
      digitalWrite(13, LOW);
      digitalWrite(12, LOW);

    }
  }
}
