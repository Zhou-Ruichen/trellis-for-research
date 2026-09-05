# Training Guidelines

Use the project's existing layout and stack; PyTorch fits model code, and
Lightning, Hydra, OmegaConf, or similar tools stay when already the project
choice. A direct script is enough for an exploratory run: load data,
construct the model, train, and save results.

Make differences between variants explicit in parameters or config values.
Keep data, split, seed, training duration, and other comparison conditions
matched when the scientific design requires it.

Record the settings and observations needed to interpret the result: model
and optimizer choices, data and split, seed when relevant, training
duration, checkpoint or output path, metrics with units, and negative
findings. Store checkpoints per existing project conventions, not in source
directories unless that is the convention. Diagnose actual failures where
they occur; see [debug guidance](../guides/debug-nan-oom.md) for NaN, Inf,
divergence, or OOM.
