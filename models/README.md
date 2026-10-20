# Model status

The archived project contains duplicate fine-tuned ViT checkpoint copies of approximately 327 MiB each. Model binaries are intentionally excluded from Git.

If models are released separately, publish one selected binary-classification model and one selected eight-class model through a stable repository such as Zenodo or Hugging Face. Each release should provide model weights, configuration, preprocessing files, a model card, dataset version, class mapping, intended-use limitations, SHA-256 checksums, and a compatible licence.

The hub requires `VIT_MODEL_PATH` to point to a local model directory before image classification is enabled. No model release DOI or URL is claimed until an external deposit has actually been created.
