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
- New code and dependencies follow [anti-bloat.md](./anti-bloat.md). Temporary
  diagnostics are removed after they answer their question.
- Result claims point to the config, seed, data, environment record, metrics,
  and outputs that support them. Metric values remain observations, not task
  pass/fail criteria.
