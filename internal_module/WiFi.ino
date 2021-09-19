#include <WiFi.h>

// Datos de red
const char* ssid = "SSID";
const char* password = "PASSWORD";

void setup() {
    Serial.begin(9600);
    conect_to_wifi();
}

void loop() {

}

void conect_to_wifi() {
  WiFi.begin(ssid, password);                                    // Conectar Wifi

  while(WiFi.status() != WL_CONNECTED) {                         // Mientras no este conectado al wifi
    delay(500);
  }
}