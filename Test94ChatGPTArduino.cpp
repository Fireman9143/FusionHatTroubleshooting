/*This test was used while manually shifting bits and latching*/


// ============================================================
// Arduino 74HC595 Change-Only Monitor
//
// Arduino connections:
//
// D2  -> 74HC595 pin 14 (DATA / DS)
// D3  -> 74HC595 pin 11 (CLOCK / SHCP)
// D4  -> 74HC595 pin 12 (LATCH / STCP)
//
// D5  -> 74HC595 Q0 / pin 15
// D6  -> 74HC595 Q1 / pin 1
// D7  -> 74HC595 Q2 / pin 2
// D8  -> 74HC595 Q3 / pin 3
// D9  -> 74HC595 Q4 / pin 4
// D10 -> 74HC595 Q5 / pin 5
// D11 -> 74HC595 Q6 / pin 6
// D12 -> 74HC595 Q7 / pin 7
//
// D13 -> 74HC595 Q7' / pin 9
//
// Arduino GND -> 74HC595 GND / pin 8
//
// DO NOT connect Arduino 5V to the Raspberry Pi circuit.
// ============================================================


// Control pins
const int DATA_PIN = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;


// 74HC595 outputs Q0 through Q7
const int Q0_PIN = 5;
const int Q1_PIN = 6;
const int Q2_PIN = 7;
const int Q3_PIN = 8;
const int Q4_PIN = 9;
const int Q5_PIN = 10;
const int Q6_PIN = 11;
const int Q7_PIN = 12;


// Serial output from 74HC595
const int Q7_PRIME_PIN = 13;


// Previous states
int oldData;
int oldClock;
int oldLatch;

int oldQ0;
int oldQ1;
int oldQ2;
int oldQ3;
int oldQ4;
int oldQ5;
int oldQ6;
int oldQ7;

int oldQ7Prime;


// ============================================================
// SETUP
// ============================================================

void setup()
{
  Serial.begin(115200);

  // Control inputs
  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);

  // 74HC595 output monitoring
  pinMode(Q0_PIN, INPUT);
  pinMode(Q1_PIN, INPUT);
  pinMode(Q2_PIN, INPUT);
  pinMode(Q3_PIN, INPUT);
  pinMode(Q4_PIN, INPUT);
  pinMode(Q5_PIN, INPUT);
  pinMode(Q6_PIN, INPUT);
  pinMode(Q7_PIN, INPUT);

  // Q7'
  pinMode(Q7_PRIME_PIN, INPUT);


  // ----------------------------------------------------------
  // Save the starting state.
  // We do NOT print these values.
  // ----------------------------------------------------------

  oldData = digitalRead(DATA_PIN);
  oldClock = digitalRead(CLOCK_PIN);
  oldLatch = digitalRead(LATCH_PIN);

  oldQ0 = digitalRead(Q0_PIN);
  oldQ1 = digitalRead(Q1_PIN);
  oldQ2 = digitalRead(Q2_PIN);
  oldQ3 = digitalRead(Q3_PIN);
  oldQ4 = digitalRead(Q4_PIN);
  oldQ5 = digitalRead(Q5_PIN);
  oldQ6 = digitalRead(Q6_PIN);
  oldQ7 = digitalRead(Q7_PIN);

  oldQ7Prime = digitalRead(Q7_PRIME_PIN);


  Serial.println();
  Serial.println("================================");
  Serial.println("74HC595 CHANGE-ONLY MONITOR");
  Serial.println("================================");
  Serial.println("Waiting for changes...");
  Serial.println();
}


// ============================================================
// LOOP
// ============================================================

