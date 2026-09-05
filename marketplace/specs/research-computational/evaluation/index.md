# Evaluation Guidelines

Evaluation answers the stated scientific question. Keep the comparison
fair: use the same data and conditions where the design requires them,
state which parameters differ, and report units, sample set, split, and
exclusions. Check only input assumptions that affect the calculation, such
as shape, schema, dtype, units, coordinates, or data isolation; let actual
failures guide further debugging.

## Metrics And Results

Choose the metrics and result form the question and existing project
conventions require; there is no required JSON schema or fixed metrics
file. Record actual values, conditions, definitions, and relevant output
paths in the project's existing record, log, notebook, or report.

A result that misses an expectation is still a scientific finding: report
the value, the comparison conditions, and a plausible interpretation
without turning the expectation into a pass/fail criterion.

## Figures And Tables

Keep generated figures and tables with the run or analysis that produced
them, using the project's existing paths, and put curated paper or review
material in the report area when one exists. Each comparison makes clear
what was compared and under which conditions; do not rely on numbers copied
from a dashboard when the underlying evidence is unavailable.

## Diagnostic Code

Parameterize a diagnostic when it is reused; a one-off investigation can
stay in a small local script or notebook. Keep variants as explicit
parameters or configuration values rather than copied files.
