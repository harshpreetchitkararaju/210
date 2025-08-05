#include <WiFiNINA.h>
#include <ThingSpeak.h>
#include "DHT.h"

// Wi-Fi details
const char* ssid = "Harshpreet";       
const char* pass = "harshpreet";    
// ThingSpeak details
unsigned long channelID =  3026739;   
const char* writeAPIKey = "HC1RVOFLAUJGH6OO"; 

WiFiClient client;

// DHT Setup
#define DHTPIN 2          
#define DHTTYPE DHT11     
DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600);
  dht.begin();

  // Connect to Wi-Fi
  Serial.print("Connecting to Wi-Fi");
  WiFi.begin(ssid, pass);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected to Wi-Fi!");

  ThingSpeak.begin(client); 
}

void loop() {
  float temperature = dht.readTemperature();  

  if (isnan(temperature)) {
    Serial.println("Failed to read temperature from DHT sensor!");
    return;
  }

  Serial.print("Temperature: ");
  Serial.print(temperature);
  Serial.println(" °C");

 
  ThingSpeak.setField(1, temperature);
  ThingSpeak.writeFields(channelID, writeAPIKey);

  delay(30000); 
}