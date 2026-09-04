# Evaluation Guidelines

Use the project's existing evaluation layout. Exploratory metrics, diagnostics,
plots, and prediction code may stay in the script or notebook where they are
needed. Extract code only to simplify the current calculation or meet an explicit
maintenance need.

Start from the scientific question and define the minimal comparison that can
answer it. Keep data isolation and matched conditions explicit. State the split
or sample set, relevant parameter differences, units, coordinate conventions,
and exclusions. Check only input assumptions that affect the calculation. Do
not add a generic validator, preflight framework, or metric target. Software tests
require an explicit task or user request; actual failures can be diagnosed
without creating a test suite. See [minimal rules](../shared/research-minimal.md).

## Metrics And Results

Use the metrics and prediction format required by the question and existing
project conventions. No fixed `metrics.json` or prediction schema is required.
Record actual values, definitions, conditions, checkpoints or input data, and
output paths in the project's existing log, config, notebook, result record, or
report.

A metric below an expectation is an observation to explain, not a failed software
task. Report negative findings and their limitations with the same evidence as
positive findings.

## Figures And Predictions

Keep figures and prediction products with the analysis that produced them,
following existing project paths. For a retained result, record enough context
to identify the checkpoint, input data, output format, postprocessing, and
geospatial conventions when those details affect interpretation. Curate paper
or review material in the project's report area when one exists.

## Diagnostic Code

Reuse a parameterized diagnostic when it already exists or will be reused. A
one-off diagnostic can remain local to the analysis. Represent variants with
explicit parameters or configs instead of copied scripts named `v2` or `final`.
