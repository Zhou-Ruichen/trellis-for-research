# Training Guidelines

Use the project's existing layout and stack; PyTorch fits model code, and
Lightning, Hydra, OmegaConf, or similar tools stay when already the project
choice. A direct script is enough for an exploratory run: load data,
construct the model, train, and save results.

Early stopping and checkpoint selection count as selection under the
[evaluation guidelines](../evaluation/index.md).

Record with a retained run the model and optimizer choices, data and split,
the seed schedule for the Python, NumPy, framework, and data-loader RNGs
that matter, training duration, augmentation and label conventions, and
the checkpoint or output path. A checkpoint alone is not a result; report
the evaluation run on it. Diagnose actual failures where they occur; see
[debug guidance](../guides/debug-nan-oom.md) for NaN, Inf, divergence, or
OOM.
