# Guide: Add An Experiment

Follow this when adding a new model, data setting, ablation, or training run.

## Steps

1. Search existing configs under `configs/`.
2. Create or edit a config override under `configs/exp/`.
3. Reuse the existing training entrypoint.
4. Add or update small tests only if the experiment requires new reusable code.
5. Run the training, comparisons, seeds, or folds required by the scientific
   question. Use a smaller execution check only when it helps diagnose the path.
6. Record the command in the task response or project notes when it must survive
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

## Required Config Fields

At minimum, an experiment config should resolve:

- seed;
- data manifest path;
- model name and parameters;
- optimizer and scheduler;
- training duration;
- output root or run name;
- logging backend if used.

## Completion Checklist

- [ ] The experiment is represented as config.
- [ ] New code was added only when config could not express the change.
- [ ] The run command is clear.
- [ ] The runs required by the scientific question are represented.
- [ ] Metric targets are reported as observations, not task pass/fail criteria.
