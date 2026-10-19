//Code modified from the book IoT Projects with Arduino Nano 33 BLE Sense (Kurniawan, 2021, pp. 111–136)
#include "DHT.h"
#include <ArduinoBLE.h>
#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

BLEService sensorService("16150f38-e7a9-4fe1-ae08-48464baf25b2");
BLEStringCharacteristic temperatureSensorLevel("ff99948c-18ff-4ed8-942e-512b9b24b6da", BLERead | BLENotify,15);
BLEStringCharacteristic humiditySensorLevel("8084aa6b-6cae-461f-9540-e1a5768de49d", BLERead | BLENotify,15);

float oldTemperature = 0;
float oldHumidity = 0;
int loopN = 0;

void setup() {
  Serial.begin(9600);
  Serial.println("DHT22 test!");
  dht.begin();

  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1);
  }

  BLE.setLocalName("TempHumiditySensor01");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(temperatureSensorLevel);
  sensorService.addCharacteristic(humiditySensorLevel);
  BLE.addService(sensorService);
  temperatureSensorLevel.writeValue( String(oldTemperature));
  humiditySensorLevel.writeValue(String(oldHumidity));

  BLE.advertise();
  Serial.println("Bluetooth device active, waiting for connections...");

}

void loop() {
 BLEDevice central = BLE.central();
  if (central) {
  Serial.print("Connected to central: ");
  Serial.println(central.address());
    while (central.connected()) {
    //long currentMillis = millis();
    updateTempHumidityLevel ();
    delay(300);
    }
  Serial.print("Disconnected from central: ");
  Serial.println(central.address());
    }
    loopN += 1;
    if (loopN == 100000){
    ESP.restart();
  }
}
  void updateTempHumidityLevel() {
  delay(2000);

  float h = dht.readHumidity();
  float t = dht.readTemperature();

  if (isnan(h) || isnan(t)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.println();

  if (t != oldTemperature) {
  temperatureSensorLevel.writeValue(String(t));
  oldTemperature = t;
  }

  if (h != oldHumidity) {
  humiditySensorLevel.writeValue(String(h));
  oldHumidity = h;
  }
}
