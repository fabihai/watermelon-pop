#define SEED_BUTTON 33
#define RESET_BUTTON 25
#define ANALOG_PIN 32

// variables
int lastSeedState = HIGH; // the previous state from the input pin
int currentSeedState;     // the current reading from the input pin
int lastResetState = HIGH;
int currentResetState;

float floatMap(float x, float in_min, float in_max, float out_min, float out_max) {
  return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
}

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  pinMode(SEED_BUTTON, INPUT_PULLUP); // initializes seed button as PULLUP
  pinMode(RESET_BUTTON, INPUT_PULLUP); // initializes reset button as pullup
}

void loop() {
  // put your main code here, to run repeatedly:
  // handles potentiometer
  int analogValue = analogRead(ANALOG_PIN);
  Serial.println(analogValue);

  //handles seed button
  currentSeedState = digitalRead(SEED_BUTTON);
  if (currentSeedState == HIGH) {
    Serial.println("SEEDHIGH");
  } else {
    Serial.println("SEEDLOW");
  }

  // handles reset button
  currentResetState = digitalRead(RESET_BUTTON);
  if (currentResetState == HIGH) {
    Serial.println("RESETHIGH");
  } else {
    Serial.println("RESETLOW");
  }
  delay(50);

  // Rescale to potentiometer's voltage (from 0V to 3.3V):
  // float voltage = floatMap(analogValue, 0, 4095, 0, 3.3);

  // // print out the value you read:
  // Serial.print("Analog: ");
  // Serial.print(analogValue);
  // Serial.print(", Voltage: ");
  // Serial.println(voltage);
  // delay(1000);
}
