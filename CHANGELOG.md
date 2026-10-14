# Changelog

Notable changes to this Trellis spec-template repository. Format based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/) as git tags. Pin a version with
`trellis init --registry gh:Zhou-Ruichen/trellis-for-research/marketplace#<tag>`.

## v0.6.11 - 2026-10-15

### Changed
- `workflows/research.md`: the `in_progress` blocks and step 2.1 match the
  action to the current request instead of requiring a calculation run on
  every turn. A discussion or assessment gets a judgment from the evidence
  at hand, a design request compares the candidate schemes and gives a
  preferred option, a question about a log or an earlier result is answered
  from the existing record, and a calculation runs when the request
  authorizes it. The `no_task` block covers discussion and explanation
  beside short calculations. The Phase Index, the `#### X.Y` steps, the six
  workflow-state blocks, and the identical `-inline` blocks keep their form,
  and the `task.py` commands and record paths are unchanged.
- `shared/research-minimal.md` (both templates): a bounded assessment ends
  with the result that answers its question, and that result may be
  negative. In continuing research, a comparison answers the current
  unknown first; a repeat or an added condition is chosen by what it
  contributes to the interpretation, and the continuation plan follows the
  current assignment, the evidence that holds, and the available resources.
  Counterevidence updates only the level it actually refutes (an
  assumption, a configuration, a mechanism, or the research topic), the
  refuted configuration or claim is no longer used, and the evidence that
  remains selects the next comparison that distinguishes the explanations
  at issue. An exploratory task records what was observed, compared, and
  interpreted; thresholds and automatic continue-or-stop rules stay with a
  confirmatory design the user has asked for.
- `evaluation/index.md` (both templates): the recorded numbers describe the
  difference observed in the comparison, and a claim about stability or
  general superiority rests on the repeated-run evidence that shows it;
  this replaces the rule that one run per condition leaves conditions
  unranked, which mixed the observed difference with cross-run stability.
  The scale of repetition follows the question and the available resources.
  Run counts, units, and variation are stated as the records contain them,
  and what the records do not contain stays unknown. A comparison design
  gives each new case one named change from its reference condition; with
  several factors in play it names each factor's levels and the
  combinations actually run, keeping existing runs and proposed new cases
  distinct. A near-equal result is interpreted together with the variation
  and the comparison's resolving power, at the level of explanation the
  design isolates.
- `shared/scientific-writing.md` (both templates): the details in a short
  reply are selected by the reader's current question. Material supplied in
  the request or read from a record is stated as given, with its source
  named; it claims checked only after an actual comparison with a
  reference, an expected value, or the source. An untested step or an
  unknown is stated when it affects the current judgment, the use of the
  result, or the next step, and the status sits beside the claim it
  affects; a reply answered from the given material ends with that answer
  instead of a closing line about what was not checked. A condition
  necessary to a conclusion is written with that conclusion. Scientific
  concepts keep the field's terms while ordinary software constructs and
  existing file names such as `prd.md` and `result.md` keep their names.
  The paired examples gain a given-log row.
- `scripts/README.md`: the ASCII description now matches `validate.py`,
  which exempts `examples/`, `README.zh-CN.md`, and the bilingual
  `shared/scientific-writing.md` files from the content check while keeping
  every path ASCII.
- `README.md` and `README.zh-CN.md` pin `v0.6.11`.

## v0.6.10 - 2026-10-13

### Changed
- `shared/scientific-writing.md` holds every reply in the working session,
  including progress updates, debugging and log reviews, run reports, and
  one-line answers, to a manuscript's standard of evidence and wording.
  Every sentence carries a fact, a value, an action, or a conclusion, and a
  sentence that carries none is deleted. A reply opens with the answer, the
  result, or the current state, including a failure or an unknown, and ends
  once the answer and its evidence are given.
- New "Evidence status" section: the verb of a claim states its evidence as
  executed (command completed, file written), checked (output compared with
  a reference, an expected value, or the source), or inferred (judged from a
  log, a code reading, or partial output, with that basis named). Untested,
  unknown, and failed steps are written as such. Writing an executed step as
  checked, or an inference as a fact, is fabricated evidence, and removing a
  hedge adds no run, check, or result.
