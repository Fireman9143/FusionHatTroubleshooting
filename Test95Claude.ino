// ============================================================
// 74HC595 LATCH-TRIGGERED SNAPSHOT MONITOR
//
// Instead of logging every individual pin change, this counts
// SRCLK pulses between each RCLK (latch) event, then reads the
// full Q0-Q7 state the instant latch fires. One clean line is
// printed per "frame" sent to the shift register, which makes
// it easy to see:
//   - whether every send is exactly 8 clock pulses
//   - the exact byte that actually got latched
//
// WIRING (connect these as simple test-point taps, Arduino as
// INPUT only -- do not drive these pins):
//   Arduino pin 2  <- Fusion/595 CLOCK  (SRCLK, 595 pin 11)
//   Arduino pin 3  <- Fusion/595 LATCH  (RCLK,  595 pin 12)
//   Arduino pin 4  <- Fusion/595 DATA   (SDI,   595 pin 14)  [reference only]
//   Arduino pin 5  <- 595 Q0  (pin 15)
//   Arduino pin 6  <- 595 Q1  (pin 1)
//   Arduino pin 7  <- 595 Q2  (pin 2)
//   Arduino pin 8  <- 595 Q3  (pin 3)
//   Arduino pin 9  <- 595 Q4  (pin 4)
//   Arduino pin 10 <- 595 Q5  (pin 5)
//   Arduino pin 11 <- 595 Q6  (pin 6)
//   Arduino pin 12 <- 595 Q7  (pin 7)
//   Arduino GND    <- common GND with the Fusion/Pi
//
// Pins 2 and 3 are used because they're the Uno's two hardware
// interrupt pins (INT0/INT1) -- CLOCK and LATCH must be on these.
// ============================================================

const int PIN_CLOCK = 2;   // SRCLK
const int PIN_LATCH = 3;   // RCLK
const int PIN_DATA  = 4;   // SDI (informational only)

const int PIN_Q0 = 5;
const int PIN_Q1 = 6;
const int PIN_Q2 = 7;
const int PIN_Q3 = 8;
const int PIN_Q4 = 9;
const int PIN_Q5 = 10;
const int PIN_Q6 = 11;
const int PIN_Q7 = 12;

volatile unsigned long clockPulseCount = 0;
volatile bool latchFired = false;

unsigned long frameNumber = 0;

void onClockRise() {
  clockPulseCount++;
}

void onLatchRise() {
  latchFired = true;
}

void setup() {
  Serial.begin(115200);

  pinMode(PIN_CLOCK, INPUT);
  pinMode(PIN_LATCH, INPUT);
  pinMode(PIN_DATA, INPUT);
  pinMode(PIN_Q0, INPUT);
  pinMode(PIN_Q1, INPUT);
  pinMode(PIN_Q2, INPUT);
  pinMode(PIN_Q3, INPUT);
  pinMode(PIN_Q4, INPUT);
  pinMode(PIN_Q5, INPUT);
  pinMode(PIN_Q6, INPUT);
  pinMode(PIN_Q7, INPUT);

  attachInterrupt(digitalPinToInterrupt(PIN_CLOCK), onClockRise, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_LATCH), onLatchRise, RISING);

  Serial.println(F("================================================"));
  Serial.println(F("74HC595 LATCH SNAPSHOT MONITOR"));
  Serial.println(F("================================================"));
  Serial.println(F("One line per LATCH event."));
  Serial.println(F("Format: #frame [N pulses] Q7 Q6 Q5 Q4 Q3 Q2 Q1 Q0 = 0xXX"));
  Serial.println();
}

void loop() {
  if (latchFired) {
    // Let signals settle right after latch before sampling
    delayMicroseconds(20);

    int q0 = digitalRead(PIN_Q0);
    int q1 = digitalRead(PIN_Q1);
    int q2 = digitalRead(PIN_Q2);
    int q3 = digitalRead(PIN_Q3);
    int q4 = digitalRead(PIN_Q4);
    int q5 = digitalRead(PIN_Q5);
    int q6 = digitalRead(PIN_Q6);
    int q7 = digitalRead(PIN_Q7);

    byte value = (q7 << 7) | (q6 << 6) | (q5 << 5) | (q4 << 4) |
                 (q3 << 3) | (q2 << 2) | (q1 << 1) | q0;

    unsigned long pulses = clockPulseCount;
    clockPulseCount = 0;
    latchFired = false;
    frameNumber++;

    Serial.print(F("#"));
    Serial.print(frameNumber);
    Serial.print(F(" ["));
    Serial.print(pulses);
    Serial.print(F(" pulses] "));
    Serial.print(q7); Serial.print(F(" "));
    Serial.print(q6); Serial.print(F(" "));
    Serial.print(q5); Serial.print(F(" "));
    Serial.print(q4); Serial.print(F(" "));
    Serial.print(q3); Serial.print(F(" "));
    Serial.print(q2); Serial.print(F(" "));
    Serial.print(q1); Serial.print(F(" "));
    Serial.print(q0);
    Serial.print(F("  = 0x"));
    if (value < 0x10) Serial.print(F("0"));
    Serial.print(value, HEX);

    if (pulses != 8) {
      Serial.print(F("   <-- WARNING: expected 8 pulses, got "));
      Serial.print(pulses);
    }

    Serial.println();
  }
}
