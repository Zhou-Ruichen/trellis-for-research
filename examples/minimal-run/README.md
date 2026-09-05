# Minimal Runnable Example

Can a line fitted to 200 noisy synthetic observations recover the generating
relation `y = 2x + 1`? [analysis.py](analysis.py) generates the observations with
seed 42, fits ordinary least squares with Python's standard library, and prints
the parameters and in-sample metrics. It needs Python 3.10 or newer, with no
package installation.

```sh
python3 analysis.py
```

[result.json](result.json) contains an actual execution, including its Python
version and data settings. To replace that record after an intentional change:

```sh
python3 analysis.py > result.json
```

The [short report](reports/linear_regression_discussion.md) interprets the result.
The observations used for fitting are also used for evaluation; these numbers
describe this synthetic sample, not generalization to unseen or real data.

This example keeps parameters in the script and one result beside it. Edit the
existing script for a new comparison; preserve the code and results supporting
any finding you keep. Use another structure when a project actually needs it.