- New "Objections and hedges" section: a sentence that refutes a claim no
  user, reviewer, cited work, or earlier result put forward is deleted, and
  so is a hedge whose removal changes neither the reading of a fact nor the
  next step. Sentences built on the listed Chinese and English negation and
  hedge constructions (does not prove, does not mean, does not imply, cannot
  yet, is not enough to show, not X but Y, and the other listed forms) are
  deleted or rewritten as what was measured, run, checked, or left untested.
  A correction opens with the differing facts side by side.
- New "Limitations and risks" section: the limitation rule moves here from
  "Results and interpretation". The data scope goes inside the claim it
  limits, a claim wider than its evidence is narrowed in that sentence, and
  a risk tied to an operation is written before that operation.
- New "Paired examples" section: eight original and rewritten sentences on
  executed and checked claims, an inference, an unraised objection, a
  correction, scope inside the claim, and hedges on favorable results.
- `README.md` and `README.zh-CN.md` pin `v0.6.10`.

## v0.6.9 - 2026-10-11

### Fixed
- `workflows/research.md` again has the `## Phase Index` section and
  `#### X.Y` steps that Trellis 0.7 reads; since v0.6.1 session start loaded
  no research guidance and `get_context.py --mode phase` failed. The working
  order is now steps 1.1, 2.1, 2.2, and 3.1 inside the Phase Index.
- `planning-inline` and `in_progress-inline`, which Codex reads under
  `codex.dispatch_mode: inline`, repeat `planning` and `in_progress`; since
  v0.6.1 they kept a planning task's question out of `prd.md`.
- The task commands run under Trellis 0.7.0-beta.4: `task.py create` takes
  `--description`, and `task.py start` takes `--allow-empty-context`.

### Changed
- The workflow overrides the native task-creation question, review gates,
  and default sub-agent dispatch; the `no_task` block starts short
  calculations without a task.
- New projects save the research workflow as a variant with
  `default_workflow: research` and `codex.dispatch_mode: inline`, as
  existing projects do; `trellis init --workflow research` made every
  `trellis update` flag `.trellis/workflow.md` and left Codex dispatching to
  sub-agents. Such a project restores the native file with
  `trellis workflow --template native --force` after saving the variant.
- Project facts and rules go in a project-owned spec layer such as
  `.trellis/spec/project/index.md`; unedited template files update without
  merge conflicts.
- `shared/scientific-writing.md`: sentences connect through their content
  and order; differing facts stand side by side, each with its value, and a
  verb states a relation. Contrast words, connectives, and emphasis-only
  modifiers in English and Chinese are dropped, and the clauses that kept
  inference connectives and informative modifiers are removed.
  `research-minimal.md`, `evaluation/index.md`, and
  `guides/debug-nan-oom.md` state their rules without contrast clauses.
- The rule that research projects need no defensive code or tests removes
  tests, test suites, and test directories from the specs and README
  defaults. The input checks in the data and evaluation guidelines stay.
- `task.py finish` ends a task and keeps its record at the cited path;
  `task.py archive` and `/trellis:finish-work` move it under
  `.trellis/tasks/archive/`. The README no longer suggests
  `/trellis:continue`.
- `scripts/validate.py` checks the Phase Index, step headings, matching
  inline blocks, and the release pins in both READMEs. The install-shape
  check and the CI Trellis install are removed.

### Removed
- `examples/minimal-run/.gitignore`, left from the packaged example removed
  in v0.6.0.

## v0.6.8 - 2026-10-10

### Changed
- `evaluation/index.md` (both templates): when conditions share data or
  folds, report the paired per-fold differences; a single run per condition
  supports a description, not a ranking.
- `shared/reproducibility.md`: install dependencies only into a recorded
  environment.

## v0.6.7 - 2026-10-10

### Fixed
- `guides/debug-nan-oom.md`: v0.6.6 weakened two rules while removing
  disclaimer phrasing. Restored their meaning in direct form: `nan_to_num`
  or loss skipping enters the code only where the data policy requires it
  and the run record states it is active; a rerun after OOM is a recorded
  decision, and the comparison's training settings stay as they were. The
  v0.6.6 note that substantive prohibitions were unchanged was wrong for
  this file.

## v0.6.6 - 2026-10-10

