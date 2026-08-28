# Research Workflow

<!-- trellis-compatibility: 0.6.16 -->
<!-- authoritative-source: research-workflow/workflow.md -->

---

## Core Principles

1. **Plan before editing**: define the requested output, data roles, constraints, and stop rule before implementation.
2. **Use the main session**: this workflow is designed for inline execution. Do not dispatch implement or check sub-agents and do not curate JSONL context for them.
   Codex projects must explicitly set `codex.dispatch_mode: inline`; Trellis 0.6.16 defaults Codex to `auto`.
3. **Classify the work**: use exploratory, documentation, or durable mode. The mode controls checking; the run evidence tier controls provenance.
4. **Produce one research result**: exploratory work has one result-producing invocation. The same invocation supplies the sanity observation.
5. **Preserve evidence**: retained results record the command, configuration, code revision, environment, inputs, outputs, and limitations required by the project spec.
6. **Report scientific outcomes as findings**: unexpected scientific results are findings, not software failures to tune away. Scientific metric values are never task-completion gates.

---

## Trellis System

### Developer Identity

On first use, initialize your identity:

```bash
python3 ./.trellis/scripts/init_developer.py <your-name>
```

This creates `.trellis/.developer` and `.trellis/workspace/<your-name>/`.

### Spec System

`.trellis/spec/` contains project guidelines. Read only the indexes and linked files relevant to the requested change.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
```

Update a spec only for stable interfaces, confirmed invariants, reusable conventions, repository structure decisions, or a lesson observed across more than one task. A single experimental outcome is not a spec rule.

### Task System

Each task lives under `.trellis/tasks/{MM-DD-name}/` and contains `task.json`, `prd.md`, optional planning or research files, and `result.md` after execution.

```bash
# Task lifecycle
python3 ./.trellis/scripts/task.py create "<title>" [--slug <name>] [--parent <dir>]
python3 ./.trellis/scripts/task.py start <name> --allow-empty-context
python3 ./.trellis/scripts/task.py current --source
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive <name>
python3 ./.trellis/scripts/task.py list [--mine] [--status <s>]
python3 ./.trellis/scripts/task.py list-archive

# Context inspection. Inline research normally leaves these manifests absent or empty.
python3 ./.trellis/scripts/task.py list-context <name> [action]
python3 ./.trellis/scripts/task.py validate <name>

# Task metadata
python3 ./.trellis/scripts/task.py set-branch <name> <branch>
python3 ./.trellis/scripts/task.py set-base-branch <name> <branch>
python3 ./.trellis/scripts/task.py set-scope <name> <scope>

