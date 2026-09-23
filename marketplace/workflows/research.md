# Research Workflow

Work directly under `shared/research-minimal.md`. Small exploratory work can
stay in the main session and in the project's existing scripts, notebooks, and
result files. Use a Trellis task when a question must survive a session
change, an independent deliverable needs its own context, or the user asks
for a task record.

## Trellis Interface

Trellis 0.7 uses the six state blocks below to load the right context.

[workflow-state:no_task]
Work from the research question and the project's existing facts. Short
calculations stay in the current session.
[/workflow-state:no_task]

[workflow-state:planning]
If a task record is useful, write the question, inputs, and next action in
`prd.md` and continue when they are clear.
[/workflow-state:planning]

[workflow-state:planning-inline]
Keep the question and next action in the current conversation.
[/workflow-state:planning-inline]

[workflow-state:in_progress]
Read the question and run the calculation. Put the result and rerun
information in the task's `result.md` or the project's existing result record
when they matter later.
[/workflow-state:in_progress]

[workflow-state:in_progress-inline]
Run the calculation in the main session and keep only the useful result note.
[/workflow-state:in_progress-inline]

[workflow-state:completed]
Report the result, its conditions, and its location. Keep a note only when
future work needs it.
[/workflow-state:completed]

## Working order

1. State the question and the observation needed.
2. Reuse the existing entrypoint, data, and output location. Add structure only
   when it simplifies the current calculation.
3. Run the smallest useful case or comparison. Inspect an input assumption
   only when an error could silently change the result.
4. Record the result and the command, parameters, data pointer, code revision,
   and seed or environment detail needed to rerun it.
5. Stop when the requested observation is delivered with the direct support
   needed to interpret it. Keep a task record or project note only when it
   will help a later session.

When a task record is useful, the native commands remain available:

```bash
python3 ./.trellis/scripts/task.py create "<title>" --slug <name>
python3 ./.trellis/scripts/task.py start <name>
python3 ./.trellis/scripts/task.py current --source
python3 ./.trellis/scripts/task.py finish
python3 ./.trellis/scripts/task.py archive <name>
```
