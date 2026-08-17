# Research Workflow Overlay

A lighter `.trellis` workflow for exploratory research. It replaces the
software-engineering default (implement -> full check -> verify) with a
two-mode flow where verification depth follows the evidence tier, not task
size.

## Mode

Each task's `prd.md` declares its mode on line 1:

- `Mode: exploratory` (default when absent): validate an idea, run an
  experiment, answer a question. One sanity pass, then stop.
- `Mode: durable`: reusable infrastructure, data contracts, or paper-table
  evidence that later work builds on. Full check (lint, type-check, tests).

Do not promote a task to durable on the AI's own judgment; ask the user.

## What changes relative to the stock workflow

1. `workflow.md` (master copy here):
   - Request Triage and the `no_task` / `planning` breadcrumbs set the mode
     at task creation.
   - The `in_progress` breadcrumbs carry two flows plus a stop condition:
     once the requested result is established and the mode's checks pass,
     stop. No extra certainty without a concrete failure signal; no re-running
     checks that already passed; an unexpected scientific result is a finding,
     not a bug.
   - Phase 2.1 dispatch descriptions close with the mode's pass instead of
     unconditional lint/type-check.
   - Phase 2.2 is split by mode: exploratory runs one sanity pass via
     `trellis-research-check`; durable runs the full `trellis-check`.
     Any added check must answer: what failure does it catch, and what would
     you do differently once it finds one?
   - Phase 3.3 (spec update) accepts durable knowledge only; single-run
     observations go to run records, and exploratory tasks may record
     "no durable knowledge" and skip.
2. `agents/implement.md` (master copy here): the channel implement agent
   reads the mode, writes the minimum code, and closes with the mode's pass.
3. `skills/trellis-research-check/`: a one-pass sanity skill for exploratory
   tasks (executes, shapes/units, NaN/Inf, result from the stated run;
   explicitly no hashes, no repeats, no auto-fix).
4. A one-line description patch on the official `trellis-check` skill so
   exploratory work routes to `trellis-research-check` instead.

## Usage

```bash
# after trellis init in a project:
./research-workflow/apply.sh <project-dir>            # apply
./research-workflow/apply.sh <project-dir> --dry-run  # preview
./research-workflow/apply.sh <project-dir> --verify   # read-only check
```

Idempotent: files already matching the masters are left alone and produce no
new backups. Replaced files get a `.backup-<timestamp>` copy next to them.
Restart AI sessions in the project after applying so hooks reload the
workflow.

## Coexistence with `trellis update`

- `.trellis/workflow.md` and `.trellis/agents/implement.md` are tracked by
  `.template-hashes.json`. A later `trellis update` will detect these local
  modifications and ask; choose to keep the local version, or re-run
  `apply.sh` after updating.
- `trellis-research-check` is a file owned by this overlay; the Trellis
  updater does not manage it.
- The `trellis-check` description edit is a local modification of a bundled
  skill (bundled skills are hash-tracked in recent versions); on update,
  keep the local version or re-run `apply.sh`.
