# Research Workflow

This project uses Trellis as a small research record, not as an approval or
software-delivery process. The research question, evidence, and result matter;
Trellis files exist only when they help preserve those things.

## Principles

1. Work directly on conversations, small edits, read-only analysis, and tasks
   that can finish in one session.
2. Create a Trellis task only when work must survive sessions, has independent
   deliverables, involves collaboration, or the user asks for a task record.
3. Exploratory work is the default. Write the smallest code or prose that
   answers the research question.
4. Validate external data once where it enters the project. Do not add repeated
   internal checks, fallback behavior, retries, abstractions, or test machinery
   without a concrete failure they address.
5. Run an experiment only when the request needs a result. Use its first
   successful result-producing invocation for the sanity check, then stop.
6. Write for researchers: state what data were used, what was compared, what
   changed, and what the evidence supports. Do not expose Trellis terminology
   as if it were a scientific result.

## Compatibility

The six `[workflow-state:*]` blocks are the interface consumed by Trellis 0.7
hooks. Keep their names and matching close tags. The task commands remain the
stock Trellis commands; this file changes guidance, not the CLI or runtime.

```bash
python3 ./.trellis/scripts/task.py create "<title>" --slug <name>
python3 ./.trellis/scripts/task.py start <name>
python3 ./.trellis/scripts/task.py current --source
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive <name>
```

## Task Record

When a task record is useful, keep it small:

- `prd.md`: first line is `Mode: exploratory` or `Mode: durable`; then record
  the question or requested behavior, inputs, outputs, and the result that can
  change the next decision.
- `research/*.md`: only findings that must survive the session. Do not copy
  datasets, logs, figures, or generated outputs into the task directory.
- `result.md`: the command or evidence actually used, the observation, output
  paths, and limitations that change interpretation.
- `design.md`, `implement.md`, `implement.jsonl`, and `check.jsonl`: use only
  when a real interface decision, dependency, collaboration need, or sub-agent
  context requires them. Empty or seed-only JSONL files are valid when no
  sub-agent needs injected context.

`Mode: exploratory` covers experiments, analysis, and one-off research code.
`Mode: durable` is for code the repository will maintain, such as loaders,
data contracts, shared processing, and reusable training or evaluation code.
Do not promote exploratory code because a result is retained or cited.

## Request Routing

- No active task: do the work directly unless a task record meets the criteria
  above.
- Planning task: make `prd.md` sufficient for the work, then start the task.
  Do not create extra planning files to represent the same information.
- Active task: read `prd.md` and only the spec files relevant to the files or
  prose being changed.
- Prose task: load `.trellis/spec/shared/scientific-writing.md`; for a result
  discussion or report, also load `.trellis/spec/guides/write-results.md`.
- Data task: load the relevant data spec and validate the consumed columns,
  units, coordinates or time convention, and missing-value convention once at
  the project boundary.
- Sub-agents are optional. Use them only for bounded work that benefits from
  separate context or parallel execution; Trellis does not require dispatch.

## Phase Index

[workflow-state:no_task]
No active task. Work directly on conversation, small edits, read-only analysis,
and work that can finish in this session. Create a Trellis task only for work
that must survive sessions, has independent deliverables, involves
collaboration, or when the user explicitly asks for a task record.
[/workflow-state:no_task]

[workflow-state:planning]
Keep planning in prd.md: mode, question or requested behavior, inputs, outputs,
and the result that can change the next decision. Add other artifacts only for
a real interface decision, dependency, or sub-agent context need. Start the
task once this information is sufficient; Trellis adds no second approval.
[/workflow-state:planning]

