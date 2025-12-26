/*
  DigitalReadSerial

  Reads a digital input on pin 2, prints the result to the Serial Monitor

  This example code is in the public domain.

  https://docs.arduino.cc/built-in-examples/basics/DigitalReadSerial/
*/

// digital pin 2 has a pushbutton attached to it. Give it a name:
int tilt_pin = 2;

// the setup routine runs once when you press reset:
void setup() {
  // initialize serial communication at 9600 bits per second:
  Serial.begin(9600);
  // make the pushbutton's pin an input:
  pinMode(tilt_pin, INPUT);
}

// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int state = digitalRead(tilt_pin);
  // print out the state of the button:
  if(state){
    Serial.println("U");
  }
  else {
    Serial.println("D");
  }
  delay(1);  // delay in between reads for stability
}
