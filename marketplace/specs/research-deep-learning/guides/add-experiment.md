# Guide: Add An Experiment

Follow this when adding a new model, data setting, ablation, or training run.

## Steps

1. Search existing configs, scripts, and run records.
2. Edit existing experiment parameters or configs; do not add a config system
   for a one-off run.
3. Reuse the existing training entrypoint.
4. Run the training, comparisons, seeds, or folds required by the scientific
   question. Diagnose actual failures as needed; follow
   [research-minimal.md](../shared/research-minimal.md) for additional checks.
5. Record the command in the task response or project notes when it must survive
   the session.

## Do

```text
configs/exp/without_auxiliary_input.yaml
scripts/train.py --config configs/exp/without_auxiliary_input.yaml
```

## Do Not

```text
scripts/train_without_auxiliary_input.py
scripts/train_without_auxiliary_input_final.py
src/<pkg>/training/trainer_v2.py
```

## Experiment Settings

Make these values explicit in the existing config or script, and record them
when retaining the result:

- seed;
- data manifest path;
- model name and parameters;
- optimizer and scheduler;
- training duration;
- output root or run name;
- logging backend if used.

## Completion Checklist

- [ ] Experiment differences are explicit parameters or configs.
- [ ] New code was added only when existing code could not express the change.
- [ ] The run command is clear.
- [ ] The runs required by the scientific question are represented.
- [ ] Metric targets are reported as observations, not task pass/fail criteria.
