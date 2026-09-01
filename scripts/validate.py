#!/usr/bin/env python3
"""Validate the local Trellis marketplace structure."""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / "marketplace"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def load_index() -> dict:
    index_path = MARKETPLACE / "index.json"
    if not index_path.exists():
        fail("marketplace/index.json is missing")
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        fail(f"marketplace/index.json is invalid JSON: {exc}")


def validate_index() -> None:
    index = load_index()
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


def validate_required_content() -> None:
    required = {
        "marketplace/specs/research-computational/README.md": [
            "General Computational Research",
            "Template Fit",
            "research-deep-learning",
        ],
        "marketplace/specs/research-computational/shared/research-minimal.md": [
            "exploratory",
            "smallest change",
            "concrete, likely failure",
            "cheapest check",
            "Stop condition",
            "durable",
            "retained",
        ],
        "marketplace/specs/research-deep-learning/shared/research-minimal.md": [
            "exploratory",
            "smallest change",
            "concrete, likely failure",
            "cheapest check",
            "Stop condition",
            "durable",
            "retained",
        ],
        "marketplace/workflows/research.md": [
            "small research record",
            "## Phase Index",
            "Create a Trellis task only",
            "Validate external data once",
            "Sub-agents are optional",
            "Pure prose tasks do not create or run code",
            "Trellis does not add lint, type checking, tests, or full-suite",
            "Never reset, discard changes",
            "Finish without ceremony",
        ],
        "marketplace/specs/research-computational/shared/project-layout.md": [
            "data/raw/",
            "data/interim/",
            "data/processed/",
            "outputs/<run_id>/",
            "existing documented layout",
        ],
        "marketplace/specs/research-computational/shared/anti-bloat.md": [
            "Delete superseded code",
            "Repo-wide sweeps",
            "experiment record",
            "*_v2",
            "*_final",
        ],
        "marketplace/specs/research-computational/shared/reproducibility.md": [
            "manifest.json",
            "metrics.json",
            "Do not invent",
            "Scratch",
            "Retained",
            '"retention"',
            '"manager"',
            '"freeze"',
            "Once a retained run or comparison starts",
            "does not approve a scientific claim",
        ],
        "marketplace/specs/research-computational/data/index.md": [
            "Manifest Rule",
            "Boundary Validation",
            "leakage",
        ],
        "marketplace/specs/research-computational/evaluation/index.md": [
            "Retained evaluation runs",
            "Comparison",
            "reports",
        ],
        "marketplace/specs/research-deep-learning/shared/project-layout.md": [
            "data/raw/",
            "data/interim/",
            "data/processed/",
            "outputs/<run_id>/",
        ],
        "marketplace/specs/research-deep-learning/shared/anti-bloat.md": [
            "Delete superseded code",
            "Repo-wide sweeps",
            "experiment record",
            "*_v2.py",
            "*_final.py",
        ],
        "marketplace/specs/research-deep-learning/shared/reproducibility.md": [
            "manifest.json",
            "metrics.json",
            "Do not invent",
            "Scratch",
            "Retained",
            '"retention"',
            '"manager"',
            '"freeze"',
            "Once a retained run or comparison starts",
            "does not approve a scientific claim",
        ],
        "marketplace/specs/research-deep-learning/data/index.md": [
            "Format-Specific Rules",
            "Data Lake Rule",
            "Manifest Rule",
        ],
        "marketplace/specs/research-deep-learning/evaluation/index.md": [
            "Retained evaluation runs",
            "Scratch and smoke evaluation runs",
            "Retained prediction products",
        ],
        "marketplace/specs/research-deep-learning/training/index.md": [
            "PyTorch",
            "Lightning",
            "smoke",
        ],
        "marketplace/specs/research-computational/shared/scientific-writing.md": [
            "Engineering Term Isolation",
            "## Methods",
            "Anti AI Tone",
            "Write Like A Human",
            "Over-Ornamentation",
            "Bilingual Policy",
            "Self-Check Before Submitting Prose",
        ],
        "marketplace/specs/research-deep-learning/shared/scientific-writing.md": [
            "Engineering Term Isolation",
            "## Methods",
            "Anti AI Tone",
            "Write Like A Human",
            "Over-Ornamentation",
            "Bilingual Policy",
            "Self-Check Before Submitting Prose",
        ],
        "marketplace/specs/research-computational/guides/write-results.md": [
            "Write A Results Discussion",
            "scientific question",
            "Completion Checklist",
            "A completed Trellis task does not approve a scientific claim",
        ],
        "marketplace/specs/research-deep-learning/guides/write-results.md": [
            "Write A Results Discussion",
            "scientific question",
            "Completion Checklist",
            "A completed Trellis task does not approve a scientific claim",
        ],
    }
    for rel_path, needles in required.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"{rel_path} missing required text: {needle}")


