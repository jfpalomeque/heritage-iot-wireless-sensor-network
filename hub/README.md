# Raspberry Pi computing hub

The files in this directory are the recovered prototype implementation for BLE sensor reads, event logging, camera acquisition, local dashboard, and optional image/cloud actions.

Run from this directory after installing `requirements.txt`, setting `WSN_CONFIG` to a private copy of `../configs/wsn_config.example.json`, and configuring only trusted routines/actions. The dashboard can be started separately with `python app.py`.

`azure_blob_uploader.py` now requires Azure credentials through environment variables and no longer uploads anything when imported. Captured images, logs, model weights, and deployment configuration are ignored by Git.
