# Evaluation Guidelines

Use these rules for validation, metrics, comparisons, figures, tables,
diagnostics, and report artifacts.

This file governs the evidence (what to write and where). The prose around that
evidence -- captions, report text, result discussions -- is governed by
[../shared/scientific-writing.md](../shared/scientific-writing.md).

## Evaluation Layout

Exploratory evaluation may stay in a script or notebook. Use the project's
source area for components explicitly maintained across tasks.

Typical structure:

```text
src/ or lib/
  metrics.*
  evaluation.*
  plots.*
scripts/
  evaluate.*
  make_figures.*
```

Existing projects may use different names. Follow their documented ownership
boundaries.

## Verification Boundaries

Research code is exploratory: the result is discovered, not specified. Do not
add TDD, coverage targets, or metric pass/fail thresholds to an experiment.

Check execution and input assumptions:

- the pipeline runs and shapes, schemas, and units are consistent;
- errors fail loudly at boundaries instead of producing fake success;
- check data isolation and relevant numerical or coordinate conventions using
  the requested run's inputs and outputs.

Additional checks follow [research-minimal.md](../shared/research-minimal.md).
Random-input baselines are included only when the scientific design calls for them.

Report scientific outcomes:

- Do not assert metric values anywhere. "Error must be below X" encodes the
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
  "run_id": "20260610-142233-sensitivity",
  "split": "test",
  "metrics": {
    "rmse": 123.456,
    "mae": 98.765
  },
  "n_samples": 100,
  "data_manifest": "data/manifests/test_v1.json",
  "parameters": "outputs/20260610-142233-sensitivity/config.yaml",
  "notes": []
}
```

Scratch and smoke evaluation runs may write lighter logs or metrics while
debugging. Promote the run and write retained metrics before citing it in a
comparison, report, or result claim.

Do not report retained metrics only in stdout, screenshots, notebooks, or
remote logging dashboards.

## Figures And Tables

For retained generated figures and tables tied to a run, use:

```text
outputs/<run_id>/figures/
outputs/<run_id>/tables/
```

Use:

```text
reports/
```

only for curated figures, tables, and summaries intended for papers,
presentations, or human-facing review.

Reports must point back to the retained run, manifest, or data product that
created each result.

## Comparisons

Comparison tables must record:

- compared run IDs or data manifests;
- metric definitions;
- sample set, split, condition, or grouping;
- parameter differences that matter;
- assumptions and exclusions.

Do not compare numbers copied from dashboards, notebooks, or screenshots unless
the underlying retained artifacts are available.

## Diagnostic Code

One parameterized diagnostic entrypoint is better than many copied scripts.

Good:

```text
scripts/diagnose_run.py
src/project/diagnostics.py
```

Bad:

```text
scripts/diagnose_run_v2.py
scripts/evaluate_bad_case_final.py
scripts/check_new_results.py
```

## Quality Check

- [ ] Retained metrics are written to JSON with sample set or split.
- [ ] Retained figures and tables are tied to a run ID or data manifest.
- [ ] Comparison tables record what was compared and how.
- [ ] Reports contain curated artifacts, not raw output dumps.
- [ ] Report prose and captions follow scientific-writing.md: science-first, no
      engineering terms, no over-ornamentation or empty adjectives.
- [ ] New evaluation behavior did not create copied script variants.
