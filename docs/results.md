# Recorded results

This directory separates preserved machine output from structured transcriptions of the historical experiment.

## Preserved output files

- `binary_results.json` and `multi_modal_results.json` are historical evaluation outputs.
- `hf_results.json` contains the preserved Hugging Face evaluation records for binary and eight-class ViT runs. The historical key `multimodal` is retained inside that raw artifact because it is not rewritten.

The preserved ViT records report epoch 3.0. The recovered training scripts currently specify five epochs. This discrepancy is documented rather than silently reconciled. The reported 80% training-proportion results are 0.9533333333333334 accuracy for the eight-class ViT run and 1.0 for the binary run, with recorded runtimes of 14:47.082 and 7:50.018 respectively.

## Structured historical summaries

- `deployment_summary.csv`: duration and event-log counts.
- `wsn_performance.csv`: charge consumption, acquisition-script runtime, and RSSI.
- `model_results.csv`: model-level eight-class and binary accuracies and training times.
- `clip_class_results.csv`: historical class-level CLIP results.

These CSVs are transcriptions, not newly generated experimental outputs. The `source` column identifies their provenance.

## Interpretation

The model families did not share a single identical preprocessing and balancing protocol. The bespoke eight-class loader did not rebalance classes, the bespoke binary loader downsampled the majority class, and the ViT workflow balanced each class before splitting. No fixed split seed was specified in the recovered scripts. The values should therefore be treated as exploratory proof-of-concept results rather than a controlled benchmark ranking.

The historical zero-shot CLIP configuration contained duplicated `eating` and `drinking` entries in the negative prompt list. That exact list is retained in `configs/image_labels.historical.json`. The default configuration was cleaned for future runs, but the historical CLIP metrics were not recomputed.