### Changed
- Removed disclaimer-style phrasing across the specs, `workflows/research.md`,
  and README Research Defaults: trigger conditions read as "when X" instead
  of "only when X", permission sentences ("is optional", "can stay") read as
  direct instructions, and negative boilerplate arms ("instead of ...",
  "rather than ...") were dropped where the positive instruction carries the
  rule. Substantive prohibitions (terminology bans, silent NaN skipping,
  invented evidence) are unchanged.
- `shared/scientific-writing.md`: the narrative names data, method, and
  settings; the repository address with its version and the data product
  versions go in the availability statement, and run identifiers stay in the
  result record. The terminology rule is split into short sentences with
  the geodesy illustrations last.
- `shared/research-minimal.md`: the exploratory-task rule is its own bullet
  and states where thresholds and continue-or-stop rules belong.
- `README.zh-CN.md` Research Defaults and version pins aligned with
  `README.md`.

## v0.6.5 - 2026-10-10

### Changed
- Dropped the engineering metaphors "defensive layer" and "outcome gate"
  from the exploratory-task rule in `shared/research-minimal.md`; the rule
  now states what to report and what not to add directly.
- `shared/scientific-writing.md`: emphasis-only modifiers (deep, in-depth,
  strict as bare intensifiers) are dropped; a modifier stays when it adds
  information or has an established technical meaning (strictly increasing,
  statistically significant).

## v0.6.4 - 2026-10-10

### Changed
- Internal codenames fall under the same ban as coined terms and engineering
  borrowings in `shared/scientific-writing.md`; a new identifier, comment,
  docstring, log line, file name, or figure label in code and configuration
  takes the field's term or its standard abbreviation.
- Results prose spends its words on the analysis and a plain statement of
  what was observed; a limitation is stated once, beside the claim it affects
  and in proportion to its effect, without piling scope qualifiers onto a
  favorable result or hedging against objections nobody raised.
- `shared/research-minimal.md`: an exploratory task adds no outcome gate
  (pass/fail, eligible, interesting_signal) and no automatic continue or
  stop rule.

## v0.6.3 - 2026-10-10

### Changed
- Added "boundary" to the banned borrowings in `shared/scientific-writing.md`;
  say where the data are read instead.
- Renamed the `data/index.md` heading "Data boundary" to "Checks when data
  are read".

## v0.6.2 - 2026-10-10

### Changed
- Extended `shared/scientific-writing.md` to replies in the working session,
  not only manuscripts and reports. A routine update may stay brief but uses
  the manuscript's vocabulary.
- Banned borrowed engineering or software words, workflow labels, and coined
  terms for any scientific concept, procedure, comparison, or result, with
  Chinese geodesy illustrations (regularization rather than damping,
  reference model rather than baseline, checking rather than acceptance).
  The field's published literature decides the term; a project terminology
  file records those choices.

## v0.6.1 - 2026-09-23

### Changed
- Updated the documented Trellis target from `0.7.0-beta.3` to the
  non-breaking `0.7.0-beta.4` release. Its migration list is empty, so
  `trellis update` needs no `--migrate` option.
- Made the research workflow a direct exploratory path. Trellis state labels
  remain for context loading, but they do not describe approval steps or
  automatic sub-agent work.
- Reduced the default record to the number and the command, data, code, seed,
  and environment details needed to rerun it. Large outputs remain outside Git
  unless they are needed to interpret the number.
- Made repeats, extra comparisons, input checks, and uncertainty conditional
  on the question. A single run and a negative result remain valid observations.
- Removed workflow labels from the installed writing guidance and replaced
  them with the concrete data, method, settings, and number.

## v0.6.0 - 2026-09-20

### Changed
- Rewrote `shared/scientific-writing.md` around one main claim: comparisons
  serve the claim, planned comparisons are reported including losses, and
  no passages rebut objections that no reviewer or result raised.
- Kept workflow vocabulary (freeze, baseline, protocol, pipeline, manifest,
  retained or promoted run, dry run) and coined terms out of research prose
  unless attached to a named referent; required direct statements instead
  of chains of what a thing is not or claims routed through a second noun;
  placed each limitation next to the claim it weakens and cut disclaimers
  of claims nobody made; moved Git, CI, and hosting details and identifiers
  out of the narrative.
