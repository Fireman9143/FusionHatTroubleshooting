const int CLOCK_PIN = 3;
const int Q7_PIN    = 5;

volatile unsigned long clockCount = 0;

void clockISR()
{
    clockCount++;
}

void setup()
{
    pinMode(CLOCK_PIN, INPUT);
    pinMode(Q7_PIN, INPUT);

    Serial.begin(115200);

    attachInterrupt(
        digitalPinToInterrupt(CLOCK_PIN),
        clockISR,
        RISING
    );

    Serial.println();
    Serial.println("=================================");
    Serial.println("  595 Q7' SHIFT REGISTER TEST");
    Serial.println("=================================");
    Serial.println();
    Serial.println("D3 = CLOCK");
    Serial.println("D5 = Q7'");
    Serial.println();
    Serial.println("Waiting...");
}

void loop()
{
    static unsigned long lastClock = 0;

    if (clockCount != lastClock)
    {
        noInterrupts();
        unsigned long count = clockCount;
        interrupts();

        // Wait for the 595 output to settle
        delayMicroseconds(100);

        int q7 = digitalRead(Q7_PIN);

        Serial.print("CLOCK ");
        Serial.print(count);
        Serial.print("   Q7'=");
        Serial.println(q7);

        lastClock = count;
    }
}