# Model status

Trained model binaries are intentionally not distributed with this repository.

The repository provides the complete 750-image behavioural dataset and the recovered training scripts used for the binary and eight-class ViT experiments. Users can retrain the classifiers from these materials.

The historical experiments did not preserve a deterministic train/evaluation split seed, and different model pipelines used different balancing procedures. Retraining therefore reproduces the documented training procedure, but it is not expected to recreate the exact historical model weights or reported metrics.

The preserved historical result files remain available in `results/`. The recovered ViT training scripts specify five epochs, while the preserved historical ViT result records report epoch 3.0; this discrepancy is documented in [../docs/reproducibility.md](../docs/reproducibility.md).

If image classification is enabled in the hub after retraining, `VIT_MODEL_PATH` must point to the locally generated model directory.
