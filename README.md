# Trellis for Research

[Chinese installation guide](README.zh-CN.md)

Reusable Trellis spec templates and an inline workflow for computational
research.

This repository supplies two kinds of Trellis marketplace template:

- `spec` templates installed into `.trellis/spec/`;
- a `workflow` template installed into `.trellis/workflow.md` through
  `trellis workflow`.

`research-workflow/workflow.md` is the authoritative workflow source. The
marketplace copy is byte-for-byte identical and `scripts/validate.py` rejects
drift. `research-workflow/apply.sh` is a deprecated, read-only migration
checker; it no longer installs or replaces files.

It is not a project scaffold or a Trellis fork.

The templates currently cover:

- `research-core` (General Computational Research): language-agnostic rules for
  non-DL analysis, simulations, traditional ML, data processing, evaluation,
  and reproducible result claims.
- `dl-earth-research` (Geoscience Deep Learning): PyTorch-oriented training,
  evaluation, checkpoints, geospatial data, and anti-bloat conventions.

The Geoscience Deep Learning template targets:

- deep-learning training and evaluation;
- SWOT, altimetry, gravity, bathymetry, and related geoscience data workflows;
- reproducible experiment management;
- anti-bloat rules for research code: superseded variants are deleted (git
  history is the archive), while run artifacts and experiment records are
  protected.

Both templates also include a scientific-writing layer that keeps reports and
discussions readable as science rather than engineering logs: prose leads with
the finding, engineering terms stay in code and methods, AI tone (both the
mechanical "does not speak human" style and the flowery over-ornamented style,
in English or Chinese) is stripped, and bilingual prose (including Chinese) is
supported.

## Scope

- General Computational Research (`research-core`) is language-agnostic and
  layout-tolerant. It is the default choice for non-DL computational research.
- Geoscience Deep Learning (`dl-earth-research`) is Python-first, not
  Python-only. The layout and style bindings
  (`src/<pkg>/`, `pyproject.toml`, `python-style.md`) target Python/PyTorch,
  which is the expected main language. Its anti-bloat, reproducibility, run
  manifest, data manifest, and environment-recording rules are language-agnostic
  and apply to any code in the repo.
- Mixed-language work (CUDA/C++ extensions, Fortran kernels, Julia or Rust
  tooling, shell scripts) follows the same rules; add a per-language style
  file in the project's own spec when that language carries durable code.
- Designed for new projects. Existing projects with a customized spec should
  follow the adoption section below instead of `--overwrite`.
- Covers code structure, experiment management, data handling, and anti-bloat.
  CI/CD, deployment, and monitoring are intentionally out of scope; add them as
  separate spec layers if a project needs them.

## Template Selection

| Template | Use when | Avoid when |
| --- | --- | --- |
| General Computational Research (`research-core`) | Non-DL research, simulation, traditional ML, data analysis, reproducible pipelines, existing projects that need research discipline | The project needs DL-specific training/checkpoint/ablation rules |
| Geoscience Deep Learning (`dl-earth-research`) | Geoscience projects with deep-learning training, PyTorch evaluation, checkpoints, ablations, or geospatial data workflows | The project is non-DL and only needs generic research reproducibility |

Use the tagged registry for repeatable installs.

For non-DL research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --claude --codex
```

For deep-learning geoscience research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template dl-earth-research \
  --claude --codex
```

Use the unpinned `main` registry only when you intentionally want the latest
template changes:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace \
  --template research-core \
  --claude --codex
```

For an existing Trellis project, prefer `--append`: it adds only spec files
that are missing and never touches files the project has customized:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --append \
  --claude --codex
```

Use `--overwrite` only when replacing a generic
or incorrect spec:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --overwrite \
  --claude --codex
```

## Research Workflow

The workflow targets Trellis 0.6.16. For a new non-DL research repository,
install the `research-core` spec and `research` workflow together from the same
release:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --claude --codex
```

For geoscience deep learning, replace `research-core` with
`dl-earth-research`. Codex dispatch defaults to `auto` in Trellis 0.6.16, so
set inline dispatch after initialization:

```yaml
codex:
  dispatch_mode: inline
```

With that setting, implementation and checking stay in the main session. The
workflow does not require custom implement or check agents and does not curate
JSONL context for those agents. The marketplace `trellisVersion` field is an
audit marker; Trellis 0.6.16 does not enforce it during installation.