- Linked the writing rules from `shared/research-minimal.md` and workflow
  step 2.1.
- Replaced "baseline" and "protocol" in the reproducibility and data specs
  with "reference run", "reference method", "comparison", and "access URL".
- Added evaluation rules for selection versus reporting data and for
  differences measured against variation under one condition; a notebook is
  a record when it runs top to bottom from a fresh kernel.
- Gave each principle one home: variants-as-parameters and code review live
  in `anti-bloat.md`, storage in `project-layout.md`, evidence and
  "software success is not evidence" in `reproducibility.md`, comparison
  rules in `evaluation/index.md`. Removed `guides/code-review.md`; merged
  `guides/add-experiment.md` into `guides/add-run.md`.
- Made `data/index.md`, `evaluation/index.md`, and `shared/reproducibility.md`
  identical across the two templates; deep-learning specifics (selection
  data, RNG schedule, checkpoints, augmentation) moved to
  `training/index.md`. Nine files are now shared and checked byte-identical
  by the validator; `index.md` files stay short as Trellis layer catalogues.
- Added concise task-resume and decomposition rules using existing records.
- Linked Python style and training guidance from the deep-learning reference
  index; clarified delegated edit scope, outputs, completion criteria, shared
  compute coordination, and the main agent's integration responsibility.
- Replaced the packaged regression example with one standard-library analysis
  script and its result; removed run tiers, manifests, config inheritance,
  environment snapshots, and example-only packaging. The example now fits
  the same synthetic observations with ordinary least squares instead of
  gradient descent. Layout guidance no longer ships placeholder files.
- Centralized execution, checking, authorization, and evidence rules in
  `shared/research-minimal.md`; domain guides now add only domain guidance
  and link to the common rules instead of restating procedures.
- Focused checks the work needs are part of the work. Removed the blanket
  requirement that software tests, lint, builds, and type checks wait for an
  explicit request; test suites, check agents, new test infrastructure, and
  repeated successful checks are still not added by default.
- Removed the universal sealed-evaluation and freeze-confirmation ceremony.
  Data isolation, specifically declared held-out-data restrictions, and
  user-reserved decisions remain in force; completing a task does not
  itself declare exploration finished.
- Unified the duplicated shared specs across the two templates around
  shared domain-neutral wording; both templates stay self-contained.
- Shortened the workflow, spec files, and READMEs while keeping the six
  Trellis 0.7 workflow-state blocks, numbered phase and step entries, task
  CLI, marketplace ids, template paths, and published release pins
  unchanged.

## v0.5.0 - 2026-09-05

### Changed
- Made exploratory scripts the default without package, config, test-suite,
  mode, or run-tier requirements.
- Replaced mandatory manifests and schemas with the scientific information
  needed to interpret retained evidence, reusing existing records and locations.
- Limited data checks to assumptions that could silently change the result;
  ordinary file and library errors propagate without generic preflight code.
- Made spec loading question-driven and compressed the research workflow while
  preserving the Trellis state blocks and numbered context entries.
- Removed repeated checklists and general writing machinery from task guides;
  retained evidence-based scientific writing and optional independent agents.
- Removed validator assertions tied to exact spec wording. Structural checks
  remain available when explicitly requested.
- Kept native Trellis files upstream-managed and selected the research workflow
  as a separate variant. Documented direct Codex dispatch through native config.
- Limited discussion of research limitations to their effect on the claim,
  without repeated minor caveats or hypothetical concerns.

## v0.4.3 - 2026-09-02

### Changed
- Moved the "metric values are observations, not pass/fail criteria" principle
  into the exploratory stop condition in `shared/research-minimal.md`: a
  negative or null result is recorded as evidence and answered with the next
  run the task plan registered, not with a stop or a route-level conclusion.
- Stated that completing a task or a full set of runs does not end
  exploration: opening a sealed evaluation (final test period, held-out data)
  or freezing the explored configuration closes the exploratory phase and
  requires the task's registered decision to be answered and user
  confirmation. The workflow's completed state points to this rule.
- Required sub-agent handoffs in the research workflow to carry the task's
  prd.md decision and the research-minimal constraints; sub-agent output is
  reviewed against that task record.
- Noted in the README that stock Trellis bootstrap task scaffolding (for
  example `.trellis/tasks/00-bootstrap-guidelines/`) is not part of this
  template and can be deleted after adoption.

