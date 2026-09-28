const int DATA_PIN  = 2;
const int CLOCK_PIN = 3;
const int LATCH_PIN = 4;

void setup() {
  pinMode(DATA_PIN, INPUT);
  pinMode(CLOCK_PIN, INPUT);
  pinMode(LATCH_PIN, INPUT);

  Serial.begin(115200);
}

void loop() {
  static int lastData = -1;

  int data = digitalRead(DATA_PIN);

  if (data != lastData) {
    Serial.print("DATA changed -> ");
    Serial.println(data);
    lastData = data;
  }

  delay(10);
}