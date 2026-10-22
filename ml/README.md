# Machine-learning scripts

`training/` contains the recovered Hugging Face ViT fine-tuning scripts for binary and eight-class classification. `inference/` contains ViT and CLIP experiment scripts, and `diy_anns/` contains exploratory CNN/FNN/RNN work.

These are preserved research scripts, not a packaged training pipeline. Configure dataset and output paths locally. The curated 750-image dataset is already included at repository root in `image_dataset_binary/` and `image_dataset_multimodal/`. Trained model binaries are intentionally not distributed and should be generated locally from the provided training scripts.

See `../data/README.md`, `../models/README.md`, and `../docs/reproducibility.md`.
