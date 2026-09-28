const int DATA_PIN  = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;

void setup() {
  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);

  Serial.begin(115200);

  Serial.println("Arduino signal monitor started");
}

void loop() {
  int data  = digitalRead(DATA_PIN);
  int clock = digitalRead(CLOCK_PIN);
  int latch = digitalRead(LATCH_PIN);

  Serial.print("DATA=");
  Serial.print(data);
  Serial.print("  CLOCK=");
  Serial.print(clock);
  Serial.print("  LATCH=");
  Serial.println(latch);

  delay(500);
}