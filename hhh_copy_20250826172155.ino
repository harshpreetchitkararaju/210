#include <WiFiNINA.h>
#include <ArduinoHttpClient.h>

char ssid[] = "harshpreet";      
char pass[] = "harshpreet";      


char server[] = "maker.ifttt.com"; 
String IFTTT_Key = "d8FJ9kLmN2pQRsTuvwXyZ";   
String IFTTT_Event_On = "sunlight_on";        
String IFTTT_Event_Off = "sunlight_off";     

WiFiClient wifi;
HttpClient client = HttpClient(wifi, server, 80);

const int lightPin = A0;  
int threshold = 500;      


bool sunlightState = false;

void setup() {
  Serial.begin(9600);

  // Connect to WiFi
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    delay(2000);
  }
  Serial.println(" Connected to WiFi!");
}

void loop() {
  int lightValue = analogRead(lightPin);
  Serial.print("Light Sensor Value: ");
  Serial.println(lightValue);

  // Condition: sunlight detected
  if (lightValue > threshold && sunlightState == false) {
    Serial.println(" Sunlight detected → Sending IFTTT trigger");
    triggerIFTTT(IFTTT_Event_On);
    sunlightState = true;
  } 
  
  // Condition: sunlight stopped
  else if (lightValue <= threshold && sunlightState == true) {
    Serial.println(" Sunlight stopped → Sending IFTTT trigger");
    triggerIFTTT(IFTTT_Event_Off);
    sunlightState = false;
  }

  delay(5000); // check every 5 seconds
}


void triggerIFTTT(String eventName) {
  String url = "/trigger/" + eventName + "/with/key/" + IFTTT_Key;

  Serial.print(" Requesting URL: ");
  Serial.println(url);

  client.get(url);

  int statusCode = client.responseStatusCode();
  String response = client.responseBody();

  Serial.print(" Status code: ");
  Serial.println(statusCode);
  Serial.print(" Response: ");
  Serial.println(response);
}
