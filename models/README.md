# Model release

The archived project contains duplicate fine-tuned ViT checkpoint copies of approximately 327 MiB each. Model binaries are intentionally excluded from Git.

Publish one selected binary-classification model and one selected multiclass model through Hugging Face or Zenodo. Each release should provide:

- model weights, `config.json`, and preprocessor configuration;
- model card, training dataset version, class mapping, and intended-use limitations;
- SHA-256 checksum;
- licence compatible with the base model and dataset;
- a stable download URL placed in this document.

The hub's image-analysis path must be set to the downloaded local model directory before use.
