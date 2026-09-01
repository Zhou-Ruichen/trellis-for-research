# Shared Deep Learning Research Guidelines

Use the sections relevant to the current task. Optimize for reproducibility,
iteration speed, and readable research code.

An existing repository's documented layout, commands, environment, and data
locations take precedence. Do not migrate them unless the task asks for it.

## Documentation Files

| File | Read when |
| --- | --- |
| [research-minimal.md](./research-minimal.md) | Before any exploratory implementation; overrides conflicting guidance |
| [project-layout.md](./project-layout.md) | Creating, moving, or naming files |
| [anti-bloat.md](./anti-bloat.md) | Adding files, variants, scripts, helpers, or abstractions |
| [reproducibility.md](./reproducibility.md) | Running or reporting experiments |
| [scientific-writing.md](./scientific-writing.md) | Writing reports, discussions, methods, or paper drafts |
| [python-style.md](./python-style.md) | Writing Python modules |
| [../data/index.md](../data/index.md) | Touching data |
| [../training/index.md](../training/index.md) | Touching training or model code |
| [../evaluation/index.md](../evaluation/index.md) | Touching metrics, predictions, figures, or reports |

## Pre-Development Checklist

- [ ] Can this be expressed as a config change instead of new code?
- [ ] Is there an existing loader, transform, model block, metric, or utility to reuse?
- [ ] Adding new code or a dependency? Climb the reuse ladder in
      [anti-bloat.md](./anti-bloat.md) first.
- [ ] Defining done for this task? Use the smallest relevant sanity check and
      traceable evidence; report metric targets as observations
      ([../evaluation/index.md](../evaluation/index.md)).
- [ ] Is this exploratory? Keep it in `notebooks/` or a thin `scripts/` entrypoint.
- [ ] Is this durable? Put reusable logic under `src/<pkg>/`.
- [ ] Touching data? Check split, leakage, dtype, shape, and the metadata the model uses.
- [ ] Touching results? Decide whether each run is scratch, smoke, or
      retained; confirm where retained metrics, figures, config snapshots, and
      run manifests are written.
- [ ] Writing prose (report, discussion, methods, paper draft)? Plan to lead
      with the scientific finding; see [scientific-writing.md](./scientific-writing.md).

## Rules

- In a new project, use `src/<pkg>/` for reusable code. In an existing project,
  put it in the established package location.
- Use `configs/` as the single source of truth for experiment knobs.
- A new experiment is a new config override under `configs/exp/`, not a copied training script.
- `data/` is allowed, but it must be structured by lifecycle and documented with manifests.
- `outputs/<run_id>/` is the canonical home for retained run artifacts.
- Scratch and smoke runs stay lightweight and disposable unless promoted.
- `reports/` is only for curated, lightweight figures and tables that are meant to be read.
- Delete code the current task superseded, once the replacement is verified;
  git history is the archive. Suspected-dead code, bulk cleanup, and
  experiment records (`outputs/` artifacts backing results, `data/manifests/`,
  configs still referenced, anything untracked) need asking first. List every
  deletion in the completion report.
- Do not productionize one-off exploration with factories, plugin systems, config classes, or extra CLI layers.
- New code and dependencies follow the reuse ladder in anti-bloat.md; one-off
  test code is deleted after it answers its question.

## Quality Check

Before claiming completion:

- [ ] The change follows [project-layout.md](./project-layout.md).
- [ ] No duplicate `*_v2.py`, `*_final.py`, copied experiment script, or backup directory was introduced.
- [ ] New reusable logic lives under `src/<pkg>/`, not in notebooks or ad hoc scripts.
- [ ] Any result claim is backed by a retained run artifact with config, seed,
      environment freeze, data manifest, and metrics.
- [ ] Human-facing prose follows
      [scientific-writing.md](./scientific-writing.md): supported claims, plain
      language, and exact Methods details without engineering state presented
      as a scientific result.
- [ ] Any data-writing task records what was written, where it came from, and how to rebuild it.
- [ ] Metric values are reported rather than used as task pass/fail criteria;
      one-off test and diagnostic code was deleted, not committed.
