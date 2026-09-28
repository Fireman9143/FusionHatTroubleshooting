// ============================================
// SN74HC595 DIAGNOSTIC MONITOR
// Arduino Uno
//
// D2 = DATA  -> 595 pin 14
// D3 = CLOCK -> 595 pin 11
// D4 = LATCH -> 595 pin 12
// D5 = Q7'   -> 595 pin 9
// ============================================

const int DATA_PIN  = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;
const int Q7_PIN    = 5;

volatile byte capturedData[64];
volatile byte capturedQ7[64];
volatile unsigned long clockCount = 0;

void clockISR()
{
    if (clockCount < 64)
    {
        capturedData[clockCount] = digitalRead(DATA_PIN);
        capturedQ7[clockCount] = digitalRead(Q7_PIN);
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
    Serial.println("   SN74HC595 DIAGNOSTIC MONITOR");
    Serial.println("======================================");
    Serial.println();
    Serial.println("D2 = DATA");
    Serial.println("D3 = CLOCK");
    Serial.println("D4 = LATCH");
    Serial.println("D5 = Q7'");
    Serial.println();
    Serial.println("Waiting for Pi...");
    Serial.println();
}

void printBits(byte data)
{
    for (int i = 7; i >= 0; i--)
    {
        Serial.print((data >> i) & 1);
    }
}

void loop()
{
    static unsigned long lastCount = 0;
    static int lastLatch = -1;

    // Report latch changes
    int latch = digitalRead(LATCH_PIN);

    if (latch != lastLatch)
    {
        Serial.print("LATCH -> ");
        Serial.println(latch);
        lastLatch = latch;
    }

    // Report clock edges
    if (clockCount != lastCount)
    {
        noInterrupts();

        unsigned long count = clockCount;

        byte data;
        byte q7;

        if (lastCount < 64)
        {
            data = capturedData[lastCount];
            q7 = capturedQ7[lastCount];
        }
        else
        {
            data = 0;
            q7 = 0;
        }

        interrupts();

        Serial.print("CLOCK ");
        Serial.print(count);
        Serial.print(": DATA=");
        Serial.print(data);
        Serial.print("  Q7'=");
        Serial.println(q7);

        lastCount = count;

        // Every 8 clocks, identify a byte
        if ((count % 8) == 0)
        {
            Serial.println("  ---- 8 CLOCKS COMPLETE ----");
            Serial.println();
        }
    }
}