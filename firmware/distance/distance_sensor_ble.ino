#include <ArduinoBLE.h>

// Define constants for pin connections
const int triggerPin = 12;
const int echoPin = 13;
const int ledPin = 2;

// Define sound speed in cm/uS
const float SOUND_SPEED = 0.034;

// Define BLE service and characteristic UUIDs
const char* sensorServiceUUID = "16150f38-e7a9-4fe1-ae08-00distance01";
const char* distanceSensorUUID = "ff99948c-18ff-4ed8-942e-00distance01";

BLEService sensorService(sensorServiceUUID);
BLEStringCharacteristic distanceSensor(distanceSensorUUID, BLERead | BLENotify, 15);

// Variables to store distance and loop counter
float distanceCm = 0;
int loopN = 0;

void setup() {
  // Initialize serial communication
  Serial.begin(9600);

  // Initialize pin modes
  pinMode(ledPin, OUTPUT);
  pinMode(triggerPin, OUTPUT);
  pinMode(echoPin, INPUT);

  // Initialize BLE
  if (!BLE.begin()) {
    Serial.println("Starting BLE failed!");
    while (1);
  }

  // Set up BLE service and characteristic
  BLE.setLocalName("distanceSensor1");
  BLE.setAdvertisedService(sensorService);
  sensorService.addCharacteristic(distanceSensor);
  BLE.addService(sensorService);
  distanceSensor.writeValue("Distance sensor active");
}

void loop() {
  // Update distance measurement
  updateDistance();

  if (distanceCm > 0) {
    // Update BLE local name and advertise
    BLE.setLocalName(setName().c_str());
    BLE.advertise();

    // Write distance value to characteristic
    distanceSensor.writeValue(String(distanceCm));

    // Print distance to serial console
    Serial.println("Distance: " + String(distanceCm));

    // Delay for 10 seconds
    delay(10000);
  } else {
    // Set default BLE local name and advertise
    BLE.setLocalName("distanceSensor1");
    BLE.advertise();

    // Print error message to serial console
    Serial.println("Error, distance: " + String(distanceCm));

    // Turn off LED
    digitalWrite(ledPin, LOW);
  }

  // Increment loop counter and restart ESP if necessary
  loopN += 1;
  if (loopN == 1000) {
    ESP.restart();
  }
}

void updateDistance() {
  // Wait for 2 seconds between measurements
  delay(2000);

  // Clear trigger pin
  digitalWrite(triggerPin, LOW);
  delayMicroseconds(2);

  // Set trigger pin high for 10 microseconds
  digitalWrite(triggerPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(triggerPin, LOW);

  // Read echo pin and calculate distance
  long duration = pulseIn(echoPin, HIGH);
  distanceCm = duration * SOUND_SPEED / 2;
}

String setName() {
  return "distanceSensor1_" + String(distanceCm);
}