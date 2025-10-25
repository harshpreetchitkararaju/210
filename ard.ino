const int TURBIDITY_PIN = A0;
const int PH_PIN = A1;

void setup() {
  Serial.begin(9600);
  Serial.println("🐠 FIXED CODE - BOTH SENSORS 🐠");
}

void loop() {
  // Read both sensors properly
  int turbidity = analogRead(TURBIDITY_PIN);
  int phRaw = analogRead(PH_PIN);
  float voltage = phRaw * (5.0 / 1023.0);
  float pH = 7.0 + ((2.5 - voltage) * 3.0);
  
  // Turbidity logic - adjust threshold based on your sensor
  bool isDirty = (turbidity < 200); // Change this number as needed
  
  // Send all data
  Serial.print("PH:");
  Serial.print(pH, 2);
  Serial.print(",TURB:");
  Serial.print(turbidity);
  Serial.print(",DIRTY:");
  Serial.print(isDirty ? "YES" : "NO");
  Serial.print(",RAW:");
  Serial.print(phRaw);
  Serial.println();
  
  delay(3000);
}