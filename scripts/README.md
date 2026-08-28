# Scripts

`validate.py` checks the local marketplace structure:

- `marketplace/index.json` has the fields Trellis expects;
- spec paths exist and ship `README.md`; workflow paths are Markdown files
  inside the marketplace root;
- the research workflow declares its Trellis 0.6.16 audit marker, requires an
  explicit Codex inline setting, matches its authoritative source, has balanced
  state blocks, and retains its stop rules;
- workflow install examples use a release tag or the unreleased placeholder,
  and the deprecated migration script rejects common write commands and file
  redirections;
- markdown links inside the spec resolve and stay inside the repo;
- core research requirements are still present, including the scientific-writing
  layer (`shared/scientific-writing.md`, `guides/write-results.md`);
- paths are ASCII everywhere, and file content is ASCII for the portable spec
  under `marketplace/`; the exact workflow mirror keeps Trellis punctuation;
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
