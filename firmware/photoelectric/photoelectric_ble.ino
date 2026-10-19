//Code modified from the book IoT Projects with Arduino Nano 33 BLE Sense (Kurniawan, 2021, pp. 111–136)
#include <ArduinoBLE.h>
int photoElectric = 13;
int ledPin=2;
int readings[100];
int currentIndex = 0;
int loopN = 0;

BLEService sensorService("16150f38-e7a9-4fe1-ae08-00000photo_electric");
BLEStringCharacteristic phelSensor("ff99948c-18ff-4ed8-942e-00000photo_electric", BLERead | BLENotify, 15);



void setup() {
  Serial.begin(9600);
  pinMode(photoElectric, INPUT);
  pinMode(ledPin, OUTPUT);
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1)
      ;
  }
  BLE.setLocalName("photo_electric_room1c1");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(phelSensor);
  BLE.addService(sensorService);
  phelSensor.writeValue("Ok");

  for (int i = 0; i < 100; i++) {
    readings[i] = 0;
  }


}
// the loop routine runs over and over again forever:
void loop() {
  // read the input pin:
  int sensorState = digitalRead(photoElectric);

  // store the reading in the array:
  readings[currentIndex] = sensorState;
  // move to the next position in the array:
  currentIndex = (currentIndex + 1) % 10;
  delay(1);
  bool allZeros = true;

    if (currentIndex == 9) {
      for (int i = 0; i < 100; i++) {
        if (readings[i] != 0) {
        allZeros = false;
      }
    }
    if (allZeros == true){
      BLE.advertise();
      Serial.println("Alarm!");
      digitalWrite(ledPin, HIGH);
      delay(10000);
    }

    else {
      BLE.stopAdvertise();
      Serial.println("Ok");
      digitalWrite(ledPin, LOW);
    }
  }
  loopN += 1;
  if (loopN == 1000){
    ESP.restart();
  }
}