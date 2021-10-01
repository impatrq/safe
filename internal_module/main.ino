// MQ PINES
#define MQ4_PIN 35
#define MQ7_PIN 34
#define MQ9_PIN 32

const float factor_lpg = 2;                     // MQ4
const float factor_metano = 2.25;               // MQ4
const float factor_co = 5;                      // MQ7
const float factor_co2 = 1.75;                  // MQ9

// Informacion para el post
const char* SECRET_KEY = "SECRET_KEY";
const char* ENV_UPDATE_URL = "http://safe.com.ar/api/modules/env_update/";
const char* DOOR_MAC = "DOOR_MAC";

// Datos de red
const char* ssid = "SSID";
const char* password = "PASSWORD";

void setup() {
    Serial.begin(9600);
    conect_to_wifi();
}

void loop() {
    int mq4_adc = analogRead(MQ4_PIN); 
    int mq7_adc = analogRead(MQ7_PIN); 
    int mq9_adc = analogRead(MQ9_PIN); 

    float ppm_lpg = mq4_adc / factor_lpg; 
    float ppm_metano = mq4_adc / factor_metano; 
    float ppm_co = mq7_adc / factor_co; 
    float ppm_co2 = mq9_adc / factor_co2;

    delay(30000)
}

void conect_to_wifi() {
    Serial.prtint("a");
    WiFi.begin(ssid, password);                                    // Conectar Wifi

    while(WiFi.status() != WL_CONNECTED) {                         // Mientras no este conectado al wifi
        delay(500);
    }

    Serial.prtint("b");
}    