# Behavioural image dataset

This repository includes the complete **750-image behavioural dataset** used in the binary and eight-class image-classification experiments described in the manuscript.

## Dataset provenance

The images show the author performing staged behaviours in the controlled experimental setup. The author is the sole photographed participant and holds the rights to the images.

The eight behavioural classes are:

| Class | Images | Binary label |
| --- | ---: | --- |
| `carrying_a_blunt_object` | 100 | negative |
| `walking_a_dog` | 100 | negative |
| `drinking` | 100 | negative |
| `eating` | 100 | negative |
| `carrying_a_knife` | 50 | negative |
| `taking_pictures` | 100 | positive |
| `touching` | 100 | negative |
| `watching_calm` | 100 | positive |
| **Total** | **750** | **550 negative / 200 positive** |

These images were produced with one participant in one controlled setting. They are not representative of real museum visitors and should not be used to infer generalisable behaviour-recognition performance.

## Repository layout

The same 750 source images are retained in the two historical experimental layouts:

- `image_dataset_multimodal/`: eight-class layout used by the historical multiclass experiments. The directory name is preserved for reproducibility, although the manuscript now uses the clearer term **eight-class** rather than "multimodal".
- `image_dataset_binary/`: binary positive/negative layout containing the same 750 images grouped into **550 negative** and **200 positive** examples.

The files in the two directories are duplicates by content, organised differently to reproduce the historical training workflows. The larger working/source image directory used during project development is deliberately not included in the publication repository because it contains additional and duplicate images that were not part of the reported 750-image experimental dataset.

## Rights and licensing

Copyright in the behavioural images is held by Juan Francisco Palomeque-Gonzalez.

The 750-image behavioural dataset is released under the **Creative Commons Attribution 4.0 International licence (CC BY 4.0)**:

https://creativecommons.org/licenses/by/4.0/

Reuse, redistribution, and adaptation are permitted under the terms of CC BY 4.0, including the requirement to provide appropriate attribution and indicate whether changes were made.

The repository's MIT licence applies to software only and does not replace the CC BY 4.0 licence for the image dataset.

## Reproducibility notes

The historical experiments did not preserve a deterministic train/evaluation split seed. Different model pipelines also used different balancing procedures. The complete dataset and training scripts therefore support reproduction of the documented training procedure and future re-analysis, but they do not guarantee recreation of the exact historical split, trained weights, or reported metrics.

Trained model weights are intentionally not distributed. The final tagged GitHub release, including both dataset layouts, will be archived on Zenodo with the rest of the research companion.
