# Research Minimal Code (Highest Priority)

On conflict with any other spec file, this one wins for exploratory work.

Write the smallest change that answers the current question for the stated
inputs. Prefer existing project code or a library function (see
[anti-bloat.md](./anti-bloat.md)). A direct script or notebook is sufficient;
add a function or module only when it removes actual duplication or makes the
calculation easier to follow. Do not add wrappers, configuration layers, or
compatibility paths for possible future use.

Exploratory mode is the default. Durable mode applies when the user designates
a component for ongoing maintenance. Reusing code, project duration, and
retaining or publishing results do not change the mode. The evidence tier
(scratch / smoke / retained, per [reproducibility.md](./reproducibility.md))
controls what the run records, independently of the code's mode.

In exploratory mode, validate external inputs once where they enter the
project when schema, columns, units, coordinates, time, or missing values can
change the result. Trust those inputs afterward and let indexing and library
errors propagate with their tracebacks. Fix an observed failure with the smallest
correction; do not add defensive branches, exception handling, retries, strict
typing, or abstractions for hypothetical failures.
In durable mode, apply only the maintenance requirements the user requested.

Software tests, lint, type checks, and separate verification runs require an
explicit task or user request. Use the experiment's own outputs for checks of
execution, data isolation, units, finite values where expected, and provenance.
When an actual failure needs diagnosis, use the cheapest check that locates it
and remove temporary diagnostics afterward. Do not repeat a successful run for
reassurance or add tests solely because code was added, reused, or fixed.

Retained runs record the command, inputs, configuration, and outputs needed to
interpret or reproduce the result. Record a checksum only when exact byte
identity matters; checksum logic never appears scattered through experiment
code.

Stop condition: the task is done once the requested result is established,
every run the design requires has completed, and the outputs support the
reported observations. Metric values are observations, not pass/fail criteria:
a negative or null result is recorded as evidence and answered with the next
run the task plan registered, not with a stop or a route-level conclusion.
Completing a task or a full set of runs does not end exploration on its own: opening a
sealed evaluation (final test period, held-out data) or freezing the
explored configuration closes the exploratory phase, so take that step only
when the task's registered decision is answered and the user confirms.
Do not seek additional certainty without a concrete failure signal.
