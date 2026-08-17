# Changelog

Notable changes to this Trellis spec-template repository. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) as git tags. Pin a version with
`trellis init --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#<tag>`.

## v0.3.6 - 2026-08-17

One-invocation ownership and complete overlay verification. No new skill,
agent, hook, or workflow mode.

### Changed
- Phase 2.1 prepares code and configuration without executing the experiment.
  Phase 2.2 owns the single result-producing invocation and applies its sanity
  check to that same invocation.
- `trellis-research-check` now states explicitly that its one execution both
  produces the requested observation and supplies the outputs being checked.
- Task `research/` directories are limited to Markdown investigation notes and
  small metadata. Experiment artifacts stay under project `outputs/`, with
  task results recording paths instead of copies.
- The research-workflow README now matches the Phase 2.1 behavior.

### Fixed
- `apply.sh --verify` compares all four overlay-owned installed files with
  their masters instead of checking an implement-agent phrase and skill-file
  existence. Normal apply runs the same complete verification before reporting
  success.
- Includes the post-v0.3.5 implement-agent verification fix without moving the
  existing v0.3.5 tag.

## v0.3.5 - 2026-08-17

Single-owner validation and breadcrumb compression. Final static-rule
release; further changes only from real failure cases.

### Changed
- Phase 2.1 and the implement agent no longer self-check: dispatch
  descriptions say "Do not run the workflow quality check; Phase 2.2 owns
  validation", and the agent report drops the check section. The experiment
  runs exactly once, in the check step.
- The `in_progress` and `in_progress-inline` breadcrumbs are compressed to
  five lines (Trellis recommends roughly 200 bytes per per-turn block).
  Sub-agent dispatch rules, the skill-only statement's detail, and context
  order moved into the Phase 2 body where they are read once, not every
  turn.
- Core Principle 3 softened from "Persist everything" to "Persist what must
  survive the session; evidence depth follows the run tier".
- research-workflow README: the skill is always installed to both the
  Claude and Codex skill locations (matches the script).

### Fixed
- `apply.sh` rejects unknown modes instead of silently behaving like
  dry-run.

## v0.3.4 - 2026-08-17

Fixes for Codex/GPT-5.6 compatibility and two axis-wording regressions.
No new rules.

### Fixed
- `trellis-research-check` is a skill only; workflow no longer claims a
  sub-agent form for it, and Phase 2.2 loads the skill in the main session.
- `apply.sh` installs the skill for Codex too (`.agents/skills/`, the
  shared layer Trellis uses for Codex skills), alongside
  `.claude/skills/`, whenever the project has the platform directory;
  `--verify` checks both.
- Two reversed axis statements corrected to "verification depth follows the
  task mode; evidence recording follows the run tier" (Core Principle 6 and
  the research-workflow README).
- The durable flow in both `in_progress` breadcrumbs now updates spec only
  if durable knowledge exists (Phase 3.3) instead of unconditionally.
- Phase 3.4 no longer re-asks the spec-update question Phase 3.3 already
  answered.
- The validator now anchors the axis wording and the skill-only statement in
  `research-workflow/` so these cannot silently regress.

## v0.3.3 - 2026-08-17

Concept and wording fixes from review; no new mechanisms.

### Changed
- Mode and evidence tier are separated: mode (exploratory / durable)
  controls how code is written and checked; the run tier (scratch / smoke /
  retained) controls what the run records. A retained result no longer
  implies durable code; `prd.md` declares only the mode. Durable is defined
  as code the project keeps and maintains.
- `shared/research-minimal.md`: the check rule now reads "name the concrete,
  plausible failure, use the cheapest check that answers it, do not re-check
  an answered question" (the earlier wording could reject cheap sanity
  checks); "answer two questions" softened to "be able to name" to avoid
  ritual output.
- Exploratory flow no longer loads `trellis-update-spec` by default; Phase
  3.3 first decides whether durable knowledge exists and records "no durable
  knowledge" without loading the skill. Exploratory results go to
  `<task>/result.md`; retained evidence goes to the run manifest.
- `trellis-research-check`: provenance identifiers are required only for
  retained runs; scratch checks confirm the result came from the invocation
  just executed and never create provenance machinery.
- "closing pass" renamed to "final check" throughout the overlay.

### Removed
- The `apply.sh` patch of the official `trellis-check` skill description.
  Routing lives entirely in `workflow.md` and the research-check skill.

### Added
- `scripts/validate.py`: README install pins must match the latest CHANGELOG
  release; `shared/research-minimal.md` added to expected spec shape with
  required-content checks.

## v0.3.2 - 2026-08-17

Research workflow overlay and minimal-code rules. Verification depth now
follows the task mode (exploratory by default, durable on request) instead
of a single software-engineering standard.

