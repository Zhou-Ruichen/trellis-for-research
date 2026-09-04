# Guide: Add An Experiment

Use this for a new model, data setting, ablation, or training run.

1. State the scientific question and the minimal comparison that can answer it.
2. Find the existing training entrypoint, configs, data, checkpoints, and result
   records.
3. Express the difference with explicit parameters or config values. Add code
   only when the existing implementation cannot express it.
4. Run the training cases, seeds, or folds required by the question. Keep data
   isolation, split, units, and other matched conditions explicit. Diagnose
   failures when they occur; do not add generic validators or preflight layers.
5. Record the actual settings and command, observed results, negative findings,
   limitations, and paths to useful outputs in the project's existing notes,
   logs, config, notebook, or result record.

Repeated seeds or configs are part of one scientific comparison. They do not
require separate Trellis tasks. Do not turn metric expectations into task
pass/fail criteria, and do not create copied scripts named `v2` or `final`.
