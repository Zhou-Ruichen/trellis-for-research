---
name: trellis-research-check
description: Optional standalone copy of the one-pass sanity check embedded in the research marketplace workflow. Establishes that an exploratory path executes, obvious shape/unit/data errors are absent, and the reported observation comes from the same run.
---

# Research Check (exploratory, one pass)

Purpose: execute the experiment once, produce the requested observation, and
establish whether that same invocation is trustworthy enough for the current
research question. This is a single pass. It is not a review cycle.

The marketplace workflow contains these rules directly and does not require
this skill to be installed.

## Check only

- Execute the changed path exactly once. This is the result-producing
  invocation, not a preliminary run before a separate check.
- Obvious shape, dtype, unit, and coordinate errors where relevant.
- NaN/Inf or clearly invalid outputs.
- The reported observation comes from the invocation just executed. Require
  run_id or path provenance only when the run is retained or already carries
  such an identifier; do not create provenance machinery for a scratch check.

## Do not

- Add production hardening.
- Add generic defensive checks.
- Add fallback behavior.
- Introduce abstractions.
- Run unrelated test suites.
- Hash or checksum files unless integrity verification is explicitly required
  by the task; before any such check, be able to name the failure it targets
  and what would change once found.
- Repeat a check that already passed without new evidence.
- Retry automatically after a software or scientific failure.
- Treat an unexpected scientific result as a software failure. A negative or
  surprising outcome is reported, not debugged into a bug hunt.

## Stop rule

After one successful pass over the list above, stop and report. Do not execute
the experiment again or seek additional certainty without a concrete failure
signal.

## Report format

```
## Research Check

- Executes: <yes/no + how invoked>
- Shapes/units: <ok | issue + where>
- NaN/Inf: <absent | found + where>
- Result provenance: <from the invocation just executed | mismatch + detail>
- Findings: <none | list>
```
