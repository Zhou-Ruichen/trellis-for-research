# Trellis for Research

[Chinese guide](README.zh-CN.md)

Research instructions and an optional task record for Trellis. Small work runs
directly; long-running work preserves its question, state, and evidence.

| Template | Use for |
| --- | --- |
| `research-computational` | Analysis, simulation, traditional ML, and data processing |
| `research-deep-learning` | Deep-learning training, checkpoints, and model comparisons |

Both use the `research` workflow. This is a template repository, not a project
scaffold or a Trellis fork.

## Research Defaults

- Read the minimal rules and relevant project facts. Other specs answer concrete
  questions; they are not a checklist to load for every task.
- Use existing code or a direct script/notebook. No package, config system,
  compatibility layer, or test suite is required for an exploratory calculation.
- Check assumptions that could silently change scientific results. Let ordinary
  file and library errors propagate; diagnose failures when they occur.
- Execute the planned comparisons, seeds, and folds. Scientific metrics are
  observations, including negative and null results, not task pass thresholds.
- Preserve the inputs, actual settings, code state, environment, and outputs
  needed to interpret retained evidence. Existing logs, configs, notebooks, or
  task notes can provide the record. No manifest schema or output relocation.
- Create a task only for context that must survive sessions, independent
  deliverables, or an explicit request. No mode or run-tier declaration.
- Sub-agents are optional. No automatic check agent, repeated review, or software
  verification beyond the task or user's explicit request.
- Write findings with their evidence, interpretation, and actual limits. Keep
  Methods precise. Do not invent results or present software status as science.

Project-specific data conventions and existing code organization remain in place.
Mixed-language projects follow the same research rules.

## Installation

The latest tagged template is `v0.4.3`, targeting Trellis `0.7.0-beta.3`.
The simplifications described above are under **Unreleased** in
[CHANGELOG.md](CHANGELOG.md); the pinned commands below install the tagged release.

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --claude --codex
```

For deep learning, use `--template research-deep-learning`.
Remove the tag only when you intentionally want the published development branch.

### Existing Projects

Preserve customized specs and project records. `--overwrite` replaces the entire
`.trellis/spec/` directory; reserve it for untouched generic defaults.
Install the chosen version in a temporary directory and merge relevant changes,
keeping the project's data conventions, paths, tasks, and results.

`--append` adds missing spec files only. It does not update existing instructions:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --template research-computational \
  --append --claude --codex
```

### Workflow Updates

Inspect local workflow edits before replacing the selected template:

```sh
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.3 \
  --force
```

The project configuration uses `default_workflow: research`. Trellis treats a
non-native selected workflow as user-managed. Restart the agent session after
changing its workflow context.

The template changes workflow instructions, not every separately installed
skill or agent. An explicitly invoked native checker can carry different rules;
its use must follow the task's research and verification constraints.

## Project Use

The installed `shared/research-minimal.md` is the entry point.
`shared/index.md` and `guides/index.md` point to optional references.

A recorded task keeps its question, plan, and state in `prd.md`. Record results
once in `result.md` or link to existing evidence. Seeds and parameter variants
remain runs within the same question unless they are independent deliverables.
Additional context files, journals, and spec updates are used only when needed.

An untouched bootstrap-guidelines task from Trellis is not required by this
workflow. Keep any real project work it already contains.

## Repository Checks

When verification is requested:

```sh
python3 scripts/validate.py
```

The script checks marketplace metadata, paths, links, workflow-state blocks,
ASCII path/content rules, release pins, and installation shape when Trellis is
available. It does not enforce exact spec wording or establish scientific validity.

The published `v0.4.2` release was previously installed with Trellis
`0.7.0-beta.3`. That historical check does not verify the unreleased changes.

## Examples

- `examples/project-layout/`: one possible layout, not a required scaffold.
- `examples/minimal-run/`: a runnable linear-regression example with config and
  manifest files. These files demonstrate one recording choice; new experiments
  need not reproduce its structure or tests.

The examples have not been rewritten as part of the instruction simplification.

## Repository Layout

- `marketplace/specs/`: the two independently installable research templates.
- `marketplace/workflows/research.md`: the shared workflow.
- `examples/`: optional examples.
- `scripts/validate.py`: repository structure checks.

[MIT License](LICENSE)
