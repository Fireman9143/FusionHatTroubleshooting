// ============================================================
// DHT11 RAW READER (for comparison against the Raspberry Pi test)
//
// Moves the same DHT11 sensor over to the Arduino temporarily.
// No external library -- this bit-bangs the protocol directly
// using micros() so we can see whether a microcontroller with
// no OS/scheduler jitter can decode it reliably every time.
//
// WIRING:
//   DHT11 VCC  -> Arduino 5V (or 3.3V if your module is rated for it)
//   DHT11 GND  -> Arduino GND
//   DHT11 DATA -> Arduino pin 7
//   (most 3-pin DHT11 modules have a pull-up resistor built in;
//    if using a bare 4-pin sensor, add a 10k resistor from DATA to VCC)
// ============================================================

const int DHT_PIN = 7;

bool readDHT11(float &humidity, float &tempC) {
  uint8_t data[5] = {0, 0, 0, 0, 0};

  // Send start signal: pull low for 20ms, then release
  pinMode(DHT_PIN, OUTPUT);
  digitalWrite(DHT_PIN, LOW);
  delay(20);
  digitalWrite(DHT_PIN, HIGH);
  delayMicroseconds(30);
  pinMode(DHT_PIN, INPUT_PULLUP);

  // Wait for sensor's response: ~80us LOW, then ~80us HIGH
  unsigned long t0 = micros();
  while (digitalRead(DHT_PIN) == HIGH) {
    if (micros() - t0 > 100) return false; // no response from sensor
  }
  t0 = micros();
  while (digitalRead(DHT_PIN) == LOW) {
    if (micros() - t0 > 100) return false;
  }
  t0 = micros();
  while (digitalRead(DHT_PIN) == HIGH) {
    if (micros() - t0 > 100) return false;
  }

  // Read 40 data bits
  for (int i = 0; i < 40; i++) {
    // Each bit starts with a ~50us LOW pulse
    t0 = micros();
    while (digitalRead(DHT_PIN) == LOW) {
      if (micros() - t0 > 100) return false;
    }

    // The following HIGH duration tells us 0 vs 1:
    // ~26-28us = bit 0, ~70us = bit 1
    t0 = micros();
    while (digitalRead(DHT_PIN) == HIGH) {
      if (micros() - t0 > 200) return false;
    }
    unsigned long highTime = micros() - t0;

    data[i / 8] <<= 1;
    if (highTime > 40) {
      data[i / 8] |= 1;
    }
  }

  // Verify checksum (sum of first 4 bytes should match the 5th)
  uint8_t checksum = data[0] + data[1] + data[2] + data[3];
  if (checksum != data[4]) {
    return false;
  }

  humidity = data[0];  // DHT11 only reports whole-number humidity
  tempC = data[2];     // DHT11 only reports whole-number temperature

  return true;
}

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println("DHT11 raw reader starting...");
}

void loop() {
  float humidity, tempC;
  bool ok = readDHT11(humidity, tempC);

  if (ok) {
    float tempF = tempC * 9.0 / 5.0 + 32.0;
    Serial.print("humidity: ");
    Serial.print(humidity);
    Serial.print(",  Temperature: ");
    Serial.print(tempC);
    Serial.print(" C, ");
    Serial.print(tempF, 1);
    Serial.println(" F");
  } else {
    Serial.println("time out");
  }

  // DHT11 needs at least ~1s between reads; 2s gives extra margin
  delay(2000);
}
