# CAA2026 companion release checklist

The repository is prepared as a research companion. The final archival tag should be created after the remaining publication metadata decisions are resolved.

## Completed

- [x] Remove private network addresses and credentials from tracked configuration.
- [x] Preserve a sanitized historical deployment configuration.
- [x] Fix the dashboard configuration-save path.
- [x] Fix the Azure uploader undefined-variable error.
- [x] Remove dashboard dependence on historical sensor identifiers.
- [x] Add machine-readable historical deployment, WSN, model, and CLIP summaries.
- [x] Document the ViT three-epoch result versus five-epoch script discrepancy.
- [x] Add a reconstructed hardware inventory without invented prices.
- [x] Document missing Azure Data Factory infrastructure and provide only a compatible reference SQL schema.
- [x] Preserve the exact historical CLIP label list separately from the cleaned future-run configuration.
- [x] Update citation metadata with the author's full given name.
- [x] Confirm that the author is the sole photographed participant and holds the rights to the behavioural images.
- [x] Include the complete 750-image behavioural dataset in both historical experimental layouts.
- [x] Remove the larger working/source image directory from the publication repository.
- [x] Confirm that the behavioural dataset will be archived with the tagged repository release on Zenodo.
- [x] Release the behavioural dataset under CC BY 4.0.
- [x] Decide not to distribute trained model weights; provide the complete dataset and training scripts for retraining instead.
- [x] Document that the historical train/evaluation split seed was not preserved and that exact historical weights or metrics cannot be guaranteed.
- [x] Remove the obsolete placeholder for a separate behavioural-image directory.
- [x] Remove the older arXiv version as the repository's preferred citation and point README/CITATION.cff to the CAA2026 manuscript.
- [x] Run a repository secret/private-address scan; no tracked credentials or private IP addresses were identified.

## Pending before final tag

- [ ] Add the final CAA2026 manuscript DOI when minted.
- [ ] Make the repository public.
- [ ] Create the final tag, proposed `v1.0.0-caa2026`.
- [ ] Archive that exact tag on Zenodo and add the software DOI back to README/CITATION.cff.
