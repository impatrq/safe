#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

// Informacion para el post
const char* SECRET_KEY = "SECRET_KEY";
const char* ENV_UPDATE_URL = "http://...:8000/api/modules/env_update/";
const char* DOOR_MAC = "DOOR_MAC";

// Datos de red
const char* ssid = "SSID";
const char* password = "PASSWORD";

void setup() {
    Serial.begin(9600);
    conect_to_wifi();
}

void loop() {
    String response = env_update(500, 500, 500, 500);                                   // Realizamos un post mandando los valores de los valores de los gases y almacenamos la respuesta

    if (response != "Post Failed") {                                                    // Si el post no fallo
        DynamicJsonDocument response_info(1024);                                        // Creamos un domunento json dinamico
        DeserializationError error = deserializeJson(response_info, response);          // Deserializamos la respuesta que nos llego en formato json y lo almacenamos en response_info 
        if (!error) {                                                                   // Si no hay ningun error en la deserializacion
          String success_message = response_info["success_message"]; 
          if (success_message == "Successfully Updated") {
                String co_response_level = response_info["co_level"];
                String co2_response_level = response_info["co2_level"];
                String metano_response_level = response_info["metano_level"];
                String lpg_response_level = response_info["lpg_level"]; 

                pic_communication_colour(co_response_level, co2_response_level, metano_response_level, lpg_response_level);       
            }
        }  
    }  
  delay(30000);                                                   // Esperamos 30 segundos
}

void conect_to_wifi() {
    Serial.prtint("a");                                            // Para avisar que se esta iniciando la conexion wifi
    WiFi.begin(ssid, password);                                    // Conectar Wifi

    while(WiFi.status() != WL_CONNECTED) {                         // Mientras no este conectado al wifi
        delay(500);
    }
    Serial.prtint("b");                                            // Para avisar que se termino de conectar al wifi
}

String env_update(float co_level, float co2_level, float metano_level, float lpg_level) {
  if (WiFi.status() == WL_CONNECTED) {                               // Si esta conectado al WiFi

    WiFiClient client;  
    HTTPClient http;

    http.begin(client, ENV_UPDATE_URL);                         // Creamos la conexion http
    
    DynamicJsonDocument doc(2048);                              // Creamos un documento dinamico de Json e indicamos su espacio

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