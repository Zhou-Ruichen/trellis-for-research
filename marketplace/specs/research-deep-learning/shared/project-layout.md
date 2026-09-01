# Project Layout

Use the project's documented layout when one exists. The shape below is a
starting point for a new Python project, not a reason to reorganize an existing
repository.

## Recommended Layout For New Projects

```text
project/
  pyproject.toml
  README.md
  configs/
    base.yaml
    exp/
  data/
    raw/
    interim/
    processed/
    external/
    manifests/
  src/<pkg>/
    data/
    models/
    training/
    eval/
    utils/
  scripts/
  notebooks/
  tests/
  outputs/
  reports/
```

Add `configs/data/` and `configs/model/` only when the config tree grows beyond
`base.yaml` plus `configs/exp/` overrides.

## Directory Contracts

| Path | Contract |
| --- | --- |
| `configs/` | YAML configs. All hyperparameters, data paths, run settings, and feature switches live here. |
| `configs/exp/` | Experiment overrides. Add files here instead of copying train/eval scripts. |
| `data/raw/` | Immutable project-local raw data, symlinks, small samples, or pointers to external data. |
| `data/interim/` | Intermediate outputs from data processing. Rebuildable. |
| `data/processed/` | Model-ready data products. Rebuildable and manifest-backed. |
| `data/external/` | Read-only external datasets or symlinks when a project-local pointer is useful. |
| `data/manifests/` | JSON/YAML records for source, version, checksum, processing parameters, and split definitions. |
| `src/<pkg>/data/` | Dataset, datamodule, transforms, split logic, data validation in a new project. |
| `src/<pkg>/models/` | `torch.nn.Module` model definitions and model blocks. |
| `src/<pkg>/training/` | Training loop, LightningModule, optimizer/scheduler/loss builders, checkpoint logic. |
| `src/<pkg>/eval/` | Metrics, prediction writers, evaluation routines, plotting helpers. |
| `src/<pkg>/utils/` | Small shared utilities: seed, logging, config, paths, devices. |
| `scripts/` | Thin command entrypoints only. Business logic belongs in `src/<pkg>/`. |
| `notebooks/` | Exploration and inspection. Stable code must move to `src/<pkg>/`. |
| `tests/` | Durable checks when the project keeps them. |
| `outputs/<run_id>/` | Retained run artifacts: config snapshot, manifest, metrics, checkpoints, logs, predictions, figures. |
| `outputs/scratch/<run_id>/` | Optional disposable scratch or smoke outputs that are not used as result evidence. |
| `reports/` | Selected figures/tables for papers, presentations, and human review. |

## Naming Rules

- Use lower-case ASCII paths with underscores where needed.
- Prefer action-object names: `build_dataset.py`, `train.py`, `evaluate.py`.
- Use version labels for datasets, schemas, interfaces, releases, and protocols
  that intentionally coexist. Keep one maintained filename for the current
  source implementation instead of date, `v2`, `final`, or backup copies.
- Do not use non-ASCII filenames for code that agents must modify. Put Chinese notes in markdown if needed.

Bad:

```text
data_script_with_non_ascii_name.py
train_v2.py
train_final.py
output/
outputs/
model_experiment_backup_20251114/
```

Good:

```text
scripts/build_dataset.py
scripts/train.py
configs/exp/baseline.yaml
outputs/20260610-142233-baseline/
```

## Output Rule

Use `outputs/`, not `output/`. A project must not have both.

Retained `outputs/<run_id>/` directories should contain:

```text
config.yaml
manifest.json
metrics.json
environment.record.txt  # only when no stable project record exists
logs/
checkpoints/
predictions/
figures/
```

Scratch and smoke outputs may be lighter and may live under
`outputs/scratch/<run_id>/`. Promote them into a retained `outputs/<run_id>/`
directory before using them in a comparison, report, or result claim.

## Git Rule

Large or generated artifacts should normally be ignored:

```gitignore
data/raw/
data/interim/
data/processed/
data/external/
outputs/
*.ckpt
*.pt
*.pth
*.nc
*.npz
*.tif
*.tiff
```

Commit `data/manifests/`, small fixtures, code, configs, tests, and curated
`reports/` artifacts when they are intentionally part of the project record.
