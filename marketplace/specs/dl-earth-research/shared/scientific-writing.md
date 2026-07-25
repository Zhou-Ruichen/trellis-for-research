<!--
Maintainer note: the sibling template carries an equivalent copy of this file
with domain examples adapted (research-core is generic; dl-earth-research is
geoscience). Mirror structural changes -- section headings, self-check items,
cross-reference targets -- across both copies unless a change is genuinely
domain-specific. The duplication is structural: Trellis installs each template
directory as a standalone flat copy into .trellis/spec/, so the two cannot share
a single source file.
-->

# Scientific Writing

These rules govern how prose is written for this project: results discussions,
methods text, paper drafts, figure and table captions, and curated reports.
Code, configs, manifests, and commit messages are engineering artifacts and are
not affected by this file.

The goal: reports and discussions should read as geoscience, not as a build log
or a system architecture report.

## Read This When

- drafting a results discussion, conclusion, or abstract;
- writing methods text or a paper draft;
- writing figure or table captions and comparison tables for a report;
- producing anything under `reports/`.

Pair this file with the task workflow in
[../guides/write-results.md](../guides/write-results.md).

## Core Principle

Lead with the scientific claim and its physical meaning. Evidence (metrics,
maps, comparisons) supports the claim; it is not the claim. A reader should
learn what was found about the Earth system before learning how the model was
trained.

## Narrative Order

For any results section or discussion:

1. State the scientific question or hypothesis (for example: does adding a
   gravity-gradient channel improve seafloor reconstruction in a given region?).
2. State the finding in domain language: the phenomenon, the physical
   mechanism, the direction and magnitude of the effect, and where (spatially
   and temporally) it holds.
3. Give the supporting evidence (metric, map, profile, comparison) with the
   region, period, split, or track it applies to.
4. Interpret: the physics or data property that could explain the result, the
   uncertainty across seeds or folds, and the limitations (resolution, coverage,
   land contamination, reference data bias).
5. Point to reproducible evidence only as a reference (a methods paragraph, an
   appendix, or a footnote linking to the retained run).

Do not invert this into "we trained X, logged metrics, produced a figure".

## Engineering Term Isolation

Engineering terms belong in code, config, manifest, and commit messages. They
must not appear in scientific prose as if they were findings.

Avoid in prose (results, discussion, methods narrative, abstract):

- `retained run`, `run_id`, `manifest`, `artifact`, `artifact pipeline`;
- `promotion`, `promote`, `scratch`, `smoke` used as nouns describing results;
- `anti-bloat`;
- `checkpoint` as a result (acceptable in methods when it refers to a saved
  model state used for evaluation);
- `ablation` as a standalone result label (describe what was removed and why,
  e.g. "without the gravity-gradient input");
- `pipeline`, `framework`, `harness`, `orchestration`.

If a reader needs the engineering detail, link it from a methods paragraph or
appendix ("see Supplement; retained evidence under `outputs/...`") and keep the
main text in geophysical language.

## Anti AI Tone

