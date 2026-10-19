# Modular IoT Monitoring for Cultural Heritage

Open technical companion to *A Modular, Low-Cost IoT System for Environmental and Behavioural Monitoring in Cultural Heritage Sites* ([arXiv:2508.00849](https://arxiv.org/abs/2508.00849)).

Developed as the MSc Advanced Computing final project at the University of the West of Scotland (2023–2024). The project was awarded **Distinction** and received the **UWS Court Medal for academic performance**. It was presented as *“Low-Cost IoT Monitoring for Cultural Heritage: Design and Evaluation of a Modular Wireless Sensor Network.”*

The prototype combines Bluetooth Low Energy sensor nodes, ESP32-CAM nodes, a Raspberry Pi computing hub, optional Azure services, and image-classification experiments for environmental and behavioural monitoring in heritage settings.

> **Research prototype.** This repository preserves and documents the MSc project implementation. It is not production-ready security or conservation-monitoring software. Validate sensors, security controls, model performance, and privacy safeguards before any real deployment.

## Contents

- `firmware/` — Arduino sketches for ESP32 sensor and camera nodes.
- `hub/` — Raspberry Pi BLE collection, event processing, local Flask dashboard, optional image analysis and Azure Blob uploader.
- `ml/` — fine-tuning, inference, and exploratory neural-network scripts.
- `cloud/` — optional Streamlit/Azure SQL dashboard.
- `hardware/fritzing/` — Fritzing circuit sketches.
- `configs/` — non-secret example configurations and label definitions.
- `results/` — recorded experiment result JSON files.
- `docs/` — architecture, setup, reproducibility, data, and results notes.

## Quick start

1. Read [`docs/architecture.md`](docs/architecture.md) and [`docs/deployment.md`](docs/deployment.md).
2. Copy `configs/wsn_config.example.json` to a private runtime location and replace placeholder BLE identifiers and addresses.
3. Install the relevant dependency set (`hub/requirements.txt`, `ml/requirements.txt`, or `cloud/requirements.txt`).
4. Put Wi-Fi credentials in the camera sketch **locally**; do not commit them.
5. Run the hub from `hub/` with `WSN_CONFIG=/path/to/private-config.json python main.py`.

## Data and models

Raw images and trained model weights are intentionally not stored in Git. They are to be published as versioned external releases; see [`data/README.md`](data/README.md) and [`models/README.md`](models/README.md). The source archive contained duplicate checkpoints and image collections, so releases must use the manifest/checksum process described there.

## Citation

Please cite the arXiv preprint. A `CITATION.cff` file is included for GitHub citation support.

## Licence

Code is available under the [MIT License](LICENSE). Dataset and model licences must be stated separately in their respective releases.