## v0.4.2 - 2026-09-01

### Changed
- Limited the deep-learning test examples to durable modules; exploratory code
  adds a test only for a named concrete failure.
- Unified code replacement guidance: check the replacement before removing the
  superseded tracked implementation.
- Made the research workflow usable with other installed specs by treating
  `shared/research-minimal.md` as optional.

## v0.4.1 - 2026-09-01

### Changed
- Shortened the research workflow while retaining the six Trellis 0.7 state
  blocks and direct path for ordinary work.
- Replaced the single successful-run wording with the comparisons, seeds,
  folds, and repeats required by the scientific design; identical successful
  commands are not repeated only for reassurance.
- Reduced repository-maintenance guidance to reuse, parameterized variants,
  extraction after real durable duplication, and removal of code replaced by
  the current task. Research evidence and unrelated files remain outside that
  cleanup scope.
- Clarified that `v1` and `v2` are valid for datasets, schemas, interfaces,
  releases, and protocols that intentionally coexist; only purposeless source
  copies are rejected.
- Let retained runs point to an existing lockfile, container, or environment
  record. Per-run freezes are used only when no stable record exists or the run
  depends on drifting environment state.
- Removed repeated pre-development, completion, and code-review checklists that
  restated the workflow.

## v0.4.0 - 2026-09-01

### Changed
- Renamed the spec template ids and directories to the shared
  `research-<scope>[-<method>]` form: `research-computational` and
  `research-deep-learning`. The deep-learning spec now applies across research
  domains; geospatial rules are conditional on the data. Older tags retain the
  former ids.
- Reduced the research workflow to a small task record around the question,
  work, focused check, and result. Small and single-session work now proceeds
  without a Trellis task; commits, journals, archives, and sub-agents are used
  only when they help the research.
- Published the research workflow as a Trellis 0.7 marketplace workflow while
  keeping the six 0.7 workflow-state blocks and stock task commands.
- Added separate focused-check paths for exploratory experiments, maintained
  code, scientific prose, and documentation or configuration work.
- Preserved one-time validation of external data fields that can change a
  scientific result while rejecting repeated defensive checks and unnecessary
  checksum machinery.
- Extended plain-language guidance to README files, documentation, and task
  results; separated supported findings from candidate mechanisms and retained
  exact technical detail in Methods.
- Removed the shell overlay installer and its duplicate implement/check files;
  Trellis now installs and updates the workflow through its native marketplace
  commands. CI is pinned to `0.7.0-beta.3`, and validation checks the workflow
  entry and exact workflow-state parsing.

## v0.3.10 - 2026-08-18

The repository name and template labels now describe both the spec marketplace
and the research workflow overlay. Installed research rules and workflow
behavior are unchanged.

### Changed
- Renamed the repository source from `trellis-research-spec` to
  `trellis-for-research` and updated registry examples, validation text, and
  example descriptions.
- Renamed the template labels to General Computational Research and Geoscience
  Deep Learning while retaining the stable CLI ids `research-core` and
  `dl-earth-research`.
- Updated the root README introduction and repository layout to include the
  workflow overlay, implement agent, and research-check skill.

## v0.3.9 - 2026-08-17

Maintainer-only text is removed from installed research workflows without
changing workflow states, routing, research rules, or checks.

### Changed
- Replaced the 44-line workflow-state maintainer comment with a short pointer
  that retains the required-step invariant.
- Moved the generic workflow customization and lifecycle-hook notes from the
  installed `workflow.md` into the overlay README in condensed form.
- Kept all `[workflow-state:*]` block bodies unchanged.

## v0.3.8 - 2026-08-17

Research protocol changes and claim review are now explicit without adding a
skill, hook, agent, state, ledger, or task file.

### Changed
- Once a retained run or comparison starts, changes to its question or
  hypothesis, method, data, split, preprocessing, metric, baseline, or claim
  scope require a new run or comparison record. Earlier artifacts remain
  unchanged and the reason for the change is recorded.
- A changed research question starts a new Trellis task. Scratch work remains
  free to iterate and records its final protocol only if promoted.
- `result.md` records limitations or uncertainties that change the
  interpretation. Completing a task does not approve a manuscript or external
  scientific claim; that still requires researcher review of retained evidence,
  scope, uncertainty, and limitations.
