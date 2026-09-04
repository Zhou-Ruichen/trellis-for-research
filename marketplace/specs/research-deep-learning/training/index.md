# Training Guidelines

Use the project's existing layout and stack. PyTorch fits model code; use
Lightning, Hydra, OmegaConf, or another tool when it is already the project
choice. A direct script is enough for an exploratory run.

Begin with the question and the minimal comparison needed to answer it. Reuse
the existing training entrypoint and configs when possible. A one-off script may
load data, construct the model, train, and save results directly. Do not add a
package, configuration system, or CLI layer just to give a small exploration a
formal shape.

Make differences between variants explicit in parameters or config values. Keep
data, split, seed, training duration, and other comparison conditions matched
when the scientific design requires it. Repeated seeds or configs are part of
the planned comparison, not separate Trellis tasks.

Record the actual settings and observations needed to interpret the result:
model and optimizer choices, data and split, seed when relevant, training
duration, checkpoint or output path, metrics with units, and negative findings.
Use the project's existing logs, configs, notebooks, or result records; no fixed
manifest or output schema is required.

Store checkpoints according to existing project conventions. Do not put them in
source directories unless that is already the repository's convention. Diagnose
actual failures at the point they occur; do not add generic preflight checks,
metric targets, or a test suite without an explicit request.
