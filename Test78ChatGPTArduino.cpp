const int DATA_PIN = 2;

void setup() {
  pinMode(DATA_PIN, INPUT);
  Serial.begin(115200);
}

void loop() {
  Serial.print("DATA = ");
  Serial.println(digitalRead(DATA_PIN));
  delay(1000);
}