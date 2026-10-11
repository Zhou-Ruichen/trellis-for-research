# Research Workflow

## Phase Index

For research work this workflow replaces the native development workflow,
including its task-creation questions, review gates, and default sub-agent
dispatch. Work directly under `.trellis/spec/shared/research-minimal.md` and
the project's own spec facts. Small exploratory work starts in the main
session and in the project's existing scripts, notebooks, and result files,
without a task. Use a Trellis task when a question must survive a session
change, an independent deliverable needs its own context, or the user asks
for a task record.

<!-- Trellis injects the block matching the task status on each turn; Codex
with codex.dispatch_mode: inline reads the -inline variants, which repeat
their base blocks. -->

[workflow-state:no_task]
Work from the research question and the project's existing facts. Short
calculations start in the current session without a task.
[/workflow-state:no_task]

[workflow-state:planning]
Write the question, inputs, and next action in `prd.md`, and start the task
when they are clear.
[/workflow-state:planning]

[workflow-state:planning-inline]
Write the question, inputs, and next action in `prd.md`, and start the task
when they are clear.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Read the question in `prd.md` and run the calculation. Put the result and
rerun information in the task's `result.md` or the project's existing result
record when they matter later.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Read the question in `prd.md` and run the calculation. Put the result and
rerun information in the task's `result.md` or the project's existing result
record when they matter later.
[/workflow-state:in_progress-inline]

[workflow-state:completed]
Report the result, its conditions, and its location. Keep a note when
future work needs it.
[/workflow-state:completed]

#### 1.1 State the question

State the question and the observation needed. For a task record, run
`python3 ./.trellis/scripts/task.py create "<title>" --slug <name> --description "<question>"`,
write the question, inputs, and next action in `prd.md`, and run
`python3 ./.trellis/scripts/task.py start <name> --allow-empty-context` when
they are clear. Main-session work leaves the `implement.jsonl` and
`check.jsonl` sub-agent manifests empty.

#### 2.1 Run the calculation

Reuse the existing entrypoint, data, and output location; add structure when
it simplifies the current calculation. Run the smallest useful case or
comparison. Inspect an input assumption when an error could silently change
the result.

#### 2.2 Record the result

Record the result and the command, parameters, data pointer, code revision,
and seed or environment detail needed to rerun it, in the task's `result.md`
or the project's existing result record.

#### 3.1 Stop

Stop when the requested observation is delivered with the direct support
needed to interpret it. Keep a task record or project note when it will help
a later session. `python3 ./.trellis/scripts/task.py finish` clears the active
task and leaves its record in place, which keeps citations of its `prd.md`
and `result.md` valid; `task.py archive <name>` moves the record under
`.trellis/tasks/archive/`.
