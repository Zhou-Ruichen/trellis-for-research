# Research Code Review

Review when the task needs it, against the requested calculation and
evidence; this guide adds no separate review stage or reviewer agent.

- Does the code perform the intended calculation on the stated data?
- Could units, missing values, alignment, or data leakage change the result?
- Do the reported observations come from the stated outputs?
- Did the change add wrappers, duplicated logic, or unrelated work the task
  does not need?

The absence of a test suite alone is not a defect, and tests are not
mandated here; assess whether the evidence supports the requested
calculation. Execution and testing rules are in
[research-minimal.md](../shared/research-minimal.md); report actual
problems with file references, and do not manufacture findings to fill a
checklist.