void loop()
{
  int data = digitalRead(DATA_PIN);
  int clock = digitalRead(CLOCK_PIN);
  int latch = digitalRead(LATCH_PIN);

  int q0 = digitalRead(Q0_PIN);
  int q1 = digitalRead(Q1_PIN);
  int q2 = digitalRead(Q2_PIN);
  int q3 = digitalRead(Q3_PIN);
  int q4 = digitalRead(Q4_PIN);
  int q5 = digitalRead(Q5_PIN);
  int q6 = digitalRead(Q6_PIN);
  int q7 = digitalRead(Q7_PIN);

  int q7Prime = digitalRead(Q7_PRIME_PIN);


  // ----------------------------------------------------------
  // DATA changed?
  // ----------------------------------------------------------

  if (data != oldData)
  {
    Serial.print("DATA   : ");
    Serial.print(oldData);
    Serial.print(" -> ");
    Serial.println(data);

    oldData = data;
  }


  // ----------------------------------------------------------
  // CLOCK changed?
  // ----------------------------------------------------------

  if (clock != oldClock)
  {
    Serial.print("CLOCK  : ");
    Serial.print(oldClock);
    Serial.print(" -> ");
    Serial.println(clock);

    oldClock = clock;
  }


  // ----------------------------------------------------------
  // LATCH changed?
  // ----------------------------------------------------------

  if (latch != oldLatch)
  {
    Serial.print("LATCH  : ");
    Serial.print(oldLatch);
    Serial.print(" -> ");
    Serial.println(latch);

    oldLatch = latch;
  }


  // ----------------------------------------------------------
  // Q0 changed?
  // ----------------------------------------------------------

  if (q0 != oldQ0)
  {
    Serial.print("Q0     : ");
    Serial.print(oldQ0);
    Serial.print(" -> ");
    Serial.println(q0);

    oldQ0 = q0;
  }


  // ----------------------------------------------------------
  // Q1 changed?
  // ----------------------------------------------------------

  if (q1 != oldQ1)
  {
    Serial.print("Q1     : ");
    Serial.print(oldQ1);
    Serial.print(" -> ");
    Serial.println(q1);

    oldQ1 = q1;
  }


  // ----------------------------------------------------------
  // Q2 changed?
  // ----------------------------------------------------------

  if (q2 != oldQ2)
  {
    Serial.print("Q2     : ");
    Serial.print(oldQ2);
    Serial.print(" -> ");
    Serial.println(q2);

    oldQ2 = q2;
  }


  // ----------------------------------------------------------
  // Q3 changed?
  // ----------------------------------------------------------

  if (q3 != oldQ3)
  {
    Serial.print("Q3     : ");
    Serial.print(oldQ3);
    Serial.print(" -> ");
    Serial.println(q3);

    oldQ3 = q3;
  }


  // ----------------------------------------------------------
  // Q4 changed?
  // ----------------------------------------------------------

  if (q4 != oldQ4)
  {
    Serial.print("Q4     : ");
    Serial.print(oldQ4);
    Serial.print(" -> ");
    Serial.println(q4);

    oldQ4 = q4;
  }


  // ----------------------------------------------------------
  // Q5 changed?
  // ----------------------------------------------------------

  if (q5 != oldQ5)
  {
    Serial.print("Q5     : ");
    Serial.print(oldQ5);
    Serial.print(" -> ");
    Serial.println(q5);

    oldQ5 = q5;
  }


  // ----------------------------------------------------------
  // Q6 changed?
  // ----------------------------------------------------------

  if (q6 != oldQ6)
  {
    Serial.print("Q6     : ");
    Serial.print(oldQ6);
    Serial.print(" -> ");
    Serial.println(q6);

    oldQ6 = q6;
  }


  // ----------------------------------------------------------
  // Q7 changed?
  // ----------------------------------------------------------

  if (q7 != oldQ7)
  {
    Serial.print("Q7     : ");
    Serial.print(oldQ7);
    Serial.print(" -> ");
    Serial.println(q7);

    oldQ7 = q7;
  }


  // ----------------------------------------------------------
  // Q7' changed?
  // ----------------------------------------------------------

  if (q7Prime != oldQ7Prime)
  {
    Serial.print("Q7'    : ");
    Serial.print(oldQ7Prime);
    Serial.print(" -> ");
    Serial.println(q7Prime);

    oldQ7Prime = q7Prime;
  }


  // Small delay so we don't hammer the serial port
  delay(1);
}

/*

==========================
74HC595 CHANGE-ONLY MONITOR
================================
Waiting for changes...


================================
74HC595 CHANGE-ONLY MONITOR
================================
Waiting for changes...

LATCH  : 0 -> 1
Q1     : 1 -> 0
Q2     : 1 -> 0
Q3     : 1 -> 0
Q4     : 1 -> 0
LATCH  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 0 -> 1
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q1     : 0 -> 1
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q2     : 0 -> 1
LATCH  : 1 -> 0
LATCH  : 0 -> 1
LATCH  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
LATCH  : 0 -> 1
Q0     : 1 -> 0
Q3     : 0 -> 1
Q4     : 0 -> 1
LATCH  : 1 -> 0
DATA   : 0 -> 1
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
CLOCK  : 0 -> 1
CLOCK  : 1 -> 0
DATA   : 1 -> 0
*/