[workflow-state:planning-inline]
Keep planning in prd.md: mode, question or requested behavior, inputs, outputs,
and the result that can change the next decision. Skip JSONL context files for
inline work. Start once the record is sufficient; Trellis adds no second
approval.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Read prd.md and directly relevant specs. Make the smallest change that answers
the task. For an experiment, use one result-producing invocation and its output
for the focused sanity check. For prose, check evidence and claim strength
without inventing an invocation. Record the result once, update specs only for
reusable knowledge, and stop when the question is answered. Commits may preserve
completed work without a separate approval. Never discard changes or rewrite
history. Push, PR, and task archive actions follow the user's request.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Read prd.md and directly relevant specs. Work in the main session. For an
experiment, use one result-producing invocation and its output for the focused
sanity check. For prose, check evidence and claim strength without inventing an
invocation. Record the result once and stop when the question is answered.
Commits may preserve completed work without a separate approval. Never discard
changes or rewrite history. Push, PR, and task archive actions follow the user.
[/workflow-state:in_progress-inline]

[workflow-state:completed]
The recorded task result is complete. Archive or write a session journal only
when that record is useful; do not create bookkeeping solely to satisfy
Trellis.
[/workflow-state:completed]

## Phase 1: Prepare

#### 1.0 Decide whether a task record is useful

Skip Trellis for small or single-session work. When a durable record is useful,
create one task. Split parent and child tasks only when deliverables can be
completed independently.

#### 1.1 Write the minimum plan

Write or update `prd.md`. Research unclear facts before asking the user. Ask
only when the missing decision changes the scientific question, implementation,
cost, external side effect, or risk.

#### 1.2 Research when needed

Search code, data, or primary sources to answer a specific unresolved question.
Persist a short note only when the finding must survive the session. Do not
turn ordinary inspection into a literature report.

#### 1.3 Load relevant context

Read the smallest set of spec and research files that affects the task. For
exploratory code, start with `.trellis/spec/shared/research-minimal.md`. Add the
data spec for data work and the scientific-writing files for human-facing
research prose.

#### 1.4 Start work

For a recorded task, run `task.py start <name>` when `prd.md` is sufficient.
Starting records state; it is not a second approval step. Add context entries
only when a dispatched sub-agent needs them.

#### 1.5 Ready condition

The next action, required inputs, expected output, and scientific decision are
clear enough to work without guessing.

## Phase 2: Do the Research Work

#### 2.1 Implement or write

Work directly by default. If a sub-agent is useful, give it the active task
path and the exact bounded responsibility. Exploratory implementation does not
run the experiment during preparation. Pure prose tasks do not create or run
code to satisfy this phase.

#### 2.2 Focused check

Choose the branch that matches the work:

- Exploratory experiment: run the requested path once. On that invocation,
  check the external input fields that affect interpretation, obvious
  shape/dtype/unit/time errors, NaN/Inf, and that the reported observation came
  from the same output. Do not repeat a successful run for reassurance.
- Durable code: use the narrowest check required by the task and project
  instructions. Trellis does not add lint, type checking, tests, or full-suite
  runs on its own.
- Scientific prose: compare claims with the cited evidence, keep uncertainty
  and scope accurate, apply `scientific-writing.md`, and do not manufacture an
  executable check.
- Documentation or configuration: inspect the changed content and its direct
  references. Run a command only when the task or user authorizes it.

Before adding any check, name the plausible failure and how its result changes
the next action. If it does not change the decision, do not add the check.

#### 2.3 Record the result

For a recorded task, write `result.md` once. Include the actual evidence or
invocation, observation, useful output paths, and only limitations that change
interpretation. A task result records work completed; it does not approve a
claim for publication.

## Phase 3: Preserve What Matters

#### 3.1 Learn from repeated failure

Write a debugging note only after repeated failures reveal a reusable cause.
Do not create a retrospective for ordinary iteration.

#### 3.2 Update specs when knowledge is reusable

Update a spec only for a stable interface, confirmed invariant, reusable data
convention, or lesson observed beyond one isolated run. Do not record "no
durable knowledge" or promote a tentative result into project rules.

#### 3.3 Preserve work with Git

Inspect the diff and preserve unrelated work. A normal commit may record
completed work without a separate approval. Never reset, discard changes,
rewrite history, or force-push. Push and PR creation follow the user's request.

#### 3.4 Finish without ceremony

Archive the task or record a session only when future work benefits from it.
Otherwise report the result and stop.
