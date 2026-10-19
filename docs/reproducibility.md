# Reproducibility

This repository is a curated technical companion to an archived MSc project. It retains source code, Fritzing hardware sketches, configurations, label definitions, and recorded metric files, while intentionally excluding secrets, raw operational logs, images, model binaries, and Office documents.

## Source selection

- `hub/` is based on the more complete `Final_report/rpi` implementation.
- `ml/` is based on `Final_report/PC`; several files were byte-identical to copies in `Final_Version`.
- `firmware/` is based on the final-report node sketches, with the camera Wi-Fi values replaced by placeholders.
- `results/` contains the original JSON output files without alteration.

## Known limitations

- Dependency versions were not captured in the original project. The requirement files identify packages, not proven reproducible pins.
- Training scripts use historical Hugging Face APIs and may need version adaptation.
- The scripts use fixed class-folder conventions and do not yet create deterministic train/test splits.
- Runtime configuration invokes trusted Python expressions. Do not accept configuration from untrusted users.
- Reported metrics should be treated as the historical experiment record; rerun evaluation from a documented dataset/model release before making new comparative claims.
