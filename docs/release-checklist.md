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

## Pending before final tag

- [ ] Choose and state the behavioural dataset reuse licence in the public/Zenodo metadata.
- [ ] Decide whether model weights will be released and under what licence.
- [ ] Add the final CAA2026 manuscript/preprint DOI when minted.
- [ ] Run a final repository secret/private-address scan.
- [ ] Confirm README and CITATION.cff point to the intended final manuscript citation.
- [ ] Make the repository public.
- [ ] Create the final tag, proposed `v1.0.0-caa2026`.
- [ ] Archive that exact tag on Zenodo and add the software DOI back to README/CITATION.cff.
