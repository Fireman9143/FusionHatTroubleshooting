// SN74HC595 diagnostic monitor
//
// Arduino connections:
// D2 = DATA / DS
// D3 = CLOCK / SHCP
// D4 = LATCH / STCP
// D5 = Q7' serial output
//
// GND = Pi GND

const int DATA_PIN  = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;
const int Q7_PIN    = 5;

volatile unsigned long clockCount = 0;

volatile byte dataBits[64];
volatile byte q7Bits[64];

volatile bool latchSeen = false;

void clockISR()
{
  if (clockCount < 64)
  {
    dataBits[clockCount] = digitalRead(DATA_PIN);
    q7Bits[clockCount] = digitalRead(Q7_PIN);
  }

  clockCount++;
}

void setup()
{
  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);
  pinMode(Q7_PIN, INPUT);

  Serial.begin(115200);

  attachInterrupt(
    digitalPinToInterrupt(CLOCK_PIN),
    clockISR,
    RISING
  );

  Serial.println();
  Serial.println("======================================");
  Serial.println(" SN74HC595 DIAGNOSTIC MONITOR");
  Serial.println("======================================");
  Serial.println("D2 = DATA");
  Serial.println("D3 = CLOCK");
  Serial.println("D4 = LATCH");
  Serial.println("D5 = Q7'");
  Serial.println();
  Serial.println("Waiting for Pi...");
  Serial.println();
}

void printByte(byte value)
{
  for (int i = 7; i >= 0; i--)
  {
    Serial.print((value >> i) & 1);
  }
}

void loop()
{
  static unsigned long lastCount = 0;

  if (clockCount != lastCount)
  {
    noInterrupts();

    unsigned long count = clockCount;

    // Copy captured values to local arrays
    byte localData[64];
    byte localQ7[64];

    unsigned long start = lastCount;

    if (start > 64)
      start = 64;

    unsigned long end = count;

    if (end > 64)
      end = 64;

    for (unsigned long i = start; i < end; i++)
    {
      localData[i] = dataBits[i];
      localQ7[i] = q7Bits[i];
    }

    interrupts();

    for (unsigned long i = start; i < end; i++)
    {
      Serial.print("CLOCK ");
      Serial.print(i + 1);
      Serial.print(": DATA=");
      Serial.print(localData[i]);
      Serial.print("  Q7'=");
      Serial.print(localQ7[i]);
      Serial.print("  LATCH=");
      Serial.println(digitalRead(LATCH_PIN));
    }

    lastCount = count;
  }

  // Report latch changes
  static int lastLatch = -1;

  int latch = digitalRead(LATCH_PIN);

  if (latch != lastLatch)
  {
    Serial.print("LATCH -> ");
    Serial.println(latch);

    lastLatch = latch;
  }
}