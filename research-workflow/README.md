# Research Workflow Overlay

A lighter `.trellis` workflow for exploratory research. It replaces the
software-engineering default (implement -> full check -> verify) with a
two-mode flow where verification depth follows the task mode and evidence
recording follows the run tier, not task size.

## Mode and evidence tier

Two independent questions are separated on purpose:

- **Mode** (code): `prd.md` line 1 declares `Mode: exploratory` (default when
  absent) or `Mode: durable` (code the project keeps and maintains: loaders,
  pipelines, data contracts). The mode controls how code is written and how
  deeply it is checked. Do not promote a task to durable on the AI's own
  judgment; ask the user.
- **Evidence tier** (runs): scratch / smoke / retained, decided per run per
  `spec/shared/reproducibility.md`. It controls what the run records.

A retained result (paper-table evidence) does not make exploratory code
durable: a 25-line script for a paper table stays exploratory; its run
records config, command, git revision, environment, and results.

## What changes relative to the stock workflow

1. `workflow.md` (master copy here):
   - Request Triage and the `no_task` / `planning` breadcrumbs set the mode
     at task creation and separate it from the evidence tier.
   - The `in_progress` breadcrumbs carry two flows plus a stop condition:
     once the requested result is established and the mode's checks pass,
     stop. No extra certainty without a concrete failure signal; no re-running
     checks that already passed; an unexpected scientific result is a finding,
     not a bug.
   - Phase 2.1 dispatch descriptions close with the mode's final check
     instead of unconditional lint/type-check.
   - Phase 2.2 is split by mode: exploratory runs one sanity pass via
     `trellis-research-check`; durable runs the full `trellis-check`.
     Any added check must target a concrete, plausible failure and be the
     cheapest check that answers it.
   - Phase 3.3 (spec update) first decides whether durable knowledge exists;
     if not, the task records "no durable knowledge" and moves on without
     loading the update-spec skill.
2. `agents/implement.md` (master copy here): the channel implement agent
   reads the mode, writes the minimum code, and closes with the mode's final
   check.
3. `skills/trellis-research-check/`: a one-pass sanity skill for exploratory
   tasks (executes, shapes/units, NaN/Inf, result from the invocation just
   executed; provenance identifiers only for retained runs; explicitly no
   hashes, no repeats, no auto-fix). It is a skill only — there is no
   sub-agent form; the main session loads it. `apply.sh` installs it for
   Claude Code (`.claude/skills/`) and for Codex (`.agents/skills/`, the
   shared layer Trellis uses for Codex skills) whenever the project has the
   corresponding platform directory.

The official `trellis-check` skill is not patched. Routing lives entirely in
`workflow.md` (state blocks, Phase 2.2, Active Task Routing) and in the
research-check skill's own description, so the overlay only owns its own
files.

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
