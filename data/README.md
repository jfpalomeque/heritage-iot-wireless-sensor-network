# Dataset release

The original archive contains behavioural image collections used for binary and multiclass experiments. Because these files may depict identifiable people and sensitive behaviours, they are not included in Git.

The agreed release policy is to publish the full dataset externally. Before publication, create a versioned Zenodo/Hugging Face dataset release containing:

1. a dataset card describing provenance, consent/legal basis, locations, intended use, risks, and licence;
2. a `SHA256SUMS` manifest and exact directory layout;
3. class definitions matching `configs/image_labels.json`;
4. duplicate detection and split protocol documentation;
5. an access/removal contact and any necessary restrictions.

Do not publish images until the right to distribute every image has been confirmed. Add the release DOI/URL and version here once published.
