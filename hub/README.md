# Raspberry Pi computing hub

This directory contains the curated prototype implementation for BLE sensor reads, event logging, camera acquisition, the local Flask dashboard, optional image classification, and Azure Blob archiving.

Use a runtime directory outside version control. The main runner reads `WSN_CONFIG`; the dashboard can additionally use `WSN_RUNTIME_DIR`, `WSN_DATA`, and `WSN_EVENTS`. See `docs/deployment.md`.

Two configuration examples are available:

- `configs/wsn_config.example.json`: minimal and deliberately inert.
- `configs/wsn_config.historical.example.json`: sanitized reconstruction of the experimental deployment, with network addresses removed.

Model binaries are not included. Set `VIT_MODEL_PATH` before enabling the ViT camera action. Captured images, logs, model weights, and private deployment configuration are ignored by Git.

The runner still uses `exec` for trusted configuration expressions because that is part of the recovered prototype architecture. Do not expose configuration editing to untrusted users.
