#include <ArduinoJson.h>
// ▼ Pin extender ▼
#include <Wire.h>
#include <PCF8574.h>
// ▼ Infrared temperature sensor ▼
#include <Adafruit_MLX90614.h>
// ▼ RFID reader ▼
#include <SPI.h>
#include <MFRC522.h>
// ▼ Led controller ▼
#include <LedRGB.h>


#define RELAY_LOCK    P5

#define PS_SANITIZER       P7
#define PS_TEMPERATURE     P6   

#define SANITIZER_LEVEL_SENSOR  A0
#define SANITIZER_LEVEL         D3
#define SANITIZER_PUMP          D4   

#define LED_RED         P0     
#define LED_GREEN       P1 
#define LED_BLUE        P2    


#define RST_PIN            D1
#define R0_SS_PIN          D8
#define R1_SS_PIN          D9        

MFRC522 mfrc522_0(R0_SS_PIN, RST_PIN);  // Create MFRC522 instance
MFRC522 mfrc522_1(R1_SS_PIN, RST_PIN);


PCF8574 pcf8574(0x38);

Adafruit_MLX90614 mlx = Adafruit_MLX90614(); // Create Adafruit_MLX90614 instance

StaticJsonDocument<200> doc;

void setup() {
	Serial.begin(9600);		// Initialize serial communications with the PC
	while (!Serial);		// Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
	SPI.begin();			// Init SPI bus
    Wire.begin();
	mfrc522_0.PCD_Init();		// Init MFRC522
    delay(4);
    mfrc522_1.PCD_Init();
	delay(4);				// Optional delay. Some board do need more time after init to be ready, see Readme

    if (!mlx.begin()) {
        Serial.println("Error connecting to MLX sensor. Check wiring.");
        while (1);
    };
    
    LedRGB myLED(LED_RED, LED_GREEN, LED_BLUE, CC);    // CC or CA
    
    pinMode(SANITIZER_LEVEL, OUTPUT, LOW);       
    pinMode(SANITIZER_PUMP, OUTPUT, LOW);

    pinMode(SANITIZER_LEVEL_SENSOR, INPUT);

    pcf8574.pinMode(PS_SANITIZER, INPUT);     // Sanitizer proximity sensor
	pcf8574.pinMode(PS_TEMPERATURE, INPUT);     // Temperature proximity sensor
}

void loop() {
	if (mfrc522_0.PICC_IsNewCardPresent())
    {
        if (mfrc522_0.PICC_ReadCardSerial())
        {
        String card_code = "";
        for (byte i = 0; i < mfrc522_0.uid.size; i++)
        {
            card_code.concat(String(mfrc522_0.uid.uidByte[i] < 0x10 ? " 0" : " "));
            card_code.concat(String(mfrc522_0.uid.uidByte[i], DEC));
        }
        card_code.toUpperCase();
        String code_json = "{\"code\":" + card_code.substring(1) + " , \"temperature\": \"None\", \"dispenser\": \"None\", \"joining\": 1 }";
        Serial.println(code_json);
        delay(500);
        }
    }
    if (mfrc522_1.PICC_IsNewCardPresent())
    {
        if (mfrc522_1.PICC_ReadCardSerial())
        {
            String card_code = "";
            for (byte i = 0; i < mfrc522_1.uid.size; i++)
            {
                card_code.concat(String(mfrc522_1.uid.uidByte[i] < 0x10 ? " 0" : " "));
                card_code.concat(String(mfrc522_1.uid.uidByte[i], DEC));
            }
            card_code.toUpperCase();
            String code_json = "{\"code\":" + card_code.substring(1) + " , \"temperature\": \"None\", \"dispenser\": \"None\", \"joining\": 0 }";
            Serial.println(code_json);
            delay(500);
        }
    }
    int value = 0;
    value = pcf8574.digitalRead(PS_SANITIZER);
	if(value == HIGH){                          // ? HIGH or LOW
        if(readSensor() > 5){
            digitalWrite(SANITIZER_PUMP, HIGH);
            delay(1000);
            digitalWrite(SANITIZER_PUMP, LOW);
            int dispenser_percentage = readSensor();
            String disp_json = "{\"code\": \"None\", \"temperature\": \"None\", \"dispenser\": true, \"dispenser_percentage\": \"" + dispenser_percentage + "\" }";
            Serial.println(disp_json);
            delay(1000);
        }
    }
    int value = 0;
    value = pcf8574.digitalRead(PS_TEMPERATURE);
	if(value == HIGH){
        if(readSensor() > 5){
            temperature = mlx.readObjectTempC() * 1.15;
            String temp_json = "{\"code\": \"None\", \"temperature\": \"" + temperature + "\", \"dispenser\": \"None\"}";
            Serial.println(temp_json);
        }
    }
    if (Serial.available() > 0){
        String data = Serial.readStringUntil('\n');
        DeserializationError error = deserializeJson(doc, data);
        if(!error){
            if(doc["allowed"] != None){ 
                if(doc["allowed"]){
                    pcf8574.digitalWrite(RELAY_LOCK, HIGH);
                    myLED.defaultColor(doc["led_color"]);
                    delay(2000);
                    pcf8574.digitalWrite(RELAY_LOCK, LOW);
                    myLED.defaultColor("");
                }
                else{
                    myLED.defaultColor(doc["led_color"]);
                    delay(2000);
                    myLED.defaultColor("");
                }
            }
            // ! if(doc["led_color"] != None)
            // ! {
            // !     myLED.defaultColor(doc["led_color"]);  
            // ! }
        }
    }
    // ? yield();
} 

int readSensor() {
    digitalWrite(SANITIZER_LEVEL, HIGH);      // Turn the sensor ON
    delay(10);                                  // Wait 10 milliseconds
    int val = analogRead(SANITIZER_LEVEL_SENSOR);      // Read the analog value form sensor
    digitalWrite(SANITIZER_LEVEL, LOW);       // Turn the sensor OFF
    return val * 100 / 1023;              // Return current reading in percentage (0-1023 = 0%-100%)
}