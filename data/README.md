# Behavioural image dataset

This repository is intended to include the complete behavioural image dataset used in the binary and eight-class image-classification experiments described in the manuscript.

## Dataset provenance

The dataset contains **750 staged images** of the author, who is the sole photographed participant and holds the rights to the images. Images were created in the controlled experimental setup used for the MSc project.

The eight behavioural classes are:

| Class | Images | Binary label |
| --- | ---: | --- |
| `blunt_object` | 100 | negative |
| `dog` | 100 | negative |
| `drinking` | 100 | negative |
| `eating` | 100 | negative |
| `knife` | 50 | negative |
| `taking_pictures` | 100 | positive |
| `touching` | 100 | negative |
| `watching_calm` | 100 | positive |
| **Total** | **750** | **550 negative / 200 positive** |

The images were staged in one controlled setting with one participant. They should not be treated as representative of real museum visitors or as evidence of generalisable behaviour-recognition performance.

## Repository layout

The intended layout is:

```text
data/
  behaviour_images/
    blunt_object/
    dog/
    drinking/
    eating/
    knife/
    taking_pictures/
    touching/
    watching_calm/
```

The repository-wide image ignore rules explicitly allow images only inside `data/behaviour_images/`, so runtime camera captures remain excluded from version control.

## Rights and licensing

The author owns the behavioural images. A specific reuse licence for the dataset should be stated before the final public release and Zenodo archive. The software licence in the repository does not automatically apply to the image dataset.

## Reproducibility notes

The historical experiments did not preserve a deterministic train/evaluation split seed. Different model pipelines also used different balancing procedures. The complete dataset therefore supports inspection and future re-analysis, but does not by itself guarantee recreation of the exact historical split.

The final tagged GitHub release will be archived on Zenodo together with the rest of the research companion.
