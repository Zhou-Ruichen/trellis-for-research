# Evaluation Guidelines

Use these rules for validation, test evaluation, prediction export, diagnostics,
figures, and report artifacts.

This file governs the evidence (what to write and where). The prose around that
evidence -- captions, report text, result discussions -- is governed by
[../shared/scientific-writing.md](../shared/scientific-writing.md).

## Evaluation Layout

```text
src/<pkg>/eval/
  metrics.py
  predict.py
  plots.py
  diagnostics.py
scripts/
  evaluate.py
  predict.py
```

This layout is for maintained evaluation code. Exploratory metrics, diagnostics,
and plots may stay in a script or notebook; reuse existing functions where useful.

## Verification Boundaries

Research code is exploratory: the result is discovered, not specified. Do not
add TDD, coverage targets, or metric pass/fail thresholds to an experiment.

Check execution and input assumptions:

- the pipeline runs and shapes, dtypes, and units are consistent;
- errors fail loudly at boundaries instead of producing fake success;
- check data isolation and relevant numerical or coordinate conventions using
  the requested run's inputs and outputs.

Additional checks follow [research-minimal.md](../shared/research-minimal.md).
Random-input baselines are included only when the scientific design calls for them.

Report scientific outcomes:

- Do not assert metric values anywhere. "RMSE must be below X" encodes the
  answer the experiment is meant to discover.
- A missed target is a finding to report (value, condition, gap to the
  baseline or expectation, plausible explanation), not a task failure. A
  task is complete when its evidence is traceable, not when a target is met.
- Validation commands attached to a task check executability and sanity
  only; they never assert metric values.

## Metrics

Retained evaluation runs write:

```text
outputs/<run_id>/metrics.json
```

Recommended schema:

```json
{
  "run_id": "20260610-142233-baseline",
  "split": "test",
  "metrics": {
    "rmse": 123.456,
    "mae": 98.765
  },
  "n_samples": 100,
  "data_manifest": "data/manifests/test_v1.json",
  "checkpoint": "outputs/20260610-142233-baseline/checkpoints/epoch=012.ckpt",
  "notes": []
}
```

Scratch and smoke evaluation runs may write lighter logs or metrics while
debugging. Promote the run and write the retained metrics file before citing it
in a comparison, report, or result claim.

Do not report retained metrics only in stdout, screenshots, notebooks, or
remote logging dashboards.

## Figures

For retained generated figures tied to a run, use:

```text
outputs/<run_id>/figures/
```

Scratch figures may live under `outputs/scratch/<run_id>/figures/` and may be
deleted unless promoted.

Use:

```text
reports/
```

only for curated figures and tables intended for papers, presentations, or
human-facing reports.

## Prediction Products

For retained runs, write model predictions under:

```text
outputs/<run_id>/predictions/
```

Retained prediction products must record:

- checkpoint path;
- input data manifest;
- prediction format;
- coordinate convention and grid definition when geospatial;
- postprocessing steps.

## Diagnostic Code

One parameterized diagnostic entrypoint is better than many copied scripts.

Good:

```text
scripts/diagnose_run.py
src/<pkg>/eval/diagnostics.py
```

Bad:

```text
scripts/diagnose_run_v2.py
scripts/diagnose_failed_sample_final.py
scripts/evaluate_old_checkpoint.py
```

## Quality Check

- [ ] Retained metrics are written to JSON with split and sample count.
- [ ] Retained figures and predictions are tied to a run ID.
- [ ] Predictions record the input data version, output format, and postprocessing.
- [ ] Geospatial outputs record coordinate convention and grid definition when applicable.
- [ ] Reports contain curated artifacts, not raw output dumps.
- [ ] Report prose and captions follow scientific-writing.md: science-first, no
      engineering terms, no over-ornamentation or empty adjectives, and units on quantitative figures.
- [ ] New evaluation behavior did not create copied script variants.
