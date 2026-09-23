# Keep Research Code Small

Reuse the project's functions, entrypoints, and installed dependencies. Keep
experiment differences in parameters or an existing config instead of making
copies such as `train_v2.py` or `analysis_final.py`.

Add a function or module when it removes real duplication or makes the current
calculation easier to rerun. Add a framework, registry, plugin system, CLI
layer, test suite, or compatibility layer only for a concrete need. A one-off
check can stay in the script or notebook where it was useful.

Remove a superseded implementation after the replacement works. Keep data
references, reported numbers, settings needed to interpret them, and
unrelated changes. Review the calculation itself when a test suite is absent.
