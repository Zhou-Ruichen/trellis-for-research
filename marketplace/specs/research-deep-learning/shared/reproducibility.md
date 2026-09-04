# Reproducibility

A result should be traceable to the inputs, code, configuration, environment,
assumptions, and outputs that produced it. Use the record that fits the work:
an existing training log, configuration, notebook, `result.md`, an immutable
source reference, or a short note is enough when it preserves the relevant
facts.

## Temporary and retained work

Temporary outputs include debugging attempts, failed training runs, quick
probes, and intermediate checkpoints that do not support a conclusion. Keep
them in a clearly temporary location and remove them when they stop being
useful.

Retain outputs used in a comparison, report, paper, model handoff, baseline,
or result claim. Retain enough evidence to identify:

- the exact dataset version, variables, split, and sampling or filtering rules;
- the command or notebook, model and training parameters, and seed or seed schedule;
- the code state, including relevant uncommitted changes;
- the Python, framework, accelerator, and dependency records when they affect results;
- metrics, checkpoints or predictions, logs, negative or null observations,
  assumptions, and known limitations.

Evidence may be distributed across existing project files. Do not require a
per-run manifest, config snapshot, fixed JSON fields, or empty fields. If a
config or script may change later, preserve the values and code changes used by the run, or
record a revision that identifies them; a pointer to a mutable file alone is
insufficient.

## Environment and randomness

Use the project's existing environment record, such as `uv.lock`, a conda or
venv record, a container digest, or a dependency export. Record per-run
versions only when no stable record exists or the environment can drift. Do not
install unrecorded dependencies into `base` or another project's environment.

Record the seed or seed schedule for Python, NumPy, PyTorch, data-loader
workers, and other RNGs that matter to the run. Note deterministic algorithm
settings and known nondeterminism from hardware, kernels, or parallelism when
they affect interpretation. Do not impose a project-wide determinism setting
when the experiment does not need it.

## Protocol changes and claims

For a retained comparison, keep the question, model and method, dataset
version, split, preprocessing, metric definition, baseline, and claim scope
identifiable. If one changes, retain the earlier evidence and state what
changed in the new record.

Describe the evaluated split and outputs before claiming that a model
improved, converged, or reproduced a number. Include parameters, randomness,
data version, code state, environment details that matter, and limitations. A
completed training command alone does not support a scientific claim.

Weights & Biases, SwanLab, TensorBoard, CSV logs, and console output may mirror
the record. Keep enough project-local evidence to recover the inputs and
decisions if an external service changes or disappears.
