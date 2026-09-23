# Training Guidelines

Use the project's existing layout and stack; PyTorch fits model code, and
Lightning, Hydra, OmegaConf, or similar tools stay when already the project
choice. A direct script is enough for an exploratory run: load data,
construct the model, train, and save results.

If early stopping or checkpoint choice affects the result, say which data and
rule made the choice. For a result someone should rerun, record the model and
optimizer settings, data or split, relevant seed, command, and result path.
Keep a checkpoint only when it is needed to rerun or interpret that result.
Diagnose actual failures where they occur; see [debug guidance](../guides/debug-nan-oom.md)
for NaN, Inf, divergence, or OOM.