Prose should read like a researcher explaining the work to a colleague, not like
a model performing competence. Two opposite failure modes both read as
machine-written and are not allowed: mechanical stiffness (the "does not speak
human" failure) and over-ornamentation (the flowery, empty-rhetoric failure).

### Write Like A Human

- Vary sentence length and structure. Do not turn prose into a disguised bullet
  list, and do not open every sentence with a transition adverb ("Furthermore",
  "Moreover", "Additionally", "Consequently") chained in sequence.
- Use real causal connectives ("because", "since", "although", "so") only where
  the logic is causal, not as decoration.
- State the reason directly. "Reconstruction error fell because the gravity
  input resolves short wavelengths" beats "the gravity channel exhibited
  substantial improvement, underscoring its pivotal role".
- Do not fake balance: drop "however" or "on the other hand" when there is no
  real tension, and do not pad a point into a rule-of-three to sound thorough.
- Prefer one concrete sentence over a vague one padded to look comprehensive.

### Over-Ornamentation

Empty flourish inflates without informing. Do not use:

- delve, leverage, harness, unlock, unveil, navigate, illuminate, demystify;
- tapestry, realm, landscape, paradigm, synergy, beacon, testament, frontier;
- myriad, plethora, "a host of", "a wealth of";
- "it is worth noting", "it should be noted", "it is important to note";
- "plays a crucial/pivotal/vital role", "stands as", "at the forefront of";
- "in today's world", "in an increasingly X world", "the ever-evolving X".

Each is a signal that a sentence is performing competence instead of stating a
fact. Replace with the concrete observation.

For Chinese prose, also drop translation-style padding and official-document
cliches. Avoid phrases that translate to "in the background of", "deeply
explore", "empower" or "assist", "a tapestry of", "manifests" or "highlights",
"committed to", "continuously optimize", and "comprehensively elevate", and
avoid forced three-part parallelism used only to sound thorough. Write plain,
factual Chinese.

### Empty Adjectives And Hollow Comparisons

- robust, scalable, modular, flexible, comprehensive, seamless, cutting-edge,
  next-generation;
- state-of-the-art or significant unless a specific comparison or statistical
  test is in the same section;
- "we implemented X module", "we built a pipeline" stated as a finding.

If a word can be deleted without losing information, delete it. Replace each
empty adjective with the concrete statement: what was predicted, over what
region and data, with what uncertainty, compared to what baseline.

## Sentence Leads

Open sentences with the scientific content, not the engineering action.

Bad:

> We ran a retained evaluation and `metrics.json` shows RMSE decreased.

Good:

> Reconstruction error over the test tracks fell to X km, with the largest
> gains on steep slopes where gravity gradients carry the most information; the
> supporting run is logged under the project's run directory.

## Numbers And Uncertainty

- Report the region, period, split, or track a number applies to.
- Report uncertainty (spread across seeds, folds, or independent tracks) when a
  claim depends on it; a single run is not a distribution.
- Keep units, coordinate conventions, and reference frame explicit.
- Distinguish a smoke check from a reported result. A smoke check is never
  evidence for a claim.

## Figures And Tables

- Captions are self-contained: they state the conclusion the figure supports,
  the region and data, and read independently of the body text.
- A caption must not be a file path or a variable name.
- Maps and profiles carry explicit colorbars, units, CRS, and coastlines or
  reference features when relevant.
- Comparison tables must explain why each comparison is scientifically
  meaningful (which mechanism or input it isolates), not only list metrics.
- Axis labels, legends, and units are explicit. No `y`, `pred`, `ssh`, or
  `output` as a final label.

## Reports Directory

`reports/` holds curated, human-facing material only: a figure, a table, a
short write-up. It must not contain raw logs, full metric dumps, or scratch
output. Every curated item points back to the retained run or data product that
produced it.

## Bilingual Policy

- Code, identifiers, docstrings, comments, filenames, manifests, and commit
  messages stay in English.
- The language of prose (reports, discussions, paper drafts) is a per-project
  choice. Declare it once in the project spec and stay consistent.
- When the prose language is not English (for example Chinese), write native
  prose directly; do not translate English sentence by sentence. Keep physical
  quantities in their standard symbols and units and avoid translation-style
  phrasing.

## Self-Check Before Submitting Prose

- [ ] The section opens with the scientific question or finding, not a run
      description.
- [ ] No engineering terms (`retained run`, `manifest`, `artifact`,
      `promotion`, `run_id`, `scratch`/`smoke`) appear as if they were results.
- [ ] No over-ornamentation (`delve`, `unveil`, `leverage`, `tapestry`,
      `navigate`, `myriad`, "it is worth noting", or the Chinese cliches above) remains.
- [ ] No empty adjectives (`robust`, `scalable`, `seamless`,
      `state-of-the-art` without comparison) remain.
- [ ] No mechanical transition-adverb chains or prose-as-bullet-list; sentence
      structure varies and connectives are causal, not filler.
- [ ] Every number carries its region, split, or track, plus uncertainty where
      it matters.
- [ ] Captions are self-contained, science-oriented, and carry units and CRS.
- [ ] Comparison tables justify why each comparison matters.
- [ ] `reports/` contains only curated material that links back to evidence.
- [ ] Smoke checks are labeled as smoke, not as results.
