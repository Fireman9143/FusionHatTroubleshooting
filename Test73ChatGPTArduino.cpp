const int DATA_PIN  = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;

volatile unsigned long clockCount = 0;
volatile byte capturedData[32];
volatile byte capturedLatch[32];

void clockISR() {
  if (clockCount < 32) {
    capturedData[clockCount] = digitalRead(DATA_PIN);
    capturedLatch[clockCount] = digitalRead(LATCH_PIN);
  }

  clockCount++;
}

void setup() {
  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);

  Serial.begin(115200);

  attachInterrupt(
    digitalPinToInterrupt(CLOCK_PIN),
    clockISR,
    RISING
  );

  Serial.println();
  Serial.println("Pi 595 CLOCK MONITOR");
  Serial.println("====================");
  Serial.println("Waiting for clock edges...");
}

void loop() {

  static unsigned long lastCount = 0;

  if (clockCount != lastCount) {

    noInterrupts();

    unsigned long count = clockCount;

    Serial.print("Clock edges detected: ");
    Serial.println(count);

    if (count <= 32) {
      for (unsigned long i = lastCount; i < count; i++) {
        Serial.print("  Edge ");
        Serial.print(i + 1);
        Serial.print(": DATA=");
        Serial.print(capturedData[i]);
        Serial.print("  LATCH=");
        Serial.println(capturedLatch[i]);
      }
    }

    interrupts();

    lastCount = count;
  }
}