#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>

const char* ssid = "AirFiber-pHLK0q";      
const char* password = "54455445";        
const char* mqtt_server = "192.168.1.250"; 

WiFiClient wifiClient;
PubSubClient client(wifiClient);

unsigned long lastMsg = 0;

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi connected!");
  client.setServer(mqtt_server, 1883);
}

void loop() {
  if (!client.connected()) {
    while (!client.connected()) {
      if (client.connect("Nano33IoTClient")) {
        Serial.println("Connected to MQTT broker!");
      } else {
        delay(2000);
      }
    }
  }

  client.loop();

  unsigned long now = millis();
  if (now - lastMsg > 3000) {
    lastMsg = now;

    
    int lightValue = random(0, 1000);

    char msg[10];
    sprintf(msg, "%d", lightValue);
    client.publish("terrarium/light", msg);

    Serial.print("Published: ");
    Serial.println(msg);
  }
}
