# Keep Research Code Small

Reuse the project's existing functions, entrypoints, and dependencies before
adding code; the standard library and an already-installed package come next.
Keep experiment differences in parameters or existing configs, not in copies
named `train_v2.py` or `analysis_final.py`.

Extract a function or module only when it removes real duplication or
clarifies the current calculation; no factories, registries, base classes,
plugin systems, or CLI layers for possible future work. When a task replaces
tracked code, remove the superseded implementation and its unused wrappers
once the replacement works.

This does not authorize unrelated cleanup: preserve original data, retained
results, settings referenced by results, untracked files, and unrelated work,
and report suspected dead code outside the task instead of deleting it.
