# Deep Learning Research Guides

Use these guides for common research-code workflows.

## Documentation Files

| Guide | When to read |
| --- | --- |
| [add-experiment.md](./add-experiment.md) | Adding a model, data setting, ablation, or training run |
| [write-results.md](./write-results.md) | Drafting a results discussion, report, or paper section |
| [debug-nan-oom.md](./debug-nan-oom.md) | Debugging NaN, inf, divergence, or out-of-memory failures |
| [code-review.md](./code-review.md) | Reviewing research-code changes before completion |

## Quick Navigation By Task

| Task | Read |
| --- | --- |
| Add a new DL experiment | [add-experiment.md](./add-experiment.md) |
| Change model, optimizer, data, or training duration | [../training/index.md](../training/index.md) and [add-experiment.md](./add-experiment.md) |
| Evaluate, export predictions, or make figures | [../evaluation/index.md](../evaluation/index.md) |
| Write a results discussion or report | [write-results.md](./write-results.md) and [../shared/scientific-writing.md](../shared/scientific-writing.md) |
| Debug unstable training or OOM | [debug-nan-oom.md](./debug-nan-oom.md) |
| Review for reproducibility and bloat | [code-review.md](./code-review.md) |

## Rules Summary

| Rule | Reference |
| --- | --- |
| New experiments are config overrides, not copied scripts | [../training/index.md](../training/index.md) |
| Retained runs need manifest, metrics, data record, seed, and an environment record | [../shared/reproducibility.md](../shared/reproducibility.md) |
| Scratch and smoke runs stay lightweight unless promoted | [../shared/reproducibility.md](../shared/reproducibility.md) |
| Durable data products need manifests and checks for the fields the model uses | [../data/index.md](../data/index.md) |
| Report prose leads with the finding, not the run | [../shared/scientific-writing.md](../shared/scientific-writing.md) |
| Superseded code is deleted after verification; experiment records require care | [../shared/anti-bloat.md](../shared/anti-bloat.md) |
| Check execution and data assumptions; report scientific outcomes without pass/fail targets | [../evaluation/index.md](../evaluation/index.md) |
