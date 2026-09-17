int soundValue = 0;
int brightness = 0;

void setup()
{
  pinMode(A0, INPUT);
  pinMode(3, OUTPUT);
  pinMode(5, OUTPUT);
  pinMode(6, OUTPUT);
  pinMode(9, OUTPUT);
  Serial.begin(9600);
}

void loop()
{
  soundValue = analogRead(A0);
  brightness = map(soundValue, 100, 900, 0, 255);
  brightness = constrain(brightness, 0, 255);
  analogWrite(3, brightness);
  analogWrite(5, brightness);
  analogWrite(6, brightness);
  analogWrite(9, brightness);
  Serial.println(soundValue);
  delay(5); // Delay a little bit to improve
}