# Research Workflow

An inline workflow for Trellis 0.6.16. It keeps Trellis task-state and safety
behavior while removing the engineering workflow's implement/check dispatch,
curated JSONL context, and repeated verification cycle.

## Sources

`research-workflow/workflow.md` is authoritative. The marketplace requires a
Markdown file inside its own root, so
`marketplace/workflows/research/workflow.md` is an exact mirror.
`python3 scripts/validate.py` compares their bytes and fails on drift.

The marketplace entry has stable ID `research`, type `workflow`, and a
`trellisVersion: 0.6.16` audit marker. Trellis 0.6.16 does not enforce that
field during installation. The workflow repeats the target version in its
header, and the deprecated verifier requires an exact CLI version match.

## Behavior

`prd.md` line 1 selects one mode:

- `Mode: exploratory`: edit first, then make one result-producing invocation.
  The same invocation supplies the sanity observation. There is no separate
  test suite, automatic retry, or repeat after a pass without new failure
  evidence.
- `Mode: documentation`: documentation, archive, and configuration-only work
  receives diff review only. No build or test runs. Configuration that changes
  executable behavior belongs in durable mode.
- `Mode: durable`: use the smallest relevant check. Do not create repeated
  full-suite cycles. Project instructions that require explicit user approval
  before tests or builds remain controlling.

Unexpected scientific results are findings. Scientific metric values do not
decide task completion. Retained scientific results still follow the project's
source, lineage, provenance, uncertainty, and claim-review requirements.

The main session owns implementation and checking. Trellis 0.6.16 defaults Codex to `codex.dispatch_mode: auto`, so a Codex project must explicitly set:

```yaml
codex:
  dispatch_mode: inline
```

This workflow then avoids implement/check sub-agents and does not patch
`.trellis/agents/implement.md`.

Trellis 0.6.16 refuses a seeded empty context manifest at task start unless the
caller explicitly permits it. This workflow reads task artifacts and relevant
specs directly, so activation uses:

```bash
python3 ./.trellis/scripts/task.py start <task-dir> --allow-empty-context
```

Seed-only context is not described as validated context. The explicit flag
records that empty sub-agent context is intentional.

## Installation

For a new non-DL research repository, install the spec and workflow together:

```bash
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --claude --codex
```

Replace `research-core` with `dl-earth-research` for geoscience deep learning.
Then set `codex.dispatch_mode: inline` in `.trellis/config.yaml` as shown above.

For an already initialized Trellis project, install only the workflow:

```bash
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
```

Both commands pin `v0.4.0`. Do not use `main` for normal installation.

Trellis treats every non-native workflow as user-managed. After installation,
0.6.16 removes `.trellis/workflow.md` from `.template-hashes.json`; later
`trellis update` runs cannot silently restore native workflow bytes over it.

## Safe upgrade and migration

For an existing project:

1. Run `trellis update --create-new` and review the generated runtime sidecars.
2. Set `codex.dispatch_mode: inline` in `.trellis/config.yaml` for Codex.
3. Run the marketplace workflow command with `--create-new` and compare
   `.trellis/workflow.md.new` with the active workflow.
4. Rerun without `--create-new` only after review. Add `--force` only when
   replacing local workflow edits is intended.
5. Restart AI sessions after the active workflow changes.

`apply.sh` is deprecated and read-only. Its default apply mode exits before
writing. `--dry-run` reports whether the active workflow differs;
`--verify` checks exact workflow equality, Trellis 0.6.16, balanced state
blocks, and absence of the workflow template hash.

```bash
./research-workflow/apply.sh <project-dir> --dry-run
./research-workflow/apply.sh <project-dir> --verify
```

The script never copies workflow, agent, or skill files. The optional
`skills/trellis-research-check/` directory preserves a standalone copy of the
embedded exploratory checklist, but marketplace installation does not depend
on it.

## Maintenance

Keep all edits in `research-workflow/workflow.md`, then update the marketplace
mirror in the same change. Run only:

```bash
python3 scripts/validate.py
./research-workflow/apply.sh <temporary-project> --verify
```

The `[workflow-state:*]` blocks are the source for per-turn breadcrumbs. The
validator checks balanced names and the required `no_task`, `task_error`,
`planning`, `planning-inline`, `in_progress`, `in_progress-inline`, and
`completed` states. The parser is installed in each configured platform hook
directory, for example `.codex/hooks/inject-workflow-state.py` or
`.claude/hooks/inject-workflow-state.py`.
