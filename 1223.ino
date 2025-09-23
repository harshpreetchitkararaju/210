#include <Wire.h>
#include <BH1750.h>

BH1750 lightMeter;

void setup() {
  Serial.begin(9600);       // Serial to Node-RED
  Wire.begin();
  
  if (lightMeter.begin(BH1750::CONTINUOUS_HIGH_RES_MODE)) {
    Serial.println("BH1750 ready");
  } else {
    Serial.println("Error: BH1750 not detected");
    while (1);
  }
}

void loop() {
  float lux = lightMeter.readLightLevel();   // Read light in lux
  Serial.println(lux);                       // Send to Node-RED
  delay(1000);                               // Every second
}
