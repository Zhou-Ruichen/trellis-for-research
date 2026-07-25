# Scripts

`validate.py` checks the local marketplace structure:

- `marketplace/index.json` has the fields Trellis expects;
- template paths exist and each ships a `README.md`;
- markdown links inside the spec resolve and stay inside the repo;
- core research requirements are still present, including the scientific-writing
  layer (`shared/scientific-writing.md`, `guides/write-results.md`);
- paths are ASCII everywhere, and file content is ASCII for the portable spec
  under `marketplace/`;
- content under `examples/` may include bilingual writing samples (for example a
  Chinese result discussion), so the ASCII-content check skips that subtree while
  still requiring ASCII paths;
- when Trellis is installed, the template can be copied into `.trellis/spec/`
  after `trellis init` and every expected file is present.

Run:

```sh
python3 scripts/validate.py
```

The script does not perform a remote `gh:` registry download. That requires the
repository to be published to GitHub first.
