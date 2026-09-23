# Trellis for Research

[Chinese guide](README.zh-CN.md)

Research instructions and an optional task record for Trellis. Small work
runs directly; long-running work keeps its question, numbers, and rerun notes.

| Template | Use for |
| --- | --- |
| `research-computational` | Analysis, simulation, traditional ML, and data processing |
| `research-deep-learning` | Deep-learning training and model comparisons |

Both use the `research` workflow. This repository distributes templates for
installation into Trellis projects.

## Research Defaults

- Start from `shared/research-minimal.md` plus project facts; other specs
  answer concrete questions instead of loading as a checklist.
- Reuse existing code or a direct script/notebook. Extra packages, config
  layers, tests, and wrappers are optional and need a concrete reason.
- Run the smallest useful calculation. Add a comparison, seed, or input check
  only when it answers the question or prevents a likely silent error.
- Record the reported number and the small set of command, data, code, seed,
  and environment details needed to rerun it. Keep large outputs outside Git.
- Keep data reserved for final evaluation separate under the project's stated
  restrictions; a finished task records one step in an ongoing investigation.
- Tasks are for context that must survive sessions, independent
  deliverables, or explicit requests. The main session owns ordinary work.
- Write the finding with its number, conditions, interpretation, and actual
  limits in the field's terms. Name the data, method, and settings directly;
  software status is not a finding.

Project-specific data conventions and existing code organization remain in
place; mixed-language projects follow the same rules. Differences between
releases are recorded in [CHANGELOG.md](CHANGELOG.md).

## Installation

The next template release is `v0.6.1`, targeting Trellis `0.7.0-beta.4`.
After publishing that tag, use the pinned commands below. See
[CHANGELOG.md](CHANGELOG.md) for what changed.

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.4
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.1 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.1 \
  --claude --codex
```

For deep learning, use `--template research-deep-learning`. Remove the tag
only when you intentionally want the published development branch.

### Existing Projects And Upgrades

Trellis and this research template have separate versions:

| What changes | Official entry point |
| --- | --- |
| Installed Trellis CLI | `trellis upgrade` follows its current npm channel |
| Project native files and registered specs | `trellis update` uses the installed CLI and configured spec source |
| Research template release | Change the spec source tag and select the same workflow release |

Upgrade the CLI only when adopting a newer supported version;
`trellis upgrade --dry-run` previews that package operation without
touching project files. For project updates, save current work, inspect the
proposed changes, then apply:

```sh
trellis update --dry-run
trellis update
```

Modified files enter conflict handling: merge while preserving project
facts; `--skip-all` keeps local edits and `--force` overwrites conflicts. A
pinned spec source stays on that release until its tag is changed. See the
official [upgrade reference](https://docs.trytrellis.app/zh/start/everyday-use).

For first adoption into an existing project, install the selected template
in a temporary directory and merge its relevant files, keeping data
conventions, paths, tasks, and results. Earlier manual copies need one-time
registration against the published template so future updates can
distinguish templates from local edits. `init --append` adds missing files
only; `init --overwrite` replaces the entire spec directory and suits
untouched generic defaults only.

### Select The Research Workflow

After reviewing local workflow changes, save the selected release as a
variant:

```sh
trellis workflow \
  --save research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.1 \
  --force
```

Merge these fields into `.trellis/config.yaml`, keeping other settings, and
use `research-deep-learning` for the deep-learning spec template:

```yaml
default_workflow: research
codex:
  dispatch_mode: inline
registry:
  spec:
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.6.1
    template: research-computational
```

`--save` writes `.trellis/workflows/research.md`, leaves the native global
workflow intact and keeps the project default unchanged. Keep the workflow
release and spec source tag aligned, and restart the agent session after
changing context. Inline dispatch keeps ordinary Codex work in the main
session; use a sub-agent only when the question needs one.

Keep native Trellis scripts, hooks, skills, and agents so they follow
upstream updates. In an existing project's `AGENTS.md`, point to
`.trellis/workflows/research.md` and
`.trellis/spec/shared/research-minimal.md` as the research entry points.
Use a supported remote registry source.

## Project Use

The installed `shared/research-minimal.md` is the entry point;
`shared/index.md` and `guides/index.md` point to optional references.

Describe the scientific question directly; small work needs no task or
slash command. With session hooks, opening a session loads Trellis context;
`/trellis:start` is for platforms without automatic session loading. If a
question needs a task record, keep its question and next action in `prd.md`
and put the result and rerun information in the task's `result.md` or the
project's existing result record.
Parameter variants can remain under the same question.

`/trellis:continue` advances the current task; `/trellis:finish-work`
archives completed work and writes a journal after the work is committed.
Use these native commands when their task record or journal is useful.

Write project specs from actual data conventions, source paths, and
reusable decisions; add a rule when a real task needs it. The official
[real-world scenarios](https://docs.trytrellis.app/zh/start/real-world-scenarios)
provide engineering examples; adopt only the parts relevant to the research
task. An untouched bootstrap-guidelines task from Trellis is not required
by this workflow; keep any real project work it already contains.

## Repository Checks

```sh
python3 scripts/validate.py
```

The script checks marketplace metadata, paths, links, workflow-state
blocks, ASCII rules, shared-file parity between the two templates, release
pins, and installation shape when Trellis is available.

## Examples

- `examples/project-layout/`: brief layout guidance for the files in use.
- `examples/minimal-run/`: one standard-library regression script, its actual
  result, and a short scientific report.

## Repository Layout

- `marketplace/specs/`: the two independently installable research templates.
- `marketplace/workflows/research.md`: the shared workflow.
- `examples/`: optional examples.
- `scripts/validate.py`: repository structure checks.

[MIT License](LICENSE)
