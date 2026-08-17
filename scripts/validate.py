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
        if template["type"] != "spec":
            fail(f"unsupported template type {template['type']!r}; expected 'spec'")
        template_path = ROOT / template["path"]
        if not template_path.is_dir():
            fail(f"template path does not exist: {template['path']}")
        if not (template_path / "README.md").is_file():
            fail(f"template path lacks README.md: {template['path']}")


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
        "marketplace/specs/research-core/README.md": [
            "Research Core",
            "Template Fit",
            "dl-earth-research",
        ],
        "marketplace/specs/research-core/shared/research-minimal.md": [
            "exploratory",
            "smallest change",
            "concrete, likely failure",
            "cheapest check",
            "Stop condition",
            "durable",
            "retained",
        ],
        "marketplace/specs/dl-earth-research/shared/research-minimal.md": [
            "exploratory",
            "smallest change",
            "concrete, likely failure",
            "cheapest check",
            "Stop condition",
            "durable",
            "retained",
        ],
        "research-workflow/workflow.md": [
            "verification depth follows the task mode",
            "is a skill only",
            "Phase 2.2 owns the result-producing invocation and validation",
            "one result-producing invocation",
            "Keep `research/` to Markdown investigation notes and small metadata",
            "Exploratory tasks are PRD-only by default",
            "seed-only manifests are valid otherwise",
            "actual invocation, observation, findings, and output paths",
            "spec update only if durable knowledge",
            "Never repeat a passed check",
            "default exploratory",
        ],
        "research-workflow/README.md": [
            "verification depth follows the task mode",
            "Phase 2.1 only prepares code and configuration",
            "Exploratory tasks are PRD-only by default",
            ".agents/skills",
        ],
        "research-workflow/agents/implement.md": [
            "No execution or self-validation",
            "Phase 2.2 of the workflow owns the single result-producing invocation",
            "leave that execution to Phase 2.2",
        ],
        "research-workflow/skills/trellis-research-check/SKILL.md": [
            "execute the experiment once",
            "result-producing",
            "the experiment again",
        ],
        "marketplace/specs/research-core/shared/project-layout.md": [
            "data/raw/",
            "data/interim/",
            "data/processed/",
            "outputs/<run_id>/",
            "existing documented layout",
        ],
        "marketplace/specs/research-core/shared/anti-bloat.md": [
            "Delete superseded code",
            "Repo-wide sweeps",
            "experiment record",
            "*_v2",
            "*_final",
        ],
        "marketplace/specs/research-core/shared/reproducibility.md": [
            "manifest.json",
            "metrics.json",
            "Do not invent",
            "Scratch",
            "Retained",
            '"retention"',
            '"manager"',
            '"freeze"',
        ],
        "marketplace/specs/research-core/data/index.md": [
            "Manifest Rule",
            "Boundary Validation",
            "leakage",
        ],
        "marketplace/specs/research-core/evaluation/index.md": [
            "Retained evaluation runs",
            "Comparison",
            "reports",
        ],
        "marketplace/specs/dl-earth-research/shared/project-layout.md": [
            "data/raw/",
            "data/interim/",
            "data/processed/",
            "outputs/<run_id>/",
        ],
        "marketplace/specs/dl-earth-research/shared/anti-bloat.md": [
            "Delete superseded code",
            "Repo-wide sweeps",
            "experiment record",
            "*_v2.py",
            "*_final.py",
        ],
        "marketplace/specs/dl-earth-research/shared/reproducibility.md": [
            "manifest.json",
            "metrics.json",
            "Do not invent",
            "Scratch",
            "Retained",
            '"retention"',
            '"manager"',
            '"freeze"',
        ],
        "marketplace/specs/dl-earth-research/data/index.md": [
            "SWOT",
            "Data Lake Rule",
            "Manifest Rule",
        ],
        "marketplace/specs/dl-earth-research/evaluation/index.md": [
            "Retained evaluation runs",
            "Scratch and smoke evaluation runs",
            "Retained prediction products",
        ],
        "marketplace/specs/dl-earth-research/training/index.md": [
            "PyTorch",
            "Lightning",
            "smoke",
        ],
        "marketplace/specs/research-core/shared/scientific-writing.md": [
            "Engineering Term Isolation",
            "Anti AI Tone",
            "Write Like A Human",
            "Over-Ornamentation",
            "Bilingual Policy",
            "Self-Check Before Submitting Prose",
        ],
        "marketplace/specs/dl-earth-research/shared/scientific-writing.md": [
            "Engineering Term Isolation",
            "Anti AI Tone",
            "Write Like A Human",
            "Over-Ornamentation",
            "Bilingual Policy",
            "Self-Check Before Submitting Prose",
        ],
        "marketplace/specs/research-core/guides/write-results.md": [
            "Write A Results Discussion",
            "scientific question",
            "Completion Checklist",
        ],
        "marketplace/specs/dl-earth-research/guides/write-results.md": [
            "Write A Results Discussion",
            "scientific question",
            "Completion Checklist",
        ],
    }
    for rel_path, needles in required.items():
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"{rel_path} missing required text: {needle}")


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
        # research-workflow/ holds overlay masters derived from Trellis-managed
        # project files; they keep upstream punctuation and CJK reply words.
        if any(part == "examples" for part in rel_path.parts):
            continue
        if "research-workflow" in rel_path.parts:
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
        "dl-earth-research": [
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
        "research-core": [
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

    with tempfile.TemporaryDirectory(prefix="trellis-research-spec-") as tmp:
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
    validate_no_non_ascii()
    validate_readme_pins_latest_version()
    validate_trellis_spec_shape()
    print("trellis-research-spec validation passed")


if __name__ == "__main__":
    main()