# Hierarchy
python3 ./.trellis/scripts/task.py add-subtask <parent> <child>
python3 ./.trellis/scripts/task.py remove-subtask <parent> <child>
```

Trellis 0.6.16 seeds context manifests only on platforms and modes that use them. `task.py validate` fails while a seeded manifest remains empty, and `task.py start` refuses it unless `--allow-empty-context` is supplied. Empty context is intentional here because the main session reads the task and relevant specs directly. Do not describe seed-only context as validated context.

`task.py create` creates the task and, when session identity is available, selects it for the current session. `task.py start` changes `task.json.status` from `planning` to `in_progress`. Session pointers live under `.trellis/.runtime/sessions/`. `task.py finish` clears the current session pointer without changing task status. `task.py archive` writes `status=completed`, moves the directory to `archive/`, and clears pointers that still target it.

Run `python3 ./.trellis/scripts/task.py --help` for the installed command contract.

### Workspace System

Session journals live under `.trellis/workspace/<developer>/`. Record only information that must survive the session.

```bash
python3 ./.trellis/scripts/add_session.py --title "Title" --commit "hash" --summary "Summary"
```

### Context Script

```bash
python3 ./.trellis/scripts/get_context.py
python3 ./.trellis/scripts/get_context.py --mode packages
python3 ./.trellis/scripts/get_context.py --mode phase --step <X.Y>
```

---

<!--
  [workflow-state:*] blocks are the source for per-turn breadcrumbs. The hook
  parser has no embedded copy. Every required once-only step must remain
  represented in the corresponding state block.
-->

## Phase Index

```text
Phase 1: Plan    -> classify, obtain task and implementation consent, write the minimum artifacts
Phase 2: Execute -> edit inline, then apply the mode-specific check once
Phase 3: Finish  -> record findings, decide whether specs change, commit with approval, wrap up
```

### Request Triage

- Ask for consent before creating a Trellis task. Task creation does not authorize implementation.
- Write one of these on line 1 of `prd.md`:
  - `Mode: exploratory`, the default for experiments, analyses, and result-producing scripts.
  - `Mode: documentation`, for documentation, archive, or configuration-only work that does not execute code. If a configuration change affects executable behavior, use durable mode.
  - `Mode: durable`, for maintained loaders, pipelines, interfaces, data contracts, and reusable software.
- Do not change modes without user agreement when that changes the amount of implementation or checking.
- Evidence tier is separate from mode. Retained scientific results keep the provenance required by the project spec even when their code is exploratory.

### Planning Artifacts

- `prd.md` is required. For exploratory work, record the scientific question, fixed comparison, requested output, and interpretation limits. Metric values may guide interpretation but never decide whether the task is complete.
- `design.md` is optional. Create it only for a user-reviewed interface, data-role, compatibility, or rollback decision.
- `implement.md` is optional. Create it only when real dependencies, coordination, migration, or rollback cannot be expressed by a config or run manifest.
- `research/` holds Markdown investigation notes and small metadata. Datasets, predictions, checkpoints, figures, and run directories stay under the project's output paths.
- `result.md` records the actual invocation or diff review, findings, output paths, and limitations. Do not copy planned checklists into it.
- Inline mode does not need `implement.jsonl` or `check.jsonl`.

<!-- Per-turn breadcrumb: shown when there is no active task. -->

[workflow-state:no_task]
No active task. Classify the request and ask for task-creation consent before creating a Trellis task.
When creating a task, set prd.md line 1 to Mode: exploratory, Mode: documentation, or Mode: durable. Default to exploratory; do not promote the mode without user agreement.
Task creation is not implementation approval.
[/workflow-state:no_task]

<!-- Per-turn breadcrumb: shown when the active task record cannot be read. -->

[workflow-state:task_error]
The active task record could not be read. Do not create or activate another task.
Inspect the task directory named above and repair its task.json. It must be a valid JSON object with a non-empty status.
Preserve existing task fields and artifacts. If the correct status cannot be determined safely, ask the user before reconstructing the record.
[/workflow-state:task_error]

### Phase 1: Plan

- 1.0 Create task `[required · once]`
- 1.1 Define requirements and mode `[required · repeatable]`
- 1.2 Research `[optional · repeatable]`
- 1.3 Confirm inline context `[required · once]`
- 1.4 Activate task `[required · once]`
- 1.5 Completion criteria

[workflow-state:planning]
Stay in planning. Read the task directly in the main session; do not dispatch implement/check sub-agents or curate JSONL for them.
On Codex, confirm `.trellis/config.yaml` explicitly sets `codex.dispatch_mode: inline`; the 0.6.16 default is `auto`.
Keep exploratory tasks PRD-only unless a specific optional-artifact condition applies.
After the user reviews the artifacts and authorizes implementation, start with `task.py start <task> --allow-empty-context` because empty context is intentional for this workflow.
[/workflow-state:planning]

<!-- Codex selects this block when codex.dispatch_mode=inline. -->

[workflow-state:planning-inline]
Stay in planning. Codex inline is the preferred execution mode.
Read the task directly; skip JSONL curation and create optional planning files only when their stated condition applies.
After artifact review and implementation approval, run `task.py start <task> --allow-empty-context`.
[/workflow-state:planning-inline]

### Phase 2: Execute

- 2.1 Implement inline `[required · repeatable]`
- 2.2 Apply the mode-specific check `[required · once per completed change]`
- 2.3 Roll back `[on demand]`

[workflow-state:in_progress]
Read the mode from prd.md line 1; default exploratory. Work in the main session without implement/check sub-agents.
Exploratory: edit without executing, then make one result-producing invocation; the same invocation supplies the sanity observation. No separate test suite, automatic retry, or repeat after a pass without new failure evidence.
Documentation: review the diff only; do not run a build or test.
Durable: run only the smallest relevant check authorized by the user and project instructions; do not start repeated full-suite cycles.
Record the invocation or diff review and findings in result.md, decide whether durable spec knowledge exists, then obtain commit approval.
[/workflow-state:in_progress]

<!-- Codex selects this block when codex.dispatch_mode=inline. -->

[workflow-state:in_progress-inline]
Read the mode from prd.md line 1; default exploratory. Edit directly in the main Codex session.
Exploratory: one result-producing invocation supplies the sanity observation; no separate suite, automatic retry, or repeat after a pass without new failure evidence.
Documentation: diff review only; do not run a build or test.
Durable: use the smallest relevant check and honor project-specific user approval boundaries before tests or builds.
Record result.md, decide whether specs change, and obtain commit approval. Do not dispatch sub-agents.
[/workflow-state:in_progress-inline]

### Phase 3: Finish

- 3.2 Debug retrospective `[on demand]`
- 3.3 Spec update decision `[required · once]`
- 3.4 Commit changes `[required · once]`
- 3.5 Wrap-up reminder

[workflow-state:completed]
Code committed. Run `/trellis:finish-work`; if the worktree is dirty, return to Phase 3.4.
[/workflow-state:completed]

### Rules

1. Follow required steps in order. Do not repeat a once-only step whose output exists.
2. A missing optional artifact is valid unless its stated condition applies.
3. Execution that exposes a requirement error returns to Phase 1. A software failure may return to implementation after it is localized.
4. A negative or surprising scientific value is recorded and does not trigger automatic tuning, retry, or broader testing.
5. Completion means the requested output was produced and the applicable check was recorded. It does not approve a manuscript or external scientific claim.

### Active Task Routing

- Planning or unclear requirements: load `trellis-brainstorm` when available.
- Before editing: read `prd.md`, optional planning files, relevant task research, and only the project specs needed for the change. Codex may use `trellis-before-dev`.
- After editing: apply Phase 2.2 directly in the main session. The workflow contains the full research check and does not require a custom check agent or skill.
- Repeated software debugging: use `trellis-break-loop` when available. Spec updates use `trellis-update-spec` only after Phase 3.3 finds durable knowledge.

### Guardrails

- Do not edit before `task.py start` succeeds after artifact review and user approval.
- Do not make metric thresholds completion gates.
- Do not weaken source, lineage, retained-run, or claim-review requirements to make a result pass.
- Do not overwrite earlier retained artifacts when the question, method, data, split, preprocessing, metric, baseline, or claim scope changes. Create a new run record and preserve the earlier evidence.

---

## Phase 1: Plan

#### 1.0 Create task `[required · once]`

After task-creation consent:

```bash
python3 ./.trellis/scripts/task.py create "<task title>" --slug <name>
```

Do not include the date prefix in `--slug`. Do not run `start` in the same step. Skip creation when `task.py current --source` already points to the correct task.

#### 1.1 Define requirements and mode `[required · repeatable]`

Write the mode on line 1 of `prd.md`. State inputs, requested outputs, constraints, retained-evidence requirements, and the stop rule. For exploratory work, state the scientific question and the minimal comparison whose result can change the interpretation. Do not require a preferred metric value for completion.

Ask for user decisions only when the answer changes the requested output, scientific comparison, destructive risk, or verification authority.

#### 1.2 Research `[optional · repeatable]`

Research unresolved facts in the main session. Write only findings that must survive the session to `{TASK_DIR}/research/`. Keep large artifacts in the project's normal output locations and link them from `result.md`.

#### 1.3 Confirm inline context `[required · once]`

Read `prd.md`, optional `design.md` and `implement.md`, relevant `research/` notes, and the smallest relevant part of `.trellis/spec/`. Do not curate `implement.jsonl` or `check.jsonl`. On Codex, confirm `.trellis/config.yaml` explicitly sets `codex.dispatch_mode: inline`; Trellis 0.6.16 defaults to `auto`, and the legacy `sub-agent` value is an alias for `auto`.

#### 1.4 Activate task `[required · once]`

After the user reviews the artifacts and authorizes implementation:

```bash
python3 ./.trellis/scripts/task.py start <task-dir> --allow-empty-context
```

The flag is deliberate. This workflow supplies context by direct main-session reads, so an absent or empty JSONL manifest is not an error. Without the flag, Trellis 0.6.16 may refuse the start when a seeded manifest is empty.

If the command reports a session-identity error, follow the installed command's hint and retry. Do not create a second task.

#### 1.5 Completion criteria

| Condition | Required |
| --- | :---: |
| `prd.md` exists and declares a valid mode | yes |
| User authorized implementation after artifact review | yes |
| `task.py start ... --allow-empty-context` succeeded | yes |
| Optional planning or research file exists when its condition applies | conditional |

---

## Phase 2: Execute

#### 2.1 Implement inline `[required · repeatable]`

Edit in the main session. Follow existing project structure and implement the smallest change that produces the requested output. Do not execute the experiment or run checks during this step; Phase 2.2 owns that action.

For documentation, archive, and configuration-only work, make only the requested textual or declarative change. If a configuration change affects executable behavior, return to Phase 1 and reclassify it as durable with user agreement.

#### 2.2 Apply the mode-specific check `[required · once per completed change]`

**Exploratory**

- Make one result-producing invocation.
- Use that same invocation to observe executability, relevant shapes, coordinates and units, NaN/Inf or clearly invalid outputs, and whether the reported result came from the stated run.
- Keep retained-run provenance required by the project spec. Do not add provenance machinery to scratch work.
- Do not run a separate test suite, retry automatically, fix a scientific outcome, or repeat after a pass without new failure evidence.
- If the invocation exposes a concrete software failure, stop and report it. A user-authorized fix leads to one new result-producing invocation because the previous invocation did not pass.

**Documentation**

- Review the diff against `prd.md` and the authoritative files it changes.
- Do not run a build, test, linter, type checker, or output comparison.

**Durable**

- Name the concrete software failure the check targets and choose the smallest relevant check.
- If project instructions require explicit user approval for tests or builds, request it and stop before running them.
- Do not run repeated full suites. A passed relevant check is not repeated without new failure evidence.

Write the actual invocation or diff review, observation, findings, output paths, and interpretation-changing limitations once in `<task>/result.md`. Task completion does not approve a scientific claim for publication or external release.

#### 2.3 Roll back `[on demand]`

- A requirement or mode error returns to Phase 1.
- A localized software implementation error returns to Phase 2.1 after the user-authorized scope is clear.
- A negative scientific outcome stays in `result.md`; do not change the protocol to erase it.

---

## Phase 3: Finish

#### 3.2 Debug retrospective `[on demand]`

Use a retrospective only after repeated software failures. Record a stable lesson only when the evidence supports one. Do not reinterpret an unexpected scientific result as a debugging loop.

#### 3.3 Spec update decision `[required · once]`

Decide whether the task produced durable knowledge. If no, record `no durable knowledge` and continue. If yes, update the smallest relevant spec. Single-run outcomes, tentative hypotheses, and temporary debugging notes stay in task or run records.

#### 3.4 Commit changes `[required · once]`

Inspect `git status --porcelain` and recent commit style. Separate files edited for this task from unrecognized dirty files. Present one commit plan with messages and exact paths, then wait for user confirmation. Commit only the approved files. Do not amend, push, merge, or include unrecognized changes.

#### 3.5 Wrap-up reminder

After the approved commit step, remind the user that `/trellis:finish-work` archives the task and records the session.

---

## Customizing Trellis

Edit the installed `.trellis/workflow.md` to customize local step text. Marketplace workflows are user-managed, so Trellis 0.6.16 removes `.trellis/workflow.md` from `.template-hashes.json` instead of overwriting it during `trellis update`.

The state blocks above must stay balanced and use names matching `[A-Za-z0-9_-]+`. A custom task status also needs a lifecycle hook that writes that status to `task.json`.

Supported lifecycle events are `after_create`, `after_start`, `after_finish`, and `after_archive`. `after_finish` clears the active pointer; it does not change task status.

The installed platform hook is the authoritative parser. Inspect the hook
registered for the active client, for example
`.codex/hooks/inject-workflow-state.py` or
`.claude/hooks/inject-workflow-state.py`.
