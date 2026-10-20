# Deployment notes

## Raspberry Pi hub

Create a runtime directory outside version control and copy either the minimal scaffold or the sanitized historical configuration into it.

    cd hub
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

    mkdir -p /secure/location/iot-runtime
    cp ../configs/wsn_config.example.json /secure/location/iot-runtime/wsn_config.json
    cp ../configs/data.example.json /secure/location/iot-runtime/data.json

    export WSN_RUNTIME_DIR=/secure/location/iot-runtime
    export WSN_CONFIG=/secure/location/iot-runtime/wsn_config.json
    export WSN_DATA=/secure/location/iot-runtime/data.json
    export WSN_EVENTS=/secure/location/iot-runtime/events_table.csv

    python main.py

The historical scripts assume a Linux/Raspberry Pi BLE environment. Configuration is trusted executable input because routines and actions are evaluated by the recovered runner. Do not accept configuration from untrusted users.

For the original experimental topology, schedules, and actions, consult `configs/wsn_config.historical.example.json`. Replace all network placeholders before use. The historical key `distance_senors` is intentionally preserved for compatibility with the recovered code.

## Local dashboard

Run `python app.py` with the same runtime environment variables. The dashboard editor validates JSON and writes changes to `WSN_CONFIG`.

## Image classification

Model binaries are not stored in Git. Set:

    export IMAGE_LABELS_PATH=/path/to/configs/image_labels.json
    export VIT_MODEL_PATH=/path/to/local/fine-tuned-model

before enabling camera actions that call the ViT classifier.

## Camera node

Copy `firmware/camera/` into an Arduino sketch folder, set local Wi-Fi credentials, select the correct ESP32-CAM board configuration, and upload. Configure the node's private address only in runtime configuration.

The prototype camera server has no authentication. Keep it on a controlled local network and add appropriate authentication, segmentation, transport protection, and privacy controls for any real deployment.

## Optional Azure services

Set `AZURE_STORAGE_CONNECTION_STRING`, `AZURE_CSV_CONTAINER`, and `AZURE_IMAGES_CONTAINER` before enabling the uploader. For Streamlit, set `AZURE_SQL_SERVER`, `AZURE_SQL_DATABASE`, `AZURE_SQL_USERNAME`, and `AZURE_SQL_PASSWORD`.

The original Azure Data Factory definition was not recovered. See `cloud/README.md` and `cloud/schema.sql` for the documented limits of the cloud companion.
