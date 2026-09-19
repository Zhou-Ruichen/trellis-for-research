# Scripts

`validate.py` checks the local marketplace structure:

- `marketplace/index.json` has the fields Trellis expects;
- template paths exist and each ships a `README.md`;
- markdown links inside the spec resolve and stay inside the repo;
- the six workflow-state blocks retain the interface Trellis expects;
- paths are ASCII everywhere, and file content is ASCII for the portable spec
  under `marketplace/`;
- content under `examples/` may include bilingual writing samples (for example a
  Chinese result discussion), so the ASCII-content check skips that subtree while
  still requiring ASCII paths;
- the files both templates share (`data/index.md`, `evaluation/index.md`,
  `guides/add-run.md`, `guides/write-results.md`, and every `shared/` file
  except `index.md` and `python-style.md`) stay byte-identical;
- when Trellis is installed, the template can be copied into `.trellis/spec/`
  after `trellis init` and every expected file is present.

Run:

```sh
python3 scripts/validate.py
```

The script checks structure, not scientific correctness or exact prose. It does
not perform a remote `gh:` registry download. Use it when checking template
changes; it is not part of an experiment's execution path.
