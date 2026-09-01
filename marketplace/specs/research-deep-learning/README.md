# Deep Learning Research Spec

This spec is for research repositories that train and evaluate deep-learning
models for prediction, classification, generation, reconstruction, or analysis.
Use it when model training or evaluation is a primary workflow, regardless of
the research domain or data modality.

Existing repositories keep their documented layout and entrypoints. The shape
below is a starting point for new projects, not a migration requirement.

The template is Python-first, not Python-only. Python/PyTorch conventions are
included because they are the expected main stack, while the reproducibility,
anti-bloat, data, and run-manifest rules apply to mixed-language project
code as well. Add project-local language rules for durable CUDA/C++, Fortran,
Julia, Rust, or shell code when needed.

## Template Fit

Use `research-deep-learning` for:

- repositories with deep-learning model training, checkpoints, or comparisons;
- projects that need PyTorch-oriented training and evaluation conventions;
- workflows where data versions, model configurations, and retained run
  artifacts must remain traceable.

Use `research-computational` (General Computational Research) instead when the project
is non-DL research, statistical analysis, simulation, traditional ML, or a
data-processing pipeline without deep-learning training as the main workflow.

## Documentation Files

| File | Read when |
| --- | --- |
| [shared/index.md](./shared/index.md) | Before any implementation task |
| [shared/research-minimal.md](./shared/research-minimal.md) | Before exploratory implementation; overrides heavier guidance |
| [shared/project-layout.md](./shared/project-layout.md) | Creating files or directories |
| [shared/anti-bloat.md](./shared/anti-bloat.md) | Adding files, variants, scripts, or abstractions |
| [shared/reproducibility.md](./shared/reproducibility.md) | Running experiments or reporting results |
| [shared/scientific-writing.md](./shared/scientific-writing.md) | Writing reports, discussions, methods, or paper drafts |
| [shared/python-style.md](./shared/python-style.md) | Writing Python modules |
| [data/index.md](./data/index.md) | Reading, writing, processing, or validating data |
| [training/index.md](./training/index.md) | Training, checkpoints, configs, or model code |
| [evaluation/index.md](./evaluation/index.md) | Metrics, figures, predictions, or reports |
| [guides/index.md](./guides/index.md) | Choosing a task guide |
| [guides/add-experiment.md](./guides/add-experiment.md) | Adding a new experiment |
| [guides/write-results.md](./guides/write-results.md) | Drafting a results discussion, report, or paper section |
| [guides/debug-nan-oom.md](./guides/debug-nan-oom.md) | Debugging NaN, inf, divergence, or OOM |
| [guides/code-review.md](./guides/code-review.md) | Reviewing research-code changes |

## Project Goal

Make new research code easy to run, inspect, compare, and reproduce without
turning exploratory work into over-engineered product code.

## Recommended Shape For New Research Projects

```text
project/
  pyproject.toml
  README.md
  configs/
  data/
  src/<pkg>/
  scripts/
  notebooks/
  tests/
  outputs/
  reports/
```

Use this shape only when the project has no established layout. Omit directories
that the research does not use.

## Version Notes

Install from a release tag when the exact template matters. The source
repository's root CHANGELOG.md records template-id and rule changes.
