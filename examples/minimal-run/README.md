# Minimal Runnable Example

A tiny, self-contained project that demonstrates the
`research-core` contract end to end: a data manifest, a config, a training run,
a retained-run manifest with environment freeze, and a curated report written in
the scientific style the spec requires.

The task is one-feature linear regression on synthetic data. It uses only the
Python standard library plus `pyyaml` for config files, so it runs anywhere.

## Layout

```text
minimal-run/
  pyproject.toml
  configs/
    base.yaml
    exp/
      linear.yaml      # retained experiment (config override over base)
      smoke.yaml       # tiny smoke run (writes to the scratch tier)
  data/
    processed/
      synthetic_v1.json        # committed small fixture (200 points)
    manifests/
      synthetic_v1.json        # data manifest with sha256 checksum
  src/research_demo/
    data.py        model.py        training.py
    evaluation.py  manifest.py     checksum.py
  scripts/
    build_dataset.py  train.py  evaluate.py
  tests/
    test_smoke.py
  outputs/
    20260725-100000-linear/     # committed retained-run snapshot
      manifest.json  config.yaml  metrics.json
      checkpoint.json  environment.freeze.txt
  reports/
    linear_regression_discussion.md   # bilingual EN/CN result discussion
```

## Run It

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -e . pytest

# Regenerate the synthetic dataset and refresh its manifest.
python scripts/build_dataset.py

# Train and write a retained run under outputs/<run_id>/.
python scripts/train.py --config configs/exp/linear.yaml

# Re-evaluate a saved checkpoint from a run.
python scripts/evaluate.py --run-id <run_id>

# Run the smoke path (scratch tier, no environment freeze).
python scripts/train.py --config configs/exp/smoke.yaml

# Tests.
pytest -q
```

## What To Look At

- `data/manifests/synthetic_v1.json` records source, version, schema, and a
  sha256 checksum for the processed product.
- `outputs/20260725-100000-linear/manifest.json` is a complete retained-run
  manifest: command, config snapshot, seed and randomness scope, environment
  freeze, data reference, metrics, and assumptions.
- `outputs/20260725-100000-linear/environment.freeze.txt` is the environment
  snapshot captured next to the run.
- `reports/linear_regression_discussion.md` shows the scientific-writing rules
  in practice, with an English version, a Chinese version, and a contrast
  example of the engineering tone to avoid.

## Notes

- The data are synthetic. Metrics in the committed snapshot are real outputs of
  `scripts/train.py`, not invented values.
- The committed `outputs/20260725-100000-linear/` is a documentation snapshot;
  its `git` field is a labeled placeholder. Run `scripts/train.py --run-id
  20260725-100000-linear` to regenerate it with a live commit hash.
- The smoke config writes to `outputs/scratch/`, which is gitignored and
  disposable. Promote a smoke run to retained before citing it.
