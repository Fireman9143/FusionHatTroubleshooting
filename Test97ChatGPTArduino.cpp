// ============================================================
// Arduino 74HC595 LATCH SNAPSHOT MONITOR
//
// D2  -> 74HC595 pin 11 CLOCK / SHCP
// D3  -> 74HC595 pin 12 LATCH / STCP
// D4  -> 74HC595 pin 14 DATA / DS
//
// D5  -> Q0 / pin 15
// D6  -> Q1 / pin 1
// D7  -> Q2 / pin 2
// D8  -> Q3 / pin 3
// D9  -> Q4 / pin 4
// D10 -> Q5 / pin 5
// D11 -> Q6 / pin 6
// D12 -> Q7 / pin 7
//
// D13 -> Q7' / pin 9
//
// Arduino GND -> 74HC595 GND / pin 8
//
// DO NOT connect Arduino 5V to the Raspberry Pi circuit.
// ============================================================

const int DATA_PIN  = 4;
const int CLOCK_PIN = 2;
const int LATCH_PIN = 3;

const int Q0_PIN = 5;
const int Q1_PIN = 6;
const int Q2_PIN = 7;
const int Q3_PIN = 8;
const int Q4_PIN = 9;
const int Q5_PIN = 10;
const int Q6_PIN = 11;
const int Q7_PIN = 12;

const int Q7_PRIME_PIN = 13;

int oldLatch = LOW;


void setup()
{
  Serial.begin(115200);

  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);

  pinMode(Q0_PIN, INPUT);
  pinMode(Q1_PIN, INPUT);
  pinMode(Q2_PIN, INPUT);
  pinMode(Q3_PIN, INPUT);
  pinMode(Q4_PIN, INPUT);
  pinMode(Q5_PIN, INPUT);
  pinMode(Q6_PIN, INPUT);
  pinMode(Q7_PIN, INPUT);

  pinMode(Q7_PRIME_PIN, INPUT);

  oldLatch = digitalRead(LATCH_PIN);

  Serial.println();
  Serial.println("========================================");
  Serial.println("74HC595 LATCH SNAPSHOT MONITOR");
  Serial.println("========================================");
  Serial.println("Waiting for LATCH...");
  Serial.println();
}


void loop()
{
  int latch = digitalRead(LATCH_PIN);

  // Detect rising edge of LATCH
  if (latch == HIGH && oldLatch == LOW)
  {
    int q0 = digitalRead(Q0_PIN);
    int q1 = digitalRead(Q1_PIN);
    int q2 = digitalRead(Q2_PIN);
    int q3 = digitalRead(Q3_PIN);
    int q4 = digitalRead(Q4_PIN);
    int q5 = digitalRead(Q5_PIN);
    int q6 = digitalRead(Q6_PIN);
    int q7 = digitalRead(Q7_PIN);

    int q7prime = digitalRead(Q7_PRIME_PIN);

    // Construct byte in normal Q7..Q0 order
    byte value =
        (q7 << 7) |
        (q6 << 6) |
        (q5 << 5) |
        (q4 << 4) |
        (q3 << 3) |
        (q2 << 2) |
        (q1 << 1) |
        q0;

    Serial.print("LATCH: Q7..Q0 = ");

    for (int i = 7; i >= 0; i--)
    {
      Serial.print((value >> i) & 1);
    }

    Serial.print("    HEX = 0x");

    if (value < 0x10)
      Serial.print("0");

    Serial.print(value, HEX);

    Serial.print("    Q7' = ");
    Serial.println(q7prime);
  }

  oldLatch = latch;

  delay(1);
}

/*
========================================
74HC595 LATCH SNAPSHOT MONITOR
========================================
Waiting for LATCH...

LATCH: Q7..Q0 = 00000011    HEX = 0x03    Q7' = 0
LATCH: Q7..Q0 = 00000111    HEX = 0x07    Q7' = 0
LATCH: Q7..Q0 = 00001111    HEX = 0x0F    Q7' = 0

The test displayed all segments except A and B lit up in the first digit, then all except A, B, and C, then all but A, B, C, and D.
I realized I had copied the test code again but not fixed the 595 pin 10 to GPIO 22, so it ran as GPIO 26.  I fixed that, ran the code again and got this:

========================================
74HC595 LATCH SNAPSHOT MONITOR
========================================
Waiting for LATCH...

LATCH: Q7..Q0 = 00011111    HEX = 0x1F    Q7' = 0
LATCH: Q7..Q0 = 00111111    HEX = 0x3F    Q7' = 0
LATCH: Q7..Q0 = 01111111    HEX = 0x7F    Q7' = 0
 

In this case, the segments followed the same pattern of turning off segmets.  
F, G, and DP1 were lit, then G, and DP1, then DP1 and off
*/