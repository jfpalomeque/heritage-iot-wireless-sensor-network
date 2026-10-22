# Modular IoT Monitoring for Cultural Heritage

Research companion to *A Modular, Low-Cost IoT System for Environmental and Behavioural Monitoring in Cultural Heritage Sites* ([arXiv:2508.00849](https://arxiv.org/abs/2508.00849)) and the revised CAA2026 proceedings manuscript *Low-Cost IoT Monitoring for Cultural Heritage: Design and Evaluation of a Modular Wireless Sensor Network*.

Developed from the MSc Advanced Computing final project at the University of the West of Scotland (2023-2024). The project was awarded **Distinction** and received the **UWS Court Medal for academic performance**.

The prototype combines Bluetooth Low Energy sensor nodes, ESP32-CAM nodes, a Raspberry Pi computing hub, optional Azure services, and image-classification experiments for environmental and visitor-related monitoring in a simulated heritage setting.

> **Research prototype.** This repository preserves and curates the experimental implementation. It is not production-ready security or conservation-monitoring software. Validate sensors, security controls, model performance, privacy safeguards, and long-term reliability before any real deployment.

## Contents

- `firmware/` - Arduino sketches for ESP32 sensor and camera nodes.
- `hub/` - Raspberry Pi BLE collection, event processing, local Flask dashboard, optional image analysis, and Azure Blob uploader.
- `ml/` - fine-tuning, inference, and exploratory neural-network scripts.
- `cloud/` - optional Streamlit/Azure SQL dashboard plus documentation of the unrecovered cloud-infrastructure boundary.
- `hardware/` - Fritzing circuit sketches and a reconstructed component inventory.
- `configs/` - minimal configuration, sanitized historical deployment configuration, and image-label definitions.
- `results/` - preserved ViT JSON outputs and structured historical result summaries.
- `docs/` - architecture, deployment, reproducibility, results, and release notes.

## Reproducibility status

The repository distinguishes three categories of material:

1. **Preserved artifacts**, such as the historical ViT JSON result files.
2. **Curated recovered code**, where clearly identified implementation defects were corrected without changing the historical result record.
3. **Structured transcriptions**, such as CSV summaries reconstructed from the MSc experimental documentation.

See [docs/reproducibility.md](docs/reproducibility.md) and [docs/results.md](docs/results.md) before attempting to reproduce or compare the reported results.

## Quick start

1. Read [docs/architecture.md](docs/architecture.md) and [docs/deployment.md](docs/deployment.md).
2. Use `configs/wsn_config.example.json` as a safe minimal scaffold, or consult `configs/wsn_config.historical.example.json` to inspect the original experimental topology and schedules.
3. Install the relevant dependency set from `hub/requirements.txt`, `ml/requirements.txt`, or `cloud/requirements.txt`.
4. Keep Wi-Fi credentials, cloud credentials, runtime logs, images, and private deployment addresses outside version control.
5. Set `VIT_MODEL_PATH` explicitly if image classification is enabled because model binaries are not included.

## Historical results

Machine-readable summaries are provided for deployment counts, WSN performance, model-level classification results, and class-level CLIP results. These are historical records, not newly rerun experiments. Model families used different balancing procedures and no fixed split seed was preserved, so their accuracies are exploratory rather than a strict benchmark.

The preserved ViT output files record epoch 3.0 for the reported runs, whereas the recovered training scripts currently specify five epochs. This discrepancy is documented in [docs/reproducibility.md](docs/reproducibility.md).

## Data and models

The recovered binary, multiclass, and original image datasets are versioned in the repository root. The curated behavioural dataset and its rights statement are documented in [data/README.md](data/README.md). Confirm that the release conditions remain satisfied before changing the repository visibility. Trained model weights are not included; see [models/README.md](models/README.md).

## Release status

This repository is currently being prepared for the CAA2026 companion release. The final public tag and Zenodo software DOI should be created only after the model availability decision and final manuscript DOI are resolved. See [docs/release-checklist.md](docs/release-checklist.md).

## Citation

`CITATION.cff` currently points to the arXiv preprint. It should be updated to the final CAA2026 DOI once that DOI exists.

## Licence

Code is available under the [MIT License](LICENSE). Dataset and model licences, if separate releases are created, must be stated independently.
