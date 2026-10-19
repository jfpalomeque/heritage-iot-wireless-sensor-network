# Firmware

Each directory holds one Arduino sketch used in the prototype. Install the appropriate board package and libraries before compilation:

- ESP32 / ESP32-CAM: ESP32 Arduino core, `ESPAsyncWebServer`, and `base64` support used by the camera sketch.
- DHT22 node: `DHT` and `ArduinoBLE`.
- Remaining BLE nodes: `ArduinoBLE`.

The camera sketch intentionally contains placeholder Wi-Fi values. Set them only in a local, untracked copy. The device exposes capture, download, and delete HTTP endpoints; deploy it only on a controlled network.
