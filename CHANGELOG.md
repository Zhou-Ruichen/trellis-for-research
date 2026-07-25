# Changelog

Notable changes to this Trellis spec-template repository. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) as git tags. Pin a version with
`trellis init --registry gh:Zhou-Ruichen/trellis-research-spec/marketplace#<tag>`.

## v0.3.0 - 2026-07-25

A scientific-writing layer is added alongside the existing engineering contracts
(anti-bloat, reproducibility). The engineering contracts are unchanged in
spirit; this release makes agent-written reports read as science rather than
engineering logs, and makes the templates installable and demoable end to end.

### Added
- Scientific-writing layer in both templates (`shared/scientific-writing.md`):
  science-first narrative order, engineering-term isolation, anti-AI-tone rules
  covering both mechanical stiffness and over-ornamentation (English and
  Chinese), bilingual policy, figure/table and report rules, and a self-check.
- `guides/write-results.md` in both templates: workflow for result discussions
  and paper drafts.
- Runnable example `examples/minimal-run/`: synthetic linear regression
  exercising data manifest, config, training, retained-run manifest with
  environment freeze, scratch/smoke tiers, and a bilingual result discussion.
- MIT `LICENSE`.
- Checkable geoscience data contracts in `dl-earth-research/data/index.md`
  (netCDF/Zarr, CRS, time dimension, chunking, external pointers, checksums) and
  a scientific-data-formats section in `research-core/data/index.md`.
- `Relationship With Trellis Defaults`, `Examples`, and `License` sections in
  the root README.
- `example-smoke` CI job (build, smoke train, re-evaluate, pytest).
- Maintainer sync-notes on the four duplicated template files.

### Changed
- `marketplace/index.json` descriptions and tags now mention the writing layer
  and the netCDF/Zarr data contracts.
- `scripts/validate.py` enforces the new files in required-content and
  spec-shape, and relaxes the ASCII-content check to `examples/` only (Chinese
  writing samples live there; the portable spec tree stays ASCII).
- Install commands in the README now point at `#v0.3.0`.

### Fixed
- `evaluate.py` path bug: a repo-relative manifest path was double-joined onto
  the run directory.
- Self-check taxonomy: `leverage` is now listed under over-ornamentation in both
  the body and the self-check (it was split across categories).
- Stale `buzzwords` wording in `evaluation/index.md` quality checks aligned with
  the renamed Anti AI Tone section.

## v0.2.0 and earlier

Predate this changelog. See git history.
