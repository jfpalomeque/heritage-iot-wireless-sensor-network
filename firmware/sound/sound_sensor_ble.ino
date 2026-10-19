//Code modified from the book IoT Projects with Arduino Nano 33 BLE Sense (Kurniawan, 2021, pp. 111–136)
#include <ArduinoBLE.h>

int ledPin=2;
int sensorPin=4;
boolean val =0;
int loopN = 0;

BLEService sensorService("16150f38-e7a9-4fe1-ae08-00000soundnode");
BLEStringCharacteristic soundSensor("ff99948c-18ff-4ed8-942e-00000soundnode", BLERead | BLENotify, 15);

void setup(){
  pinMode(ledPin, OUTPUT);
  pinMode(sensorPin, INPUT);
  Serial.begin (9600);
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1)
      ;
  }
  BLE.setLocalName("soundNoderoom1");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(soundSensor);
  BLE.addService(sensorService);
  soundSensor.writeValue("Sound not detected!");
}

void loop (){
  val =digitalRead(sensorPin);

  if (val==LOW) {
    BLE.advertise();
    Serial.println ("Sound detected!");
    soundSensor.writeValue("Sound detected!");
    digitalWrite(ledPin, HIGH);
    delay(10000);
  }

  else {
    BLE.stopAdvertise();
    Serial.println ("Sound not detected!");
    digitalWrite(ledPin, LOW);
  }

  loopN += 1;
  if (loopN == 1000){
    ESP.restart();
  }
}
