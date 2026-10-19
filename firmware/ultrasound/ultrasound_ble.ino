// Modified from IoT Projects with Arduino Nano 33 BLE Sense

#include <ArduinoBLE.h>

int triggerPin = 12;
int echoPin = 13;
int ledPin=2;

//define sound speed in cm/uS
#define SOUND_SPEED 0.034

BLEService sensorService("16150f38-e7a9-4fe1-ae08-00distance01");
BLEStringCharacteristic distanceSensor("ff99948c-18ff-4ed8-942e-00distance01", BLERead | BLENotify,15);

long duration = 0;
float distanceCm = 0;
int loopN = 0;

void setup(){
  pinMode(ledPin, OUTPUT);
  pinMode(triggerPin, OUTPUT); // Sets the triggerPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  Serial.begin (9600);
  if (!BLE.begin()) {
    Serial.println("starting BLE failed!");
    while (1)
      ;
  }
  BLE.setLocalName("distanceSensor1");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(distanceSensor);
  BLE.addService(sensorService);
  distanceSensor.writeValue("Distance sensor active");
}

void loop (){
  updateDistance();

  if (distanceCm > 0) {
    BLE.setLocalName(setName().c_str());
    BLE.advertise();
    Serial.println ("Distance"  + String(distanceCm));
    distanceSensor.writeValue(String(distanceCm));

    delay(10000);
  }

  else {
    BLE.setLocalName("distanceSensor1");
    BLE.advertise();
    Serial.println ("Error, distance: " + String(distanceCm));
    digitalWrite(ledPin, LOW);
  }

  loopN += 1;
  if (loopN == 1000){
    ESP.restart();
  }
}

void updateDistance() {

  // Wait a few seconds between measurements.
  delay(2000);
  // Clears the triggerPin
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);
  // Sets the triggerPin on HIGH state for 10 micro seconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance
  distanceCm = duration * SOUND_SPEED/2;
  }

String setName(){

  return "distanceSensor1_" + String(distanceCm);
}
