# Trellis for Research

[Chinese installation guide](README.zh-CN.md)

Small Trellis spec templates and a research workflow for computational
projects. Trellis records research when a durable record helps; it does not add
approval stages to ordinary work.

This repository supplies two marketplace resources:

- `marketplace/`: spec templates installed into `.trellis/spec/`;
- `marketplace/workflows/research.md`: a Trellis 0.7 workflow that keeps small
  work direct, gives exploratory experiments one focused check, and leaves
  durable-code checks to the task and project instructions.

It is not a project scaffold or a Trellis fork.

Choose one spec template for a repository; both use the same `research`
workflow. The templates currently cover:

- `research-computational` (General Computational Research): language-agnostic rules for
  non-DL analysis, simulations, traditional ML, data processing, evaluation,
  and reproducible result claims.
- `research-deep-learning` (Deep Learning Research): PyTorch-oriented training,
  evaluation, checkpoints, experiment records, and anti-bloat conventions.

The Deep Learning Research template targets:

- deep-learning training and evaluation;
- scientific data from any domain or modality;
- reproducible experiment management;
- anti-bloat rules for research code: superseded variants are deleted (git
  history is the archive), while run artifacts and experiment records are
  protected.

Both templates include scientific-writing guidance for evidence-supported
claims, exact Methods descriptions, and plain English or Chinese. The rules
identify mechanical and ornamental AI-style prose, but they are instructions
and a self-check, not a deterministic text filter.

## Scope

- General Computational Research (`research-computational`) is language-agnostic and
  layout-tolerant. It is the default choice for non-DL computational research.
- Deep Learning Research (`research-deep-learning`) is Python-first, not
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
  It does not prescribe CI/CD, deployment, or monitoring; project rules may add
  them when the research repository uses them.

## Template Selection

| Template | Use when | Avoid when |
| --- | --- | --- |
| General Computational Research (`research-computational`) | Non-DL research, simulation, traditional ML, data analysis, reproducible pipelines, existing projects that need research discipline | The project needs DL-specific training/checkpoint/ablation rules |
| Deep Learning Research (`research-deep-learning`) | Research projects with deep-learning training, evaluation, checkpoints, or model comparisons | The project is non-DL and only needs general research reproducibility |

Use the tagged registry for repeatable installs.

The workflow targets Trellis `0.7.0-beta.3` and the 0.7 marketplace workflow
interface. The stable npm tag is still 0.6.x as of this revision, so install the
0.7 beta explicitly until 0.7 becomes the stable release:

```sh
npm install -g @mindfoldhq/trellis@0.7.0-beta.3
```

For non-DL research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --claude --codex
```

For deep-learning research:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --template research-deep-learning \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --claude --codex
```

For an existing Trellis 0.7 project, select or refresh the workflow through the
same marketplace entry:

```sh
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --force
```

Trellis treats a non-native selected workflow as user-managed, so
`trellis update` does not silently restore the native workflow over it.

Use the unpinned `main` registry only when you intentionally want the latest
template changes:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace \
  --claude --codex
```

For an existing Trellis project, prefer `--append`: it adds only spec files
that are missing and never touches files the project has customized:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --template research-computational \
  --append \
  --claude --codex
```

Use `--overwrite` only when replacing a generic
or incorrect spec:

```sh
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --template research-computational \
  --overwrite \
  --claude --codex
```

## Adopting Into An Existing Project

`--overwrite` replaces the whole `.trellis/spec/` directory. If the project
already has a customized spec (project-specific directory structure, data
contracts, captured learnings), do not overwrite it. Instead:

- Prefer `research-computational` for generic adoption.
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
- the six workflow-state interface blocks;
- ASCII-only paths and contents;
- local `.trellis/spec` installation shape and the research workflow template.

The validator cannot prove remote registry installation until this repository is
published. After publishing, verify with:

```sh
tmpdir="$(mktemp -d)"
cd "$tmpdir"
git init
trellis init \
  --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --template research-computational \
  --workflow research \
  --workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --claude --codex -y
find .trellis/spec -type f | sort
find .trellis/workflows -type f | sort
trellis workflow \
  --template research \
  --marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#v0.4.2 \
  --force
```

## What The Templates Provide

- `research-computational` preserves existing project layout and records the
  evidence behind result claims.
- `research-deep-learning` keeps an existing repository's documented layout and
  recommends importable code under `src/<pkg>/` only for new Python projects.
- Configs, parameters, or retained commands are the source of truth for run
  knobs.
- `data/` is allowed, but it must be organized by lifecycle and tracked with
  manifests.
- `outputs/<run_id>/` is the source of truth for retained run artifacts;
  scratch and smoke runs stay lightweight and disposable unless promoted.
- Do not copy the current source implementation into `train_v2.py`, `*_final.py`,
  or backup directories. Version labels remain valid for datasets, schemas,
  interfaces, releases, and protocols that intentionally coexist.
- Superseded code variants are deleted by the task that replaces them rather
  than accumulated; git history is the archive. Suspected-dead code, bulk
  cleanup, and run artifacts (`outputs/`, `data/manifests/`, configs still
  referenced by results) require asking first.
- Before adding durable code, search this repository, prefer parameters or
  configs over copied scripts, reuse existing dependencies or the standard
  library, then add the smallest missing implementation. Extract shared code
  after meaningful durable duplication exists, not for possible future reuse.
- Checks fit the research decision: external data is checked once where it
  enters, the study runs every comparison, seed, fold, or repeat its design
  requires, and identical successful commands are not repeated only for
  reassurance. Scientific outcomes are reported rather than treated as software
  failures. Trellis does not add TDD, coverage targets, full test suites, or
  metric-value assertions on its own.
- `shared/research-minimal.md` sets the highest-priority minimal-code rules:
  mode-conditional defaults, a utility test for any added check, and a stop
  condition once the result is established.
- The `research` marketplace workflow is the only workflow customization.
  Small and single-session work does not require a Trellis task. Recorded tasks
  use `prd.md` and `result.md`; other artifacts are added only for a real
  interface, dependency, collaboration, or context need.
- Retained runs do not overwrite earlier evidence when the question, method,
  data, split, preprocessing, metric, baseline, or claim scope changes. Task
  completion records completed work; manuscript and external claims still
  require researcher review of the evidence, scope, uncertainty, and limits.
- Results and discussions state supported findings before engineering status;
  Methods retain the exact technical detail needed for reproduction. The
  scientific-writing layer gives English and Chinese examples of mechanical or
  ornamental AI-style prose and a short self-check.

## Examples

- `examples/project-layout/` shows the target directory shape for a new
  `research-deep-learning` project. It is a layout reference, not runnable code.
- `examples/minimal-run/` is a minimal runnable project: synthetic
  one-feature linear regression that demonstrates a retained run
  (data manifest, config, training, retained-run manifest with environment
  snapshot, and a bilingual result discussion written in the scientific style).
  See `examples/minimal-run/README.md` for how to run it.

## Repository Layout

```text
marketplace/
  index.json
  specs/
    research-deep-learning/
      shared/        # incl. scientific-writing.md
      data/
      training/
      evaluation/
      guides/        # incl. write-results.md
    research-computational/
      shared/        # incl. scientific-writing.md
      data/
      evaluation/
      guides/        # incl. write-results.md
  workflows/
    research.md
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