- The jsonl guidance no longer describes `implement.md` as mandatory merely
  because a task is complex.

## v0.3.7 - 2026-08-17

Fewer planning files and repeated check lists for exploratory tasks, based on
observed Trellis usage in a long-running research repository. No new skill,
hook, agent, or task status.

### Changed
- Exploratory tasks are PRD-only by default, including multi-step experiments.
  `design.md` and `implement.md` are created only for explicit interface,
  dependency, coordination, migration, or rollback needs.
- Optional planning files no longer copy acceptance criteria or validation
  commands from `prd.md`. Phase 2.2 owns checks, and `result.md` records the
  actual invocation, observation, findings, and output paths once.
- `implement.jsonl` and `check.jsonl` list only files needed during
  implementation or checking. Seed-only manifests are valid when no additional
  spec or research context exists; exploratory manifests avoid broad indexes.
- Later journal entries summarize the finding, commit, and `result.md` path
  instead of reproducing the check list.

## v0.3.6 - 2026-08-17

One-invocation ownership and complete overlay verification. No new skill,
agent, hook, or workflow mode.

### Changed
- Phase 2.1 prepares code and configuration without executing the experiment.
  Phase 2.2 owns the single result-producing invocation and applies its sanity
  check to that same invocation.
- `trellis-research-check` now states explicitly that its one execution both
  produces the requested observation and supplies the outputs being checked.
- Task `research/` directories are limited to Markdown investigation notes and
  small metadata. Experiment artifacts stay under project `outputs/`, with
  task results recording paths instead of copies.
- The research-workflow README now matches the Phase 2.1 behavior.

### Fixed
- `apply.sh --verify` compares all four overlay-owned installed files with
  their masters instead of checking an implement-agent phrase and skill-file
  existence. Normal apply runs the same complete verification before reporting
  success.
- Includes the post-v0.3.5 implement-agent verification fix without moving the
  existing v0.3.5 tag.

## v0.3.5 - 2026-08-17

Single-owner validation and breadcrumb compression. Final static-rule
release; further changes only from real failure cases.

### Changed
- Phase 2.1 and the implement agent no longer self-check: dispatch
  descriptions say "Do not run the workflow quality check; Phase 2.2 owns
  validation", and the agent report drops the check section. The experiment
  runs exactly once, in the check step.
- The `in_progress` and `in_progress-inline` breadcrumbs are compressed to
  five lines (Trellis recommends roughly 200 bytes per per-turn block).
  Sub-agent dispatch rules, the skill-only statement's detail, and context
  order moved into the Phase 2 body where they are read once, not every
  turn.
- Core Principle 3 softened from "Persist everything" to "Persist what must
  survive the session; evidence depth follows the run tier".
- research-workflow README: the skill is always installed to both the
  Claude and Codex skill locations (matches the script).

### Fixed
- `apply.sh` rejects unknown modes instead of silently behaving like
  dry-run.

## v0.3.4 - 2026-08-17

Fixes for Codex/GPT-5.6 compatibility and two axis-wording regressions.
No new rules.

### Fixed
- `trellis-research-check` is a skill only; workflow no longer claims a
  sub-agent form for it, and Phase 2.2 loads the skill in the main session.
- `apply.sh` installs the skill for Codex too (`.agents/skills/`, the
  shared layer Trellis uses for Codex skills), alongside
  `.claude/skills/`, whenever the project has the platform directory;
  `--verify` checks both.
- Two reversed axis statements corrected to "verification depth follows the
  task mode; evidence recording follows the run tier" (Core Principle 6 and
  the research-workflow README).
- The durable flow in both `in_progress` breadcrumbs now updates spec only
  if durable knowledge exists (Phase 3.3) instead of unconditionally.
- Phase 3.4 no longer re-asks the spec-update question Phase 3.3 already
  answered.
- The validator now anchors the axis wording and the skill-only statement in
  `research-workflow/` so these cannot silently regress.

## v0.3.3 - 2026-08-17

Concept and wording fixes from review; no new mechanisms.

