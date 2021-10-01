#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

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
const char* ENV_UPDATE_URL = "http://..../api/modules/env_update/";
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

    String response = env_update(ppm_co, ppm_co2, ppm_metano, ppm_lpg);
  
    if (response != "Post Failed") {
        DynamicJsonDocument response_info(1024); 
        DeserializationError error = deserializeJson(response_info, response);
        if (!error) {
            if (response_info["success_message"] == "Successfully Updated") {
                String co_response_level = response_info["co_level"];
                String co2_response_level = response_info["co2_level"];
                String metano_response_level = response_info["metano_level"];
                String lpg_response_level = response_info["lpg_level"];
                
                pic_communication_colour(co_response_level, co2_response_level, metano_response_level, lpg_response_level);
            }
        }  
    }  

    delay(30000);
}

void connect_to_wifi() {
    Serial.print("a");
    WiFi.begin(ssid, password);                                    // Conectar Wifi

    while(WiFi.status() != WL_CONNECTED) {                         // Mientras no este conectado al wifi
        delay(500);
    }

    Serial.print("b");
}    

String env_update(float co_level, float co2_level, float metano_level, float lpg_level) {
    if (WiFi.status() == WL_CONNECTED) {                               // Si esta conectado al WiFi

        WiFiClient client;  
        HTTPClient http;

        http.begin(client, ENV_UPDATE_URL);                         // Creamos la conexion http
        
        DynamicJsonDocument doc(1024);                              // Creamos un documento dinamico de Json e indicamos su espacio

        // Asignamos los valores con la determinada clave valor 
        doc["SECRET_KEY"] = SECRET_KEY;                           
        doc["door_mac"] = DOOR_MAC;
        doc["co_level"] = co_level;
        doc["co2_level"] = co2_level;
        doc["metano_level"] = metano_level;
        doc["lpg_level"] = lpg_level;

        String json;                                                // Creamos una variable json de tipo String
        
        serializeJson(doc, json);                                   // Serealizamos lo escrito en el documento creado previamente y lo guardamos en la variable json
                
        // Enviamos el post
        http.addHeader("Content-Type", "application/json");
        int httpResponseCode = http.POST(json);

        if (httpResponseCode == 200) {       
            String response = http.getString();                       
            return response;
        }
        else {
            return "Post Failed";
        }        
    }
}

void pic_communication_colour(String co_level, String co2_level, String metano_level, String lpg_level) {
    if (co2_level == "High" || co_level == "High" || lpg_level == "High" || metano_level == "High") {
        Serial.print("r");
    }
    else {
        if (co2_level == "Medium" || co_level == "Medium" || lpg_level == "Medium" || metano_level == "Medium") {
            Serial.print("y");
        }
        else {
            if (co2_level == "Low" || co_level == "Low" || lpg_level == "Low" || metano_level == "Low") {
                Serial.print("g");
            }
        }
    }
}