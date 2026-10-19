# Architecture

The prototype has three layers:

1. **Wireless sensor network.** ESP32/Arduino-compatible nodes report temperature/humidity, PIR movement, sound, ultrasonic distance, and photoelectric events over Bluetooth Low Energy. ESP32-CAM nodes provide local HTTP capture endpoints.
2. **Computing hub.** A Raspberry Pi discovers BLE devices, records events, invokes configured camera actions, optionally classifies captured images, and serves a local Flask dashboard.
3. **Optional cloud layer.** Azure Blob Storage can archive images and CSV logs; an Azure SQL/Streamlit dashboard can visualise events.

The hub reads a JSON configuration to identify devices and scheduled routines. The example configuration is deliberately inert and contains no deployment identifiers. The historical runner executes trusted Python expressions from this configuration; therefore the configuration file must be treated as executable, administrator-controlled input.

For the research rationale, evaluation, costs, and experimental setup, see the [arXiv preprint](https://arxiv.org/abs/2508.00849).
