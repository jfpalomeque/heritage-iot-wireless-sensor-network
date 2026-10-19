# Deployment notes

## Raspberry Pi hub

```bash
cd hub
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp ../configs/wsn_config.example.json /secure/location/wsn_config.json
export WSN_CONFIG=/secure/location/wsn_config.json
python main.py
```

The historical scripts assume a Linux/Raspberry Pi BLE environment. Pair and validate each node before configuring routines or actions. Keep `events_table.csv`, captured images, runtime `data.json`, and private configuration outside version control.

## Camera node

Copy `firmware/camera/` into an Arduino sketch folder, set local Wi-Fi credentials, select the correct ESP32-CAM board configuration, and upload. Set the node's private address only in the runtime hub configuration.

## Optional Azure services

Set `AZURE_STORAGE_CONNECTION_STRING`, `AZURE_CSV_CONTAINER`, and `AZURE_IMAGES_CONTAINER` in the hub runtime environment before enabling the uploader. For the Streamlit dashboard, set `AZURE_SQL_SERVER`, `AZURE_SQL_DATABASE`, `AZURE_SQL_USERNAME`, and `AZURE_SQL_PASSWORD`.

Do not expose the camera HTTP service to the public internet. Use network segmentation, least-privilege cloud credentials, and encryption/authentication appropriate to the deployment.
