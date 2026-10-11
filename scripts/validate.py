#!/usr/bin/env python3
"""Validate the local Trellis marketplace structure."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / "marketplace"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def validate_index() -> None:
    index = json.loads((MARKETPLACE / "index.json").read_text(encoding="utf-8"))
    templates = index.get("templates")
    if not isinstance(templates, list) or not templates:
        fail("marketplace/index.json must contain a non-empty templates array")

    for template in templates:
        for key in ("id", "type", "name", "path"):
            if not isinstance(template.get(key), str):
                fail(f"template entry must include string {key!r}: {template}")
        if template["type"] == "spec":
            template_path = ROOT / template["path"]
            if not template_path.is_dir():
                fail(f"spec template path does not exist: {template['path']}")
            if not (template_path / "README.md").is_file():
                fail(f"spec template path lacks README.md: {template['path']}")
        elif template["type"] == "workflow":
            template_path = MARKETPLACE / template["path"]
            if not template_path.is_file() or template_path.suffix != ".md":
                fail(f"workflow template must be a Markdown file: {template['path']}")
        else:
            fail(f"unsupported template type {template['type']!r}")


LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+\.md)\)")


def validate_markdown_links() -> None:
    for md_path in (MARKETPLACE / "specs").rglob("*.md"):
        text = md_path.read_text(encoding="utf-8")
        for match in LINK_RE.finditer(text):
            target = match.group(1)
            if "://" in target or target.startswith("#"):
                continue
            resolved = (md_path.parent / target).resolve()
            try:
                resolved.relative_to(ROOT)
            except ValueError:
                fail(f"{md_path.relative_to(ROOT)} links outside repo: {target}")
            if not resolved.is_file():
                fail(f"{md_path.relative_to(ROOT)} has broken link: {target}")


def validate_workflow_markers() -> None:
    # Trellis 0.7 SessionStart and `get_context.py --mode phase` read the
    # Phase Index, `--step X.Y` reads step headings, and the per-turn hook
    # reads the state blocks; `trellis workflow --save` warns when any is absent.
    # Research text does not depend on Codex dispatch mode, so each -inline
    # block repeats its base block.
    workflow = (ROOT / "marketplace/workflows/research.md").read_text(encoding="utf-8")
    if not re.search(r"^## Phase Index$", workflow, re.M):
        fail("marketplace/workflows/research.md needs a '## Phase Index' section")
    if not re.search(r"^#### \d+\.\d+", workflow, re.M):
        fail("marketplace/workflows/research.md needs '#### X.Y' step headings")
    pattern = re.compile(
        r"^\[workflow-state:([A-Za-z0-9_-]+)\]\s*\n"
        r"(.*?)\n\s*\[/workflow-state:\1\]$",
        re.M | re.S,
    )
    expected = [
        "no_task",
        "planning",
        "planning-inline",
        "in_progress",
        "in_progress-inline",
        "completed",
    ]
    matches = list(pattern.finditer(workflow))
    markers = re.findall(r"^\[/?workflow-state:[^\]]+\]$", workflow, re.M)
    if [match.group(1) for match in matches] != expected or len(markers) != 2 * len(
        expected
    ):
        fail(
            "marketplace/workflows/research.md must contain the six Trellis 0.7 "
            "workflow states in interface order"
        )
    bodies = {match.group(1): match.group(2) for match in matches}
    for status in ("planning", "in_progress"):
        if bodies[f"{status}-inline"] != bodies[status]:
            fail(f"marketplace/workflows/research.md: {status}-inline must repeat {status}")


def iter_repo_files() -> list[Path]:
    result = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    )
    return [Path(line) for line in result.stdout.splitlines() if line]


def validate_no_non_ascii() -> None:
    for rel_path in iter_repo_files():
        path = ROOT / rel_path
        if not path.is_file():
            continue
        try:
            str(rel_path).encode("ascii")
        except UnicodeEncodeError:
            fail(f"path must be ASCII: {rel_path}")
        # Content under examples/ may include bilingual writing samples (for
        # example a Chinese result discussion). Only paths must stay ASCII there.
        # Scientific-writing guidance includes bilingual prose examples.
        if any(part == "examples" for part in rel_path.parts):
            continue
        if rel_path == Path("README.zh-CN.md"):
            continue
        if rel_path.name == "scientific-writing.md" and "marketplace" in rel_path.parts:
            continue
        data = path.read_bytes()
        try:
            data.decode("ascii")
        except UnicodeDecodeError:
            fail(f"file content must be ASCII: {rel_path}")


SHARED_FILES = [
    "data/index.md",
    "evaluation/index.md",
    "guides/add-run.md",
    "guides/write-results.md",
    "shared/anti-bloat.md",
    "shared/project-layout.md",
    "shared/reproducibility.md",
    "shared/research-minimal.md",
    "shared/scientific-writing.md",
]


def validate_shared_files_identical() -> None:
    first = ROOT / "marketplace/specs/research-computational"
    second = ROOT / "marketplace/specs/research-deep-learning"
    for rel_path in SHARED_FILES:
        if (first / rel_path).read_bytes() != (second / rel_path).read_bytes():
            fail(f"templates must keep {rel_path} identical")


def validate_readme_pins_latest_version() -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## (v\d+\.\d+\.\d+) - \d{4}-\d{2}-\d{2}", changelog, re.M)
    if not match:
        fail("CHANGELOG.md has no versioned release heading")
        return
    latest = match.group(1)
    for readme_name in ("README.md", "README.zh-CN.md"):
        readme = (ROOT / readme_name).read_text(encoding="utf-8")
        pins = re.findall(r"marketplace#(v\d+\.\d+\.\d+)", readme)
        if not pins:
            fail(f"{readme_name} pins no version; expected {latest}")
        for pin in set(pins):
            if pin != latest:
                fail(f"{readme_name} pins {pin}; latest CHANGELOG release is {latest}")


def main() -> None:
    validate_index()
    validate_markdown_links()
    validate_workflow_markers()
    validate_no_non_ascii()
    validate_shared_files_identical()
    validate_readme_pins_latest_version()
    print("trellis-for-research validation passed")


if __name__ == "__main__":
    main()
