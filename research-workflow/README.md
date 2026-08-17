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
   - Phase 2.1 only prepares code and configuration. It does not execute the
     experiment or run a quality check.
   - Phase 2.2 is split by mode: exploratory performs the single
     result-producing invocation and sanity check via `trellis-research-check`;
     durable runs the full `trellis-check`.
     Any added check must target a concrete, plausible failure and be the
     cheapest check that answers it.
   - Phase 3.3 (spec update) first decides whether durable knowledge exists;
     if not, the task records "no durable knowledge" and moves on without
     loading the update-spec skill.
   - Task `research/` directories hold Markdown investigation notes and small
     metadata only. Experiment artifacts stay under project `outputs/`, and
     task results link to them.
   - Exploratory tasks are PRD-only by default, even for multi-step runs.
     `design.md`, `implement.md`, and jsonl context are added only when
     implementation or checking needs them. Phase 2.2 owns check commands, and
     `result.md` records what actually ran plus limitations or uncertainties
     that change the interpretation. Task completion does not approve a
     manuscript or external claim.
2. `agents/implement.md` (master copy here): the channel implement agent
   reads the mode and writes the minimum code. It performs no self
   validation or execution; Phase 2.2 of the workflow owns the result-producing
   invocation and quality check, so the experiment runs exactly once.
3. `skills/trellis-research-check/`: a one-pass sanity skill for exploratory
   tasks (executes, shapes/units, NaN/Inf, result from the invocation just
   executed; provenance identifiers only for retained runs; explicitly no
   hashes, no repeats, no auto-fix). It is a skill only — there is no
   sub-agent form; the main session loads it. `apply.sh` always installs it
   to both the Claude Code location (`.claude/skills/`) and the Codex
   location (`.agents/skills/`, the shared layer Trellis uses for Codex
   skills); the project is expected to run Claude and Codex together.

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

## Maintaining the workflow

The `[workflow-state:*]` blocks in `workflow.md` are the source for per-turn
breadcrumbs. The hook parser reads those blocks and has no embedded copy. Keep
every `[required · once]` step represented in the matching block, including
task activation, conditional spec update, and commit.

The live scopes are `no_task`, `planning`, `planning-inline`, `in_progress`,
and `in_progress-inline`. The `completed` block remains for compatibility but
is not reached by the normal archive flow because archiving also clears the
active-task pointer. A custom status requires both a matching block and a
lifecycle hook that writes that status to `task.json`.

After changing a step or breadcrumb, run `python3 scripts/validate.py`, apply
the overlay to a temporary initialized project, and verify it with
`research-workflow/apply.sh <project-dir> --verify`. The installed Trellis
runtime contract remains authoritative at
`.trellis/spec/cli/backend/workflow-state-contract.md`.