### Changed
- Mode and evidence tier are separated: mode (exploratory / durable)
  controls how code is written and checked; the run tier (scratch / smoke /
  retained) controls what the run records. A retained result no longer
  implies durable code; `prd.md` declares only the mode. Durable is defined
  as code the project keeps and maintains.
- `shared/research-minimal.md`: the check rule now reads "name the concrete,
  plausible failure, use the cheapest check that answers it, do not re-check
  an answered question" (the earlier wording could reject cheap sanity
  checks); "answer two questions" softened to "be able to name" to avoid
  ritual output.
- Exploratory flow no longer loads `trellis-update-spec` by default; Phase
  3.3 first decides whether durable knowledge exists and records "no durable
  knowledge" without loading the skill. Exploratory results go to
  `<task>/result.md`; retained evidence goes to the run manifest.
- `trellis-research-check`: provenance identifiers are required only for
  retained runs; scratch checks confirm the result came from the invocation
  just executed and never create provenance machinery.
- "closing pass" renamed to "final check" throughout the overlay.

### Removed
- The `apply.sh` patch of the official `trellis-check` skill description.
  Routing lives entirely in `workflow.md` and the research-check skill.

### Added
- `scripts/validate.py`: README install pins must match the latest CHANGELOG
  release; `shared/research-minimal.md` added to expected spec shape with
  required-content checks.

## v0.3.2 - 2026-08-17

Research workflow overlay and minimal-code rules. Verification depth now
follows the task mode (exploratory by default, durable on request) instead
of a single software-engineering standard.

### Added
- `research-workflow/` overlay: master `workflow.md` (two-mode flows in the
  `in_progress` breadcrumbs with an explicit stop condition; Phase 2.2 split
  by mode; Phase 3.3 spec updates restricted to durable knowledge), master
  `agents/implement.md` (mode-aware closing pass), the
  `trellis-research-check` one-pass sanity skill, an idempotent `apply.sh`
  with `--dry-run` and `--verify`, and a README covering coexistence with
  `trellis update`.
- `shared/research-minimal.md` in both templates: highest-priority minimal
  code rules. Mode-conditional defaults (exploratory adds no defensive
  code, boundary checks, hash/checksum logic, exception handling, retries,
  unit tests, strict typing, or abstractions without a concrete likely
  failure), the utility test for any added check (what failure does it
  catch, what changes once found), and the stop condition.
- Certainty discipline in `shared/scientific-writing.md` (both templates):
  state findings at the strength the evidence supports, report uncertainty
  once, state limitations once.

### Changed
- `shared/index.md` (both templates) lists `research-minimal.md` first.
- Checksum rules in `data/index.md` were verified to already be limited to
  durable data products; no change needed.

## v0.3.1 - 2026-08-17

Exploration discipline and anti-bloat sharpening. Verification regimes built
for maintained software (TDD, coverage, metric gates) are kept out of
exploratory research code; the anti-bloat rules gain a reuse ladder and
explicit handling of one-off test code; the anti-AI-tone word lists are
synced with the global agent rules.

### Added
- Verification boundaries in both templates (`evaluation/index.md`): hard
  gates apply to code, never to scientific outcomes; no TDD, coverage
  targets, or metric-value assertions; a missed target is a finding to
  report, not a task failure; validation commands check executability and
  sanity only.
- Completion-gate rules in `guides/code-review.md` (both templates) and the
  run/experiment guides (`guides/add-run.md`, `guides/add-experiment.md`):
  no metric target is written as a completion gate.
- One-off test code rules in `shared/anti-bloat.md` (both templates):
  scratch tests are deleted once they answer their question; `tests/` holds
  only durable checks.

### Changed
- `shared/anti-bloat.md` (both templates) gains a reuse ladder before new
  code or new dependencies: this codebase, then an already-installed
  dependency (for research code, usually the scientific stack), then the
  standard library, then one line, then the minimum implementation.
- `shared/scientific-writing.md` (both templates) syncs its banned-phrase
  lists with the global agent rules: English additions (underscore(s),
  showcasing, intricate, "at its core", "when it comes to", load-bearing),
  a verbatim Chinese banned-phrase list, more empty adjectives, the
  "not just X, it's Y" rephrasing pattern, and an em-dash ban.
- `scripts/validate.py` exempts `scientific-writing.md` from the
  content-ASCII rule so the Chinese banned phrases appear verbatim.

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
