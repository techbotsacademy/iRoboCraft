int triggerPin = 5;
int echoPin = 4;
int speakerPin = 8;

int distance = 0;
int music_note = 0;

long readUltrasonicDistance(int trig, int echo) {
  pinMode(trig, OUTPUT);
  digitalWrite(trig, LOW);
  delayMicroseconds(2);
  digitalWrite(trig, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig, LOW);
  pinMode(echo, INPUT);
  return pulseIn(echo, HIGH);
}

void setup() {
  Serial.begin(9600);
  pinMode(speakerPin, OUTPUT);
}

void loop() {
  // Echo time microsecond me read karo
  long duration = readUltrasonicDistance(triggerPin, echoPin);
 
  // Microseconds ko cm me convert karo
  distance = duration / 58;

  // Readouts clear dekhne ke liye Serial print
  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  // Distance ko music notes (0 se 7) me map karo
  // (Range 2cm se 30cm set ki hai taaki Tinkercad simulation me 1-7 notes asani se trigger ho sakein)
  music_note = map(distance, 2, 30, 1, 7);
  music_note = constrain(music_note, 1, 7);

  // Exact Tinkercad logic
  if (distance < 25 && distance > 0) {
    if (music_note == 1) {
      tone(speakerPin, 523, 200); // C5
    }
    if (music_note == 2) {
      tone(speakerPin, 587, 200); // D5
    }
    if (music_note == 3) {
      tone(speakerPin, 659, 200); // E5
    }
    if (music_note == 4) {
      tone(speakerPin, 740, 200); // F#5
    }
    if (music_note == 5) {
      tone(speakerPin, 784, 200); // G5
    }
    if (music_note == 6) {
      tone(speakerPin, 880, 200); // A5
    }
    if (music_note == 7) {
      tone(speakerPin, 988, 200); // B5
    }
  }

  delay(100); // Stable readings aur smooth sound ke liye delay 100ms kar diya gaya hai
}