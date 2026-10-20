# Configuration files

Two WSN configuration examples are provided.

- `wsn_config.example.json` is a minimal, deliberately inert scaffold for a new deployment.
- `wsn_config.historical.example.json` is a sanitized transcription of the configuration documented for the original experiment. Private network addresses are replaced by placeholders, while historical node names, schedules, trigger relationships, and script calls are retained.

The historical code uses the key `distance_senors`. The misspelling is preserved because the recovered runner, trigger, and action code expect that key.

`image_labels.historical.json` preserves the label list used by the archived zero-shot CLIP workflow, including duplicated `eating` and `drinking` negative prompts. `image_labels.json` removes those accidental duplicates for future runs. Historical reported CLIP metrics were not recomputed after this cleanup.