### Added
- `research-workflow/` overlay: master `workflow.md` (two-mode flows in the
  `in_progress` breadcrumbs with an explicit stop condition; Phase 2.2 split
  by mode; Phase 3.3 spec updates restricted to durable knowledge), master
  `agents/implement.md` (mode-aware closing pass), the
  `trellis-research-check` one-pass sanity skill, an idempotent `apply.sh`
  with `--dry-run` and `--verify`, and a README covering coexistence with
  `trellis update`.
- `shared/research-minimal.md` in both templates: highest-priority minimal
  code rules. Mode-conditional defaults (exploratory adds no defensive
  code, boundary checks, hash/checksum logic, exception handling, retries,
  unit tests, strict typing, or abstractions without a concrete likely
  failure), the utility test for any added check (what failure does it
  catch, what changes once found), and the stop condition.
- Certainty discipline in `shared/scientific-writing.md` (both templates):
  state findings at the strength the evidence supports, report uncertainty
  once, state limitations once.

### Changed
- `shared/index.md` (both templates) lists `research-minimal.md` first.
- Checksum rules in `data/index.md` were verified to already be limited to
  durable data products; no change needed.

## v0.3.1 - 2026-08-17

Exploration discipline and anti-bloat sharpening. Verification regimes built
for maintained software (TDD, coverage, metric gates) are kept out of
exploratory research code; the anti-bloat rules gain a reuse ladder and
explicit handling of one-off test code; the anti-AI-tone word lists are
synced with the global agent rules.

### Added
- Verification boundaries in both templates (`evaluation/index.md`): hard
  gates apply to code, never to scientific outcomes; no TDD, coverage
  targets, or metric-value assertions; a missed target is a finding to
  report, not a task failure; validation commands check executability and
  sanity only.
- Completion-gate rules in `guides/code-review.md` (both templates) and the
  run/experiment guides (`guides/add-run.md`, `guides/add-experiment.md`):
  no metric target is written as a completion gate.
- One-off test code rules in `shared/anti-bloat.md` (both templates):
  scratch tests are deleted once they answer their question; `tests/` holds
  only durable checks.

### Changed
- `shared/anti-bloat.md` (both templates) gains a reuse ladder before new
  code or new dependencies: this codebase, then an already-installed
  dependency (for research code, usually the scientific stack), then the
  standard library, then one line, then the minimum implementation.
- `shared/scientific-writing.md` (both templates) syncs its banned-phrase
  lists with the global agent rules: English additions (underscore(s),
  showcasing, intricate, "at its core", "when it comes to", load-bearing),
  a verbatim Chinese banned-phrase list, more empty adjectives, the
  "not just X, it's Y" rephrasing pattern, and an em-dash ban.
- `scripts/validate.py` exempts `scientific-writing.md` from the
  content-ASCII rule so the Chinese banned phrases appear verbatim.

## v0.3.0 - 2026-07-25

A scientific-writing layer is added alongside the existing engineering contracts
(anti-bloat, reproducibility). The engineering contracts are unchanged in
spirit; this release makes agent-written reports read as science rather than
engineering logs, and makes the templates installable and demoable end to end.

### Added
- Scientific-writing layer in both templates (`shared/scientific-writing.md`):
  science-first narrative order, engineering-term isolation, anti-AI-tone rules
  covering both mechanical stiffness and over-ornamentation (English and
  Chinese), bilingual policy, figure/table and report rules, and a self-check.
- `guides/write-results.md` in both templates: workflow for result discussions
  and paper drafts.
- Runnable example `examples/minimal-run/`: synthetic linear regression
  exercising data manifest, config, training, retained-run manifest with
  environment freeze, scratch/smoke tiers, and a bilingual result discussion.
- MIT `LICENSE`.
- Checkable geoscience data contracts in `dl-earth-research/data/index.md`
  (netCDF/Zarr, CRS, time dimension, chunking, external pointers, checksums) and
  a scientific-data-formats section in `research-core/data/index.md`.
- `Relationship With Trellis Defaults`, `Examples`, and `License` sections in
  the root README.
- `example-smoke` CI job (build, smoke train, re-evaluate, pytest).
- Maintainer sync-notes on the four duplicated template files.

### Changed
- `marketplace/index.json` descriptions and tags now mention the writing layer
  and the netCDF/Zarr data contracts.
- `scripts/validate.py` enforces the new files in required-content and
  spec-shape, and relaxes the ASCII-content check to `examples/` only (Chinese
  writing samples live there; the portable spec tree stays ASCII).
- Install commands in the README now point at `#v0.3.0`.

### Fixed
- `evaluate.py` path bug: a repo-relative manifest path was double-joined onto
  the run directory.
- Self-check taxonomy: `leverage` is now listed under over-ornamentation in both
  the body and the self-check (it was split across categories).
- Stale `buzzwords` wording in `evaluation/index.md` quality checks aligned with
  the renamed Anti AI Tone section.

## v0.2.0 and earlier

Predate this changelog. See git history.
