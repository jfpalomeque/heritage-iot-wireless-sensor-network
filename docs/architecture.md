# Architecture

The prototype has three layers:

1. **Wireless sensor network.** ESP32-WROOM-32-based nodes report temperature/humidity, PIR movement, sound, ultrasonic distance, and photoelectric events over Bluetooth Low Energy. Three ESP32-CAM nodes with OV2640 cameras provide local HTTP capture endpoints over Wi-Fi.
2. **Computing hub.** A Raspberry Pi 4 Model B with 4 GB RAM discovers BLE devices, records events, invokes configured actions, acquires camera images, optionally classifies them locally, and serves a Flask dashboard.
3. **Optional cloud layer.** Azure Blob Storage can archive images and CSV logs; the experimental workflow used Azure Data Factory to move event records to Azure SQL, with Streamlit for remote visualisation.

The hub reads JSON configuration describing nodes, scheduled routines, and trigger-action relationships. The minimal example is deliberately inert. A separate sanitized historical example records the original experimental topology and schedules without private network addresses.

The recovered runner executes trusted Python expressions from configuration. This is a research-prototype design, not a safe general-purpose plugin system, and the configuration file must be treated as executable administrator-controlled input.

The camera endpoints are also research-prototype HTTP services without authentication. They should remain on a controlled local network unless replaced or hardened for operational deployment.
