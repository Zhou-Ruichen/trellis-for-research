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

The current template release is `v0.5.0`, targeting Trellis `0.7.0-beta.3`.
See [CHANGELOG.md](CHANGELOG.md) for the research defaults in this release.

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --claude --codex
```

For deep learning, use `--template research-deep-learning`.
Remove the tag only when you intentionally want the published development branch.

### Existing Projects And Upgrades

Trellis and this research template have separate versions:

| What changes | Official entry point |
| --- | --- |
| Installed Trellis CLI | `trellis upgrade` follows its current npm channel |
| Project native files and registered specs | `trellis update` uses the installed CLI and configured spec source |
| Research template release | Change the spec source tag and select the same workflow release |

Upgrade the CLI only when adopting a newer supported version. `trellis upgrade
--dry-run` previews that package operation; it does not update project files.
For project updates, preserve existing work, inspect the proposed changes, then
apply the migration:

```sh
trellis update --migrate --dry-run
trellis update --migrate
```

Modified files enter conflict handling. Merge the changes while preserving project
facts; `--skip-all` keeps local edits and `--force` overwrites conflicts. A pinned
spec source stays on that release until its tag is changed. See the official
[upgrade reference](https://docs.trytrellis.app/zh/start/everyday-use).

For a first adoption into an existing project, install the selected template in
a temporary directory and merge its relevant files. Keep data conventions, paths,
tasks, and results. Earlier manual copies need a one-time registration against the
published template so future updates can distinguish templates from local edits.
`init --append` adds missing files only; it is not a refresh of customized specs.
`init --overwrite` replaces the entire spec directory and is suitable only for
untouched generic defaults.

### Select The Research Workflow

After reviewing local workflow changes, save the selected release as a variant:

```sh
trellis workflow \
  --save research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --force
```

Merge these fields into `.trellis/config.yaml`, keeping other settings. Use
`research-deep-learning` for the deep-learning spec template:

```yaml
default_workflow: research
codex:
  dispatch_mode: inline
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0
    template: research-computational
```

`--save` writes `.trellis/workflows/research.md` and leaves the native global
workflow intact; it does not set the project default. Keep the workflow release
and spec source tag aligned. Restart the agent session after changing context.
Inline dispatch keeps ordinary Codex work in the main session; independent agents
remain available when useful.

The template changes workflow instructions, not every separately installed
skill or agent. An explicitly invoked native checker can carry different rules;
its use must follow the task's research and verification constraints.

Keep native Trellis scripts, hooks, skills, and agents unchanged so they can
follow upstream updates. For ordinary research, use the selected workflow
directly and call its task CLI only when needed. Generic native skills can
carry their own phase routing or verification procedures; do not invoke them
automatically to implement this research workflow.

In an existing project's `AGENTS.md`, outside the managed Trellis block, point
to `.trellis/workflows/research.md` and `.trellis/spec/shared/research-minimal.md`
as the research entry points. Keep project-specific conventions alongside them.
This avoids maintaining patched copies of native skills. A future change to
Trellis's workflow format or loader may still require a template update.

Custom skill paths absent from the template are not replaced by normal updates.
The registry source must be a supported remote source, not a local checkout path.

## Project Use

The installed `shared/research-minimal.md` is the entry point.
`shared/index.md` and `guides/index.md` point to optional references.

Describe the scientific question directly. Small work needs no task or slash
command. With working session hooks, opening a session loads Trellis context;
`/trellis:start` is for platforms without automatic session loading.

A recorded task keeps its question, plan, and state in `prd.md`. Record results
once in `result.md` or link to existing evidence. Seeds and parameter variants
remain runs within the same question unless they are independent deliverables.
Additional context files, journals, and spec updates are used only when needed.

`/trellis:continue` advances the current task. `/trellis:finish-work` archives
completed work and writes a journal after the work is committed. These native
commands are optional here; their use follows the research workflow's execution
and verification rules. They are not additional approval stages.

Write project specs from actual data conventions, source paths, and reusable
decisions. Add a rule when a real task needs it; do not fill every template or
turn a single experimental observation into a permanent requirement. The official
[real-world scenarios](https://docs.trytrellis.app/zh/start/real-world-scenarios)
provide engineering examples; adopt only the parts relevant to the research task.

An untouched bootstrap-guidelines task from Trellis is not required by this
workflow. Keep any real project work it already contains.

## Repository Checks

When verification is requested:

```sh
python3 scripts/validate.py
```

The script checks marketplace metadata, paths, links, workflow-state blocks,
ASCII path/content rules, release pins, and installation shape when Trellis is
available. It does not enforce exact spec wording.

The simplified spec and workflow have been installed in existing research
repositories with Trellis `0.7.0-beta.3`, including native phase and step loading.

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
