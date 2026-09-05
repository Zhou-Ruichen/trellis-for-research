# Evaluation Guidelines

Evaluation starts from the scientific question and the minimal comparison
that answers it. Keep data isolation and matched conditions explicit: state
the split or sample set, relevant parameter differences, units, coordinate
conventions, and exclusions. Check only input assumptions that affect the
calculation, and let actual failures guide debugging.

## Metrics And Results

Use the metrics and prediction format the question and existing project
conventions require; no fixed `metrics.json` or prediction schema is
needed. Record actual values, definitions, conditions, checkpoints or input
data, and output paths in the project's existing log, config, notebook, or
result record.

A metric below an expectation is an observation to explain, not a failed
software task. Report negative findings and their limitations with the same
evidence as positive findings.

## Figures And Predictions

Keep figures and prediction products with the analysis that produced them,
following existing project paths. For a retained result, record enough
context to identify the checkpoint, input data, output format,
postprocessing, and geospatial conventions when those details affect
interpretation. Curate paper or review material in the project's report
area when one exists.

## Diagnostic Code

Reuse a parameterized diagnostic when it already exists or will be reused;
a one-off diagnostic can stay local to the analysis. Represent variants
with explicit parameters or configs instead of copied scripts.
