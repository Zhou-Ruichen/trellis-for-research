# Guide: Add An Experiment

Use for a new model, data setting, ablation, or training run.

1. State the scientific question and the minimal comparison that answers it.
2. Find the existing training entrypoint, configs, data, checkpoints, and
   result records; express the difference with parameters or config values.
3. Run the training cases, seeds, or folds the question requires, keeping
   data isolation, split, units, and other matched conditions explicit.
4. Record the actual settings and command, observed results, negative
   findings, limitations, and useful output paths in the project's existing
   record.

Repeated seeds or configs are runs within one comparison, not separate
Trellis tasks. Execution and checking rules are in
[research-minimal.md](../shared/research-minimal.md).