For an already initialized Trellis project, install only the workflow with:

```sh
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0
```

Both commands pin `v0.4.0`. Do not use `main` for a normal project install.

The installation has three execution paths:

- Exploratory research makes one result-producing invocation. That invocation
  supplies the sanity observation; there is no separate test suite, automatic
  retry, or repeat after a pass without new failure evidence.
- Documentation, archive, and configuration-only tasks receive diff review
  only, with no build or test. A configuration change that affects executable
  behavior is durable work instead.
- Durable code receives only the smallest relevant check. Project instructions
  that require user approval before tests or builds remain controlling.

Scientific metric values do not determine task completion. Unexpected
scientific results are recorded as findings, and retained results keep the
project's provenance and claim-review requirements.

For an existing project, use this sequence:

1. Run `trellis update --create-new` and review the runtime sidecars before
   accepting Trellis-managed changes.
2. Set `codex.dispatch_mode: inline` explicitly in `.trellis/config.yaml` for
   Codex projects. The 0.6.16 default is `auto`.
3. Run the workflow command above with `--create-new`. This writes
   `.trellis/workflow.md.new` without changing the active workflow or its hash
   state.
4. Compare the active file with the `.new` file. When replacement is intended,
   rerun the workflow command without `--create-new`; add `--force` only after
   reviewing local workflow edits.
5. Restart AI sessions. The non-native workflow is user-managed, so Trellis
   0.6.16 removes `.trellis/workflow.md` from `.template-hashes.json` and later
   `trellis update` runs do not silently restore the native workflow.

Projects previously using the overlay can preview migration without writes:

```sh
./research-workflow/apply.sh <project-dir> --dry-run
```

The old script's default apply mode now fails before writing. The marketplace
workflow does not reference `.trellis/agents/implement.md`; let `trellis
update` manage that runtime file and do not copy the removed repository patch
back into a project.

## Adopting Into An Existing Project

`--overwrite` replaces the whole `.trellis/spec/` directory. If the project
already has a customized spec (project-specific directory structure, data
contracts, captured learnings), do not overwrite it. Instead:

- Prefer `research-core` for generic adoption.
- Copy only the layout-independent guides (`shared/anti-bloat.md` and
  `shared/reproducibility.md`) into the existing spec layer if full template
  installation would conflict with project-specific structure.
- Keep the project's own documented layout. An established repo's
  `directory-structure.md` or equivalent wins.
- Prepend a short note in copied files mapping template paths to the repo's
  actual module layout.

Reserve `--overwrite` for specs that are still untouched Trellis defaults.

## Relationship With Trellis Defaults

`trellis init` writes generic project-level placeholders into `.trellis/`
(project notes, environment and conventions docs, and so on). These templates
install into `.trellis/spec/` as a dedicated research-engineering layer and do
not remove those project-level placeholders.

Recommended strategy: overlay, do not replace.

- The template's `spec/` tree is authoritative for research-engineering
  concerns: code layout, anti-bloat, reproducibility, data contracts,
  evaluation, and scientific writing. Keep Trellis's project-level placeholders
  (outside `spec/`) for environment, tooling, and team notes.
- Each area has its own `index.md` (`shared/`, `data/`, `evaluation/`,
  `training/`, `guides/`). These are template-owned; if a Trellis default also
  provides an area index, prefer the template's research index for
  research-engineering rules.
- For non-conflicting task guides, merge them into `guides/` rather than
  duplicating. When a Trellis default and this template disagree on a
  research-engineering rule, the template wins; record any deliberate
  divergence in the project spec so it is visible.
- Confirm the exact placeholder set against the Trellis version in use, then
  keep this template as the research layer on top of it.

## Local Validation

Run:

```sh
python3 scripts/validate.py
```

The validator checks:

- Trellis marketplace `index.json` schema;
- spec directory and workflow Markdown path existence;
- the declared Trellis 0.6.16 audit marker and explicit Codex inline setting;
- authoritative workflow and marketplace mirror equality;
- balanced workflow-state blocks and required research stop rules;
- pinned workflow release references and rejection of common write commands or
  file redirections in the deprecated script;
- markdown links inside the spec;
- core research requirements;
- ASCII-only paths and contents;
- local `.trellis/spec` installation shape when the `trellis` CLI is installed.

The validator cannot prove remote registry installation until this repository is
published. After publishing, verify with:

