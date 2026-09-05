# Trellis for Research

[Chinese guide](README.zh-CN.md)

Research instructions and an optional task record for Trellis. Small work
runs directly; long-running work preserves its question, state, and evidence.

| Template | Use for |
| --- | --- |
| `research-computational` | Analysis, simulation, traditional ML, and data processing |
| `research-deep-learning` | Deep-learning training, checkpoints, and model comparisons |

Both use the `research` workflow. This is a template repository, not a
project scaffold or a Trellis fork.

## Research Defaults

- Start from `shared/research-minimal.md` plus project facts; other specs
  answer concrete questions instead of loading as a checklist.
- Reuse existing code or a direct script/notebook. No package, config
  system, or compatibility layer is required for an exploratory calculation;
  errors propagate with tracebacks and are diagnosed where they occur.
- Focused checks the work needs are part of the work: matched comparisons
  and planned seeds, one boundary check for assumptions that could silently
  change results, and the experiment's own outputs as evidence. No default
  test suite, lint or type pass, check agent, or repeated re-runs.
- Metrics are observations, including negative and null results, never task
  pass thresholds.
- Preserve the inputs, settings, code state, environment, and outputs needed
  to interpret retained evidence, reusing existing records. No manifest
  schema or output relocation.
- Keep held-out data isolated under the project's stated restrictions; task
  completion does not declare results final or exploration finished.
- Tasks are for context that must survive sessions, independent
  deliverables, or explicit requests; sub-agents are optional helpers.
- Write findings with evidence, interpretation, and actual limits; do not
  invent results or present software status as science.

Project-specific data conventions and existing code organization remain in
place; mixed-language projects follow the same rules. These defaults are
unreleased development-branch changes; the last published release stays `v0.5.0`,
with differences recorded in [CHANGELOG.md](CHANGELOG.md).

## Installation

The current template release is `v0.5.0`, targeting Trellis
`0.7.0-beta.3`. See [CHANGELOG.md](CHANGELOG.md) for what changed.

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
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
trellis update --migrate --dry-run
trellis update --migrate
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
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0 \
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
    source: gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.5.0
    template: research-computational
```

`--save` writes `.trellis/workflows/research.md`, leaves the native global
workflow intact, and does not set the project default. Keep the workflow
release and spec source tag aligned, and restart the agent session after
changing context. Inline dispatch keeps ordinary Codex work in the main
session; independent agents remain available when useful.

Keep native Trellis scripts, hooks, skills, and agents unchanged so they
follow upstream updates; generic native skills may carry their own routing
or verification procedures and are not invoked automatically by this
workflow. In an existing project's `AGENTS.md`, outside the managed Trellis
block, point to `.trellis/workflows/research.md` and
`.trellis/spec/shared/research-minimal.md` as the research entry points,
keeping project-specific conventions alongside them. A future change to
Trellis's workflow format or loader may still require a template update.
Custom skill paths absent from the template are not replaced by normal
updates, and the registry source must be a supported remote source, not a
local checkout path.

## Project Use

The installed `shared/research-minimal.md` is the entry point;
`shared/index.md` and `guides/index.md` point to optional references.

Describe the scientific question directly; small work needs no task or
slash command. With session hooks, opening a session loads Trellis context;
`/trellis:start` is for platforms without automatic session loading. A
recorded task keeps its question, plan, and state in `prd.md` and records
results once in `result.md` or links existing evidence. Seeds and parameter
variants remain runs within the same question unless they are independent
deliverables.

`/trellis:continue` advances the current task; `/trellis:finish-work`
archives completed work and writes a journal after the work is committed.
These native commands are optional and follow the research workflow's
rules; they are not additional approval stages.

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
blocks, ASCII rules, release pins, and installation shape when Trellis is
available. It does not enforce exact spec wording.

Validation of these unreleased changes covers repository checks and native
context loading in a temporary Trellis `0.7.0-beta.3` project. These changes
have not been deployed to existing research projects.

## Examples

- `examples/project-layout/`: brief layout guidance, without placeholder files.
- `examples/minimal-run/`: one standard-library regression script, its actual
  result, and a short scientific report. No package installation or run tiers.

## Repository Layout

- `marketplace/specs/`: the two independently installable research templates.
- `marketplace/workflows/research.md`: the shared workflow.
- `examples/`: optional examples.
- `scripts/validate.py`: repository structure checks.

[MIT License](LICENSE)
