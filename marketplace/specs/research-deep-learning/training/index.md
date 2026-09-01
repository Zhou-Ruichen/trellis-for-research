# Training Guidelines

Use these rules for model definitions, training loops, config files,
checkpoints, and experiment variants.

## Preferred Stack

- Python package layout under `src/<pkg>/`.
- PyTorch for model code.
- Lightning is acceptable when it is already the project choice.
- YAML config files in `configs/`.
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

Reusable logic belongs in the project's established package location, or under
`src/<pkg>/` in a new project.

## Config Rule

Configs are the single source of truth for:

- data paths and manifest paths;
- model architecture;
- loss and metrics;
- optimizer and scheduler;
- batch size, epochs, precision, devices, gradient accumulation;
- seed and determinism settings;
- output root and run naming.

Bad:

```python
lr = 3e-4
batch_size = 8
model = UNet(channels=64)
```

Good:

```python
lr = cfg.optimizer.lr
batch_size = cfg.training.batch_size
model = build_model(cfg.model)
```

## Experiment Variants

A new experiment is a config override:

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

## Minimal Execution Check

For a maintained training pipeline, keep a tiny configuration that exercises one
step on the cheapest device that supports the model:

```text
configs/exp/smoke.yaml
```

The configuration should:

- use a tiny fixture or tiny subset;
- run one epoch or one training step;
- use CPU when the model supports it; otherwise use the smallest supported GPU
  path without adding a separate CPU implementation;
- verify loss is finite;
- write enough log or metrics evidence to debug failures.

A smoke run only needs the full manifest and environment freeze if it is
promoted to a retained run.

## Quality Check

- [ ] New experiment added a config, not a copied training script.
- [ ] Training outputs land under `outputs/`; retained run outputs land under
      `outputs/<run_id>/`.
- [ ] Retained run manifest records config, seed, code state, environment, and
      data manifest.
- [ ] Maintained training behavior has one small execution path on a supported
      device; exploratory work uses the requested result-producing invocation.
- [ ] Model code remains reusable and testable under `src/<pkg>/`.
