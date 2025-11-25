// Blue Pill + FTDI: blink LED on PC13 when PC sends 'B'

void setup() {
  pinMode(PC13, OUTPUT);
  digitalWrite(PC13, HIGH);   // LED off on many Blue Pills (inverted logic)

  Serial.begin(115200);       // match this in Python
  Serial.println("Connected to A429 Reader!");
  digitalWrite(PC13, LOW);   // LED on
  delay(2500);
  digitalWrite(PC13, HIGH);  // LED off
  delay(1000);
}

void loop() {
  if (Serial.available() > 0) {
    char c = Serial.read();

    if (c == 'B') {           // Blink command
      while (!Serial.available()) {
        // wait here OR add timeout logic if you want
       }
      char digit = Serial.read();
      int n = digit - '0';
      blinkLed(n);            // blink 3 times
      Serial.println("OK BLINK");
    }
    // you can add more commands later, e.g. '1' = on, '0' = off, etc.
  }
}

void blinkLed(int times) {
  for (int i = 0; i < times; i++) {
    digitalWrite(PC13, LOW);   // LED on
    delay(200);
    digitalWrite(PC13, HIGH);  // LED off
    delay(200);
  }
}
