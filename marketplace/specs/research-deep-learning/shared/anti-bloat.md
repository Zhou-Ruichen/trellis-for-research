# Keep The Repository Maintainable

Deep-learning repositories become difficult to maintain when each experiment
copies a training script, adds a wrapper, or leaves the replaced implementation
beside the new one. Prevent that accumulation while leaving exploration free to
change.

## Reuse Before Adding

Before adding durable code:

1. Search for an existing loader, transform, model block, metric, plot, or helper
   that already owns the behavior.
2. Prefer a parameter or experiment config over a copied script.
3. Reuse an existing dependency or the standard library before adding a new
   dependency or local implementation.
4. Add only the smallest implementation the task still needs.

Extract shared code when repeated durable logic is already present. Do not add a
factory, registry, base class, plugin system, or config class for possible future
reuse.

## Keep Variants In Config

Use one training entrypoint with explicit experiment configs:

```text
scripts/train.py
configs/exp/baseline.yaml
configs/exp/transformer.yaml
configs/exp/without_auxiliary_input.yaml
```

Do not accumulate source variants:

```text
scripts/train_v2.py
scripts/train_transformer_final.py
src/<pkg>/training/trainer_old.py
```

Version labels are valid when the thing itself has a versioned identity and the
versions need to coexist: datasets, schemas, public interfaces, model releases,
or experiment protocols. `dataset_v1.json` and `dataset_v2.json` can therefore
be correct. A suffix is not a substitute for deciding which source file owns
the current implementation.

## Exploratory And Diagnostic Code

One-off notebook cells, scripts, and diagnostics may stay direct and local.
Delete temporary instrumentation after it answers the question. Move logic into
the maintained source area only when another task needs it or the repository
will keep using it.

## Replace Without Accumulating

When the current task replaces tracked code, remove the superseded implementation
after the replacement has been checked. Git history preserves it. Do not keep `_old`,
`_final`, backup directories, compatibility wrappers, duplicate tests, or source
versions without a current reason to coexist.

This rule does not authorize unrelated cleanup. Report suspected dead code that
the current task did not replace. Preserve retained outputs, data manifests,
configs referenced by results, and untracked files unless the user requests
their removal.

In the completion report, mention material files added or removed and the reason.