def validate_workflow_states() -> None:
    workflow = (ROOT / "marketplace/workflows/research.md").read_text(encoding="utf-8")
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


def iter_repo_files() -> list[Path]:
    try:
        result = subprocess.run(
            ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except (subprocess.CalledProcessError, FileNotFoundError):
        return [
            path.relative_to(ROOT)
            for path in ROOT.rglob("*")
            if path.is_file() and ".git" not in path.parts
        ]
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
        # scientific-writing.md additionally carries the Chinese anti-AI-tone
        # word list; the banned phrases must appear verbatim to be matchable.
        if any(part == "examples" for part in rel_path.parts):
            continue
        if rel_path.name == "scientific-writing.md" and "marketplace" in rel_path.parts:
            continue
        data = path.read_bytes()
        try:
            data.decode("ascii")
        except UnicodeDecodeError:
            fail(f"file content must be ASCII: {rel_path}")


def validate_trellis_spec_shape() -> None:
    trellis = shutil.which("trellis")
    if trellis is None:
        print("WARN: trellis not found; skipped install-shape validation", file=sys.stderr)
        return

    expected_by_template = {
        "research-deep-learning": [
            "README.md",
            "shared/index.md",
            "shared/project-layout.md",
            "shared/anti-bloat.md",
            "shared/reproducibility.md",
            "shared/scientific-writing.md",
            "shared/research-minimal.md",
            "shared/python-style.md",
            "data/index.md",
            "training/index.md",
            "evaluation/index.md",
            "guides/index.md",
            "guides/add-experiment.md",
            "guides/write-results.md",
            "guides/debug-nan-oom.md",
            "guides/code-review.md",
        ],
        "research-computational": [
            "README.md",
            "shared/index.md",
            "shared/project-layout.md",
            "shared/anti-bloat.md",
            "shared/reproducibility.md",
            "shared/scientific-writing.md",
            "shared/research-minimal.md",
            "data/index.md",
            "evaluation/index.md",
            "guides/index.md",
            "guides/add-run.md",
            "guides/write-results.md",
            "guides/code-review.md",
        ],
    }

    with tempfile.TemporaryDirectory(prefix="trellis-for-research-") as tmp:
        tmp_path = Path(tmp)
        subprocess.run(
            ["git", "init"],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        subprocess.run(
            [trellis, "init", "--claude", "--codex", "-y"],
            cwd=tmp_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        for template in load_index()["templates"]:
            if template["type"] != "spec":
                continue
            template_id = template["id"]
            if template_id not in expected_by_template:
                fail(f"missing spec-shape expectations for template {template_id!r}")
            template_path = ROOT / template["path"]
            spec_path = tmp_path / ".trellis/spec"
            if spec_path.exists():
                shutil.rmtree(spec_path)
            shutil.copytree(template_path, spec_path)

            for rel_path in expected_by_template[template_id]:
                if not (spec_path / rel_path).is_file():
                    fail(
                        f"Trellis spec-shape validation missing "
                        f"{template_id}/.trellis/spec/{rel_path}"
                    )


def validate_readme_pins_latest_version() -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## (v\d+\.\d+\.\d+) - \d{4}-\d{2}-\d{2}", changelog, re.M)
    if not match:
        fail("CHANGELOG.md has no versioned release heading")
        return
    latest = match.group(1)
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    pins = re.findall(r"marketplace#(v\d+\.\d+\.\d+)", readme)
    if not pins:
        fail(f"README.md pins no version; expected {latest}")
    for pin in set(pins):
        if pin != latest:
            fail(f"README.md pins {pin}; latest CHANGELOG release is {latest}")


def main() -> None:
    validate_index()
    validate_markdown_links()
    validate_required_content()
    validate_workflow_states()
    validate_no_non_ascii()
    validate_readme_pins_latest_version()
    validate_trellis_spec_shape()
    print("trellis-for-research validation passed")


if __name__ == "__main__":
    main()
