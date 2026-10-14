# Scripts

`validate.py` checks the local marketplace structure:

- `marketplace/index.json` has the fields Trellis expects;
- template paths exist and each ships a `README.md`;
- markdown links inside the spec resolve and stay inside the repo;
- `workflows/research.md` keeps the markers Trellis 0.7 reads: a
  `## Phase Index` section, `#### X.Y` step headings, and the six
  workflow-state blocks in interface order, each `-inline` block repeating
  its base block;
- paths are ASCII everywhere, and file content is ASCII except under
  `examples/` (bilingual writing samples such as a Chinese result
  discussion), in `README.zh-CN.md`, and in the two
  `shared/scientific-writing.md` files, whose prose examples are bilingual;
  the content check skips exactly those files and the path check still
  covers them;
- the files both templates share (`data/index.md`, `evaluation/index.md`,
  `guides/add-run.md`, `guides/write-results.md`, and every `shared/` file
  except `index.md` and `python-style.md`) stay byte-identical;
- the install commands in `README.md` and `README.zh-CN.md` pin the latest
  `CHANGELOG.md` release.

Run:

```sh
python3 scripts/validate.py
```

The script checks structure; scientific content and wording are outside its
checks. It does not run Trellis or download the `gh:` registry. Its workflow checks follow the
markers Trellis 0.7.0-beta.4 reads; when the targeted Trellis version changes,
confirm in a project on that version that
`python3 ./.trellis/scripts/get_context.py --mode phase` prints the research
Phase Index. Use the script when checking template changes; it is not part of
an experiment's execution path.
