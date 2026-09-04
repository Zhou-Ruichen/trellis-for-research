# Training Guidelines

Use these rules for model definitions, training loops, config files,
checkpoints, and experiment variants.

## Preferred Stack

- Existing project layout; a direct script is enough for an exploratory run.
- PyTorch for model code.
- Lightning is acceptable when it is already the project choice.
- Existing experiment configs when available.
- Optional Hydra/OmegaConf is acceptable, but do not add it to small scripts only
  to look structured.

## Recommended Training Layout

```text
configs/
  base.yaml
  exp/
src/<pkg>/
  data/
  models/
  training/
scripts/
  train.py
```

Split out `configs/data/` and `configs/model/` groups when the config tree
grows; `configs/exp/` stays the home of experiment overrides either way.

For a new project, `scripts/train.py` can be a thin entrypoint:

1. load config;
2. resolve paths;
3. set seed;
4. create datamodule/dataloaders;
5. create model/trainer;
6. write retained-run manifest when the run is kept as evidence;
7. train.

This layout is for maintained training code. An exploratory script may load
data, construct the model, train, and save results directly.

## Config Rule

Reuse existing configs. Without a config system, a one-off script may declare
parameters and construct the model directly. Retained results still record the
values used, per [reproducibility.md](../shared/reproducibility.md).

## Experiment Variants

When the project uses experiment configs, a variant is a config override:

```text
configs/exp/baseline.yaml
configs/exp/transformer.yaml
configs/exp/without_auxiliary_input.yaml
```

Never add:

```text
scripts/train_v2.py
scripts/train_transformer_final.py
src/<pkg>/training/train_old.py
```

## Checkpoints

For retained runs, write checkpoints under:

```text
outputs/<run_id>/checkpoints/
```

Checkpoint filenames should include epoch and a primary validation metric when
available:

```text
epoch=012-val_rmse=123.456.ckpt
```

Do not store checkpoints in source directories.
Scratch and smoke checkpoints may live under `outputs/scratch/<run_id>/` and
may be deleted when they are no longer useful.

## Quality Check

- [ ] Experiment differences are explicit parameters or configs, not copied scripts.
- [ ] Training outputs land under `outputs/`; retained run outputs land under
      `outputs/<run_id>/`.
- [ ] Retained run manifest records config, seed, code state, environment, and
      data manifest.
- [ ] Execution follows [research-minimal.md](../shared/research-minimal.md),
      using the requested result-producing runs.
