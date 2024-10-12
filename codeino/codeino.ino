#include <WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>
#include <ArduinoJson.h>

#define DHTPIN 4
#define DHTTYPE DHT11 

const char* ssid = "Wokwi-GUEST";
const char* password = "";

const char* MQTTServer = "broker.emqx.io";
const char* MQTT_Topic = "sensor/temperature_humidity";
const char* MQTT_ID = "5b3c4629-c4be-44e5-b05e-bd50c4c1ee95";
int Port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

DHT dht(DHTPIN, DHTTYPE);

void WIFIConnect() {
  Serial.println("Connecting to SSID");
  WiFi.begin(ssid, password);  // Kết nối đến mạng WiFi Minh Thu 5G
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("WiFi connected");
  Serial.print(", IP address: ");
  Serial.println(WiFi.localIP());
}

void MQTT_Reconnect() {
  while (!client.connected()) {
    if (client.connect(MQTT_ID)) {
      Serial.print("MQTT Topic: ");
      Serial.print(MQTT_Topic);
      Serial.print(" connected");
      client.subscribe(MQTT_Topic);
      Serial.println("");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      delay(5000);
    }
  }
}

void setup() {
  Serial.begin(115200);
  dht.begin();
  WIFIConnect();  // Gọi hàm kết nối WiFi

  client.setServer(MQTTServer, Port);
}

void loop() {
  if (!client.connected()) {
    MQTT_Reconnect();
  }
  client.loop();
  
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }
  Serial.print("Humidity: ");
  Serial.print(h);
  Serial.print("%  Temperature: ");
  Serial.print(t);

  String payload = "{\"temperature\": " + String(t) + ", \"humidity\": " + String(h) + "}";
  client.publish(MQTT_Topic, payload.c_str());

  delay(2000);
}
