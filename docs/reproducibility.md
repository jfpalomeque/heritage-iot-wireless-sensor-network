# Reproducibility

This repository is a curated technical companion to an archived MSc project. It retains source code, Fritzing hardware sketches, configurations, label definitions, the complete 750-image behavioural dataset, and recorded metric files while intentionally excluding secrets, raw operational logs, and trained model binaries.

## Source selection

- `hub/` is based on the more complete `Final_report/rpi` implementation.
- `ml/` is based on `Final_report/PC`; several files were byte-identical to copies in `Final_Version`.
- `firmware/` is based on the final-report node sketches, with camera Wi-Fi credentials replaced by placeholders.
- Original JSON result artifacts in `results/` are preserved without rewriting.
- `configs/wsn_config.historical.example.json` is a sanitized transcription of the deployment configuration documented in the MSc report appendix. Private network addresses were replaced.

## Curation fixes

The companion corrects several code defects found during manuscript and repository audit. These changes improve the curated code but do not alter the historical experiment record:

- `hub/app.py` now writes edited configuration back to the configuration file rather than overwriting dashboard data, and validates submitted JSON.
- `hub/azure_blob_uploader.py` no longer references the undefined `new_csv_file_path` variable and now protects the current dashboard image for every configured room.
- `hub/data_reload.py` no longer depends on specific historical node identifiers. It parses event records by event type and characteristic/trigger fields and handles CSV rotation.
- `hub/actions.py` resolves the default labels file from the repository and requires `VIT_MODEL_PATH` explicitly because model binaries are not shipped in Git.
- the default CLIP label file removes duplicate negative prompt entries; the exact historical list remains available separately.

## Historical training discrepancy

The recovered ViT training scripts specify five epochs, while all preserved result records for the reported ViT runs store `epoch: 3.0`. The repository does not infer which later editing step produced this mismatch. The manuscript reports the preserved historical outcomes and does not claim that the current training scripts exactly recreate those runs.

## Reproducing the training procedure

The complete behavioural dataset and recovered training scripts are included so that the binary and eight-class ViT training procedures can be rerun. Trained model binaries are intentionally not distributed.

The historical experiments did not preserve a deterministic train/evaluation split seed. Consequently, a new run can reproduce the documented procedure but should not be expected to generate the exact historical split, trained weights, or reported metrics.

## Known limitations

- Exact dependency versions were not captured in the original project.
- Hugging Face APIs used by the training scripts are historical and may require adaptation.
- No deterministic random seed was specified for the historical train/evaluation splits.
- Bespoke and ViT pipelines used different class-balancing procedures.
- The original Azure Data Factory pipeline export and SQL DDL were not preserved. `cloud/schema.sql` is a compatible reference schema, not recovered infrastructure.
- Runtime configuration executes trusted Python expressions through `exec`.
- Camera HTTP endpoints in the prototype are unauthenticated and must not be exposed directly to untrusted networks.
- Trained model weights are not distributed.

Reported metrics are the historical experiment record. New comparative claims should be based on newly versioned training runs with documented split seeds, dependencies, checksums, and evaluation outputs.
