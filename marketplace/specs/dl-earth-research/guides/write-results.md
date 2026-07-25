<!--
Maintainer note: the sibling template carries an equivalent copy of this file
with domain examples adapted (research-core is generic; dl-earth-research is
geoscience). Mirror structural changes -- section headings, self-check items,
cross-reference targets -- across both copies unless a change is genuinely
domain-specific. The duplication is structural: Trellis installs each template
directory as a standalone flat copy into .trellis/spec/, so the two cannot share
a single source file.
-->

# Guide: Write A Results Discussion

Use this when drafting a results discussion, conclusion, paper section, or any
curated write-up under `reports/`.

Read [../shared/scientific-writing.md](../shared/scientific-writing.md) first.
That file holds the rules; this guide is the workflow.

## Steps

1. Write the scientific question in one sentence before any numbers (for
   example: does a gravity-gradient input improve seafloor reconstruction in a
   given region, and where does it help or hurt?).
2. List the retained evidence that can answer it (run directory, checkpoint, or
   data product). If none exists, stop and produce it first; do not draft a
   claim ahead of evidence.
3. Draft the finding in domain language: the effect, its direction, magnitude,
   and the region, period, split, or track it applies to.
4. Add the interpretation: the physics or data property that could explain the
   result, uncertainty across seeds or independent tracks, and the limitations
   (resolution, coverage, land contamination, reference data bias).
5. Place every number with its region and uncertainty.
6. Move engineering detail (command, config path, checkpoint path, run id) to a
   methods paragraph, footnote, or appendix; link to the retained run.
7. Run the self-check in [../shared/scientific-writing.md](../shared/scientific-writing.md).

## Do

```text
reports/bathymetry_gravity_summary.md   # curated discussion + figures
outputs/<run_id>/manifest.json          # evidence the discussion links to
outputs/<run_id>/checkpoints/...        # saved model referenced by methods
```

A reader of the report should understand the finding without opening the run
directory; a reviewer who wants to verify can follow the link to the retained
run and checkpoint.

## Do Not

```text
reports/raw_metrics_dump.md
reports/run_log.md
discussion that opens with "we ran a retained evaluation and metrics.json shows"
```

## Smoke Vs Result

If only a smoke check ran, write "smoke check passed; no result is claimed",
not a discussion. Promote the run to retained before any claim, following
[../shared/reproducibility.md](../shared/reproducibility.md).

## Completion Checklist

- [ ] The write-up opens with the scientific question or finding.
- [ ] Every claim links to retained evidence.
- [ ] Engineering terms live in methods, footnotes, or appendix, not in the
      narrative.
- [ ] The self-check in `scientific-writing.md` passes.
