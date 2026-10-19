//Code modified from the book IoT Projects with Arduino Nano 33 BLE Sense (Kurniawan, 2021, pp. 111–136)
#include <ArduinoBLE.h>

int inputPin = 13;   // Sensor input
int pirState = LOW;  // we start, assuming no motion detected
int val = 0;         // variable for reading the pin status
int loopN = 0;
#define LED_PIN 2

BLEService sensorService("16150f38-e7a9-4fe1-ae08-00000pirnode");
BLEStringCharacteristic pirSensor("ff99948c-18ff-4ed8-942e-00000pirnode", BLERead | BLENotify, 15);



void setup() {
  pinMode(inputPin, INPUT);  // declare sensor as input
  pinMode(LED_PIN, OUTPUT);
  Serial.begin(9600);
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1)
      ;
  }
  BLE.setLocalName("pirNoderoom1");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(pirSensor);
  BLE.addService(sensorService);
  pirSensor.writeValue("Motion detected!");
}

void loop() {
  val = digitalRead(inputPin);  // read input value
  if (val == HIGH) {            // check if the input is HIGH

    if (pirState == LOW) {
      BLE.advertise();
      Serial.println("Motion detected!");
      pirSensor.writeValue("Motion detected!");
      digitalWrite(LED_PIN, HIGH);  // Only show message on change
      pirState = HIGH;
      loopN += 1;
      delay(10000);
    }
  } else {
    if (pirState == HIGH) {
      BLE.stopAdvertise();
      Serial.println("Motion ended!");
      pirSensor.writeValue("Motion ended!");
      digitalWrite(LED_PIN, LOW);
      pirState = LOW;
    }
  }
  if (loopN == 1000){
    ESP.restart();
  }
}
