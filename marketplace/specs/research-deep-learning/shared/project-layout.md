# Project Layout

Follow the project's documented layout. The repository's existing structure
also decides where new training, data, evaluation, notebook, output, and report
files belong. For a new project, create only what the current work uses.

An exploratory run can be a direct script or notebook. It does not require a
package, configuration hierarchy, test directory, or command-line machinery.
Use the source area for code maintained across tasks, and use existing configs
when the project has them. Keep variants as explicit parameters or config
overrides rather than copied training or evaluation scripts.

Record retained evidence in the form the project already uses. Include the
actual command or settings, seed when relevant, data and split, model and
training conditions, observed results with units, and paths to checkpoints,
logs, or products as needed. A config, log, notebook, or `result.md` can be the
record. Keep temporary outputs separate from evidence used for a result, using
existing project conventions; do not require moving outputs into a prescribed
tree.

Keep filenames readable and avoid `v2`, `final`, or backup copies for current
source. Follow the repository's existing Git rules for large generated files.