```sh
tmpdir="$(mktemp -d)"
cd "$tmpdir"
git init
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --template research-core \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.0 \
  --claude --codex -y
grep -F '<!-- trellis-compatibility: 0.6.16 -->' .trellis/workflow.md
find .trellis/spec -type f | sort
```

## What The Templates Enforce

- `research-core` preserves existing project layout while enforcing retained
  evidence for result claims.
- `dl-earth-research` recommends modern Python layout with importable code
  under `src/<pkg>/`.
- Configs, parameters, or retained commands are the source of truth for run
  knobs.
- `data/` is allowed, but it must be organized by lifecycle and tracked with
  manifests.
- `outputs/<run_id>/` is the source of truth for retained run artifacts;
  scratch and smoke runs stay lightweight and disposable unless promoted.
- No `train_v2.py`, `*_final.py`, duplicate experiment scripts, or backup
  directories as normal development patterns.
- Superseded code variants are deleted by the task that replaces them rather
  than accumulated; git history is the archive. Suspected-dead code, bulk
  cleanup, and run artifacts (`outputs/`, `data/manifests/`, configs still
  referenced by results) require asking first.
- New code and dependencies follow a reuse ladder: this codebase first, then
  an already-installed dependency (for research code, usually the scientific
  stack), then the standard library, then one line; only after all four fail,
  the minimum implementation the task needs. One-off test code is deleted
  once it answers its question; `tests/` holds only durable checks.
- Verification boundaries fit exploratory research: hard gates apply to code
  (runs, shapes and units, loud boundary errors, construction-level sanity
  properties) and never to scientific outcomes. No TDD, coverage targets, or
  metric-value assertions; a missed target is reported as a finding, not a
  task failure. Validation commands check executability and sanity only.
- `shared/research-minimal.md` sets the highest-priority minimal-code rules:
  mode-conditional defaults, a utility test for any added check, and a stop
  condition once the result is established.
- The marketplace `research` workflow provides inline exploratory,
  documentation/configuration-only, and durable paths. The optional
  `trellis-research-check` skill repeats the embedded exploratory checklist for
  standalone use; it is not an installation dependency.
- Exploratory Trellis tasks use `prd.md` and `result.md` by default.
  `research/`, `design.md`, and `implement.md` are added only when their stated
  planning condition applies. The inline workflow does not curate JSONL
  sub-agent context.
- Retained runs do not overwrite earlier evidence when the question, method,
  data, split, preprocessing, metric, baseline, or claim scope changes. Task
  completion records completed work; manuscript and external claims still
  require researcher review of the evidence, scope, uncertainty, and limits.
- Result discussions, methods, and reports lead with the scientific finding,
  keep engineering terms out of prose, and strip AI tone (mechanical stiffness
  and flowery over-ornamentation) with verbatim banned-phrase lists in
  English and Chinese; the scientific-writing
  layer (`shared/scientific-writing.md` and `guides/write-results.md` in each
  template) defines the rules and a self-check.

## Examples

- `examples/project-layout/` shows the target directory shape for a new
  `dl-earth-research` project. It is a layout reference, not runnable code.
- `examples/minimal-run/` is a minimal runnable project: synthetic
  one-feature linear regression that demonstrates a retained run
  (data manifest, config, training, retained-run manifest with environment
  freeze, and a bilingual result discussion written in the scientific style).
  See `examples/minimal-run/README.md` for how to run it.

## Repository Layout

```text
marketplace/
  index.json
  workflows/
    research/
      workflow.md    # validated mirror of the authoritative source
  specs/
    dl-earth-research/
      shared/        # incl. scientific-writing.md
      data/
      training/
      evaluation/
      guides/        # incl. write-results.md
    research-core/
      shared/        # incl. scientific-writing.md
      data/
      evaluation/
      guides/        # incl. write-results.md
research-workflow/
  workflow.md        # authoritative source
  apply.sh           # deprecated read-only migration checker
  skills/trellis-research-check/  # optional standalone copy
examples/
  project-layout/    # layout reference
  minimal-run/       # runnable end-to-end demo
scripts/
  validate.py
LICENSE
```

The marketplace schema follows Trellis `index.json` requirements: a `templates`
array with entries containing string `id`, `type`, `name`, and `path` fields.

## License

Released under the [MIT License](./LICENSE).
