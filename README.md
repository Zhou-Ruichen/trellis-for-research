# Trellis Research Spec

Reusable Trellis spec templates for research projects.

This repository is not a Python project scaffold. It is a ruleset that Trellis
installs into `.trellis/spec/` so AI coding agents follow the same research
engineering conventions across projects.

The templates currently cover:

- `research-core`: language-agnostic research rules for non-DL analysis,
  simulations, traditional ML, data processing, evaluation, and reproducible
  result claims.
- `dl-earth-research`: deep-learning geoscience research with PyTorch-oriented
  training, evaluation, checkpoint, data, and anti-bloat conventions.

`dl-earth-research` targets:

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

- `research-core` is language-agnostic and layout-tolerant. It is the default
  choice for non-DL computational research.
- `dl-earth-research` is Python-first, not Python-only. The layout and style bindings
  (`src/<pkg>/`, `pyproject.toml`, `python-style.md`) target Python/PyTorch,
  which is the expected main language. The core contracts -- anti-bloat,
  reproducibility, run manifests, data manifests, environment recording -- are
  language-agnostic and apply to any code in the repo.
- Mixed-language work (CUDA/C++ extensions, Fortran kernels, Julia or Rust
  tooling, shell scripts) follows the same contracts; add a per-language style
  file in the project's own spec when that language carries durable code.
- Designed for new projects. Existing projects with a customized spec should
  follow the adoption section below instead of `--overwrite`.
- Covers code structure, experiment management, data handling, and anti-bloat.
  CI/CD, deployment, and monitoring are intentionally out of scope; add them as
  separate spec layers if a project needs them.

## Template Selection

| Template | Use when | Avoid when |
| --- | --- | --- |
| `research-core` | Non-DL research, simulation, traditional ML, data analysis, reproducible pipelines, existing projects that need research discipline | The project needs DL-specific training/checkpoint/ablation rules |
| `dl-earth-research` | Geoscience projects with deep-learning training, PyTorch evaluation, checkpoints, ablations, or geospatial data workflows | The project is non-DL and only needs generic research reproducibility |

Use the tagged registry for repeatable installs.

For non-DL research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#v0.3.1 \
  --template research-core \
  --claude --codex
```

For deep-learning geoscience research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#v0.3.1 \
  --template dl-earth-research \
  --claude --codex
```

Use the unpinned `main` registry only when you intentionally want the latest
template changes:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace \
  --template research-core \
  --claude --codex
```

For an existing Trellis project, prefer `--append`: it adds only spec files
that are missing and never touches files the project has customized:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#v0.3.1 \
  --template research-core \
  --append \
  --claude --codex
```

Use `--overwrite` only when replacing a generic
or incorrect spec:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#v0.3.1 \
  --template research-core \
  --overwrite \
  --claude --codex
```

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
- template path existence;
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
  --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#v0.3.1 \
  --template research-core \
  --claude --codex -y
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
  one-feature linear regression that exercises the full contract end to end
  (data manifest, config, training, retained-run manifest with environment
  freeze, and a bilingual result discussion written in the scientific style).
  See `examples/minimal-run/README.md` for how to run it.

## Repository Layout

```text
marketplace/
  index.json
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

Released under the [MIT License](./LICENSE). MIT is chosen over Apache-2.0
because these templates are rulesets (markdown) that get installed into other
projects: the permissive, recognition-friendly terms fit that use, and the
patent-grant machinery of Apache-2.0 adds no value for documentation-only
content.
