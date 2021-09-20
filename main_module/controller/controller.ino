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

#define RELAY_LOCK P1

#define PS_SANITIZER D4
#define PS_TEMPERATURE D3

#define SANITIZER_LEVEL_SENSOR A0
#define SANITIZER_LEVEL P2
#define SANITIZER_PUMP P0

#define LED_RED P7
#define LED_GREEN P6
#define LED_BLUE P5

#define RST_PIN D3
#define R0_SS_PIN D8
#define R1_SS_PIN D0

MFRC522 mfrc522_0(R0_SS_PIN, RST_PIN); // Create MFRC522 instance
MFRC522 mfrc522_1(R1_SS_PIN, RST_PIN);

PCF8574 pcf8574(0x27);

//Adafruit_MLX90614 mlx = Adafruit_MLX90614(); // Create Adafruit_MLX90614 instance

StaticJsonDocument<200> doc;

void setup()
{
    Serial.begin(9600); // Initialize serial communications with the PC
    while (!Serial)
        ;        // Do nothing if no serial port is opened (added for Arduinos based on ATMEGA32U4)
    SPI.begin(); // Init SPI bus
    pcf8574.pinMode(SANITIZER_LEVEL, OUTPUT);
    pcf8574.pinMode(SANITIZER_PUMP, OUTPUT);

    pinMode(SANITIZER_LEVEL_SENSOR, INPUT);

    pinMode(PS_SANITIZER, INPUT); // Sanitizer proximity sensor
    pinMode(PS_TEMPERATURE, INPUT);
    pcf8574.pinMode(RELAY_LOCK, OUTPUT);
    pcf8574.pinMode(LED_RED, OUTPUT);
    pcf8574.pinMode(LED_GREEN, OUTPUT);
    pcf8574.pinMode(LED_BLUE, OUTPUT);
    Serial.print("Init pcf8574...");
    if (pcf8574.begin())
    {
        Serial.println("OK");
    }
    else
    {
        Serial.println("KO");
    }

    mfrc522_0.PCD_Init(); // Init MFRC522
    delay(4);
    mfrc522_1.PCD_Init();
    delay(4); // Optional delay. Some board do need more time after init to be ready, see Readme

    // if (!mlx.begin()) {
    //     Serial.println("Error connecting to MLX sensor. Check wiring.");
    //     while (1);
    //};

    pcf8574.digitalWrite(RELAY_LOCK, LOW);
    pcf8574.digitalWrite(LED_RED, LOW);
    pcf8574.digitalWrite(LED_GREEN, LOW);
    pcf8574.digitalWrite(LED_BLUE, LOW);
    // Temperature proximity sensor
}

void loop()
{
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
            card_code = card_code.substring(1);
            card_code.replace(" ", "");
            String code_json = "{\"code\":\"" + card_code + "\", \"joining\": 1 }";
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
            card_code = card_code.substring(1);
            card_code.replace(" ", "");
            String code_json = "{\"code\":\"" + card_code + "\", \"joining\": 0 }";
            Serial.println(code_json);
            delay(500);
        }
    }
    int value = 0;
    value = digitalRead(PS_SANITIZER);
    if (value == LOW)
    { // ? HIGH or LOW
        if (readSensor() > 5)
        {
            pcf8574.digitalWrite(SANITIZER_PUMP, HIGH);
            delay(1000);
            pcf8574.digitalWrite(SANITIZER_PUMP, LOW);
            int dispenser_percentage = readSensor();
            Serial.print("{\"dispenser_percentage\": \"");
            Serial.print(dispenser_percentage);
            Serial.println("\" }");
            delay(1000);
        }
    }
    value = 1;
    value = digitalRead(PS_TEMPERATURE);
    if (value == LOW)
    {
        //float temperature = mlx.readObjectTempC() * 1.15;
        Serial.print("{\"temperature\": \"");
        //Serial.print(temperature);
        Serial.println("\"}");
        delay(500);
    }
    if (Serial.available() > 0)
    {
        Serial.println("Holis");
        String data = Serial.readStringUntil('\n');
        DeserializationError error = deserializeJson(doc, data);
        bool var = doc["allowed"];
        Serial.println(var);
        if (!error)
        {
            if (doc["allowed"])
            {
                Serial.println("allowed");
                pcf8574.digitalWrite(RELAY_LOCK, HIGH);
                pcf8574.digitalWrite(LED_GREEN, HIGH);
                delay(2000);
                pcf8574.digitalWrite(RELAY_LOCK, LOW);
                pcf8574.digitalWrite(LED_GREEN, LOW);
            }
            else
            {
                pcf8574.digitalWrite(LED_RED, HIGH);
                delay(2000);
                pcf8574.digitalWrite(LED_RED, LOW);
                //myLED.defaultColor("");
            }

            if (doc["led_color"] != None)
            {
                //doc["led_color"]
            }
        }
    }
    yield();
}

int readSensor()
{
    pcf8574.digitalWrite(SANITIZER_LEVEL, HIGH); // Turn the sensor ON
    delay(10);                                   // Wait 10 milliseconds
    int val = analogRead(SANITIZER_LEVEL_SENSOR);
    Serial.println(val);
    pcf8574.digitalWrite(SANITIZER_LEVEL, LOW); // Turn the sensor OFF
    return val * 100 / 560;                     // Return current reading in percentage (0-1023 = 0%-100%)
}