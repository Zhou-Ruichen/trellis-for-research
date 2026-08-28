#!/usr/bin/env python3
"""Validate the local Trellis marketplace structure."""

from __future__ import annotations

import json
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE = ROOT / "marketplace"
WORKFLOW_ID = "research"
WORKFLOW_SOURCE = ROOT / "research-workflow/workflow.md"
WORKFLOW_MIRROR = MARKETPLACE / "workflows/research/workflow.md"
COMPATIBLE_TRELLIS_VERSION = "0.6.16"
INSTALL_READMES = (
    "README.md",
    "README.zh-CN.md",
    "research-workflow/README.md",
)
REQUIRED_WORKFLOW_STATES = (
    "no_task",
    "task_error",
    "planning",
    "planning-inline",
    "in_progress",
    "in_progress-inline",
    "completed",
)


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

    seen_ids: set[str] = set()
    workflow_entry: dict | None = None
    for template in templates:
        if not isinstance(template, dict):
            fail(f"template entry must be an object: {template!r}")
        for key in ("id", "type", "name", "path"):
            if not isinstance(template.get(key), str):
                fail(f"template entry must include string {key!r}: {template}")
        template_id = template["id"]
        if template_id in seen_ids:
            fail(f"duplicate template id: {template_id}")
        seen_ids.add(template_id)

        template_type = template["type"]
        if template_type == "spec":
            template_path = (ROOT / template["path"]).resolve()
            try:
                template_path.relative_to(MARKETPLACE.resolve())
            except ValueError:
                fail(f"spec template path leaves marketplace root: {template['path']}")
            if not template_path.is_dir():
                fail(f"spec template path does not exist: {template['path']}")
            if not (template_path / "README.md").is_file():
                fail(f"spec template path lacks README.md: {template['path']}")
        elif template_type == "workflow":
            template_path = (MARKETPLACE / template["path"]).resolve()
            try:
                template_path.relative_to(MARKETPLACE.resolve())
            except ValueError:
                fail(f"workflow path leaves marketplace root: {template['path']}")
            if template_path.suffix != ".md" or not template_path.is_file():
                fail(f"workflow path must name a Markdown file: {template['path']}")
            if template_id == WORKFLOW_ID:
                workflow_entry = template
        else:
            fail(f"unsupported template type {template_type!r}")

    if workflow_entry is None:
        fail(f"marketplace lacks workflow template {WORKFLOW_ID!r}")
    if workflow_entry["path"] != "workflows/research/workflow.md":
        fail("research workflow path is not the stable marketplace path")
    if workflow_entry.get("trellisVersion") != COMPATIBLE_TRELLIS_VERSION:
        fail(
            "research workflow trellisVersion must be "
            f"{COMPATIBLE_TRELLIS_VERSION}"
        )


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
            "General Computational Research",
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
            "trellis-compatibility: 0.6.16",
            "Trellis 0.6.16 defaults Codex to `auto`",
            "`codex.dispatch_mode: inline`",
            "[workflow-state:task_error]",
            "--allow-empty-context",
            "one result-producing invocation",
            "same invocation supplies the sanity observation",
            "No separate test suite",
            "automatic retry",
            "repeat after a pass without new failure evidence",
            "diff review only; do not run a build or test",
            "smallest relevant check",
            "Scientific metric values are never task-completion gates",
            "unexpected scientific results are findings",
            "retained results record the command",
            "Do not dispatch implement or check sub-agents",
            "Task completion does not approve a scientific claim",
            ".codex/hooks/inject-workflow-state.py",
        ],
        "research-workflow/README.md": [
            "`research-workflow/workflow.md` is authoritative",
            "`trellisVersion: 0.6.16`",
            "Trellis 0.6.16 does not enforce",
            "`codex.dispatch_mode: auto`",
            "dispatch_mode: inline",
            "--template research",
            "--marketplace gh:Zhou-Ruichen/trellis-for-research/marketplace#",
            "--workflow-source gh:Zhou-Ruichen/trellis-for-research/marketplace#",
            "task.py start <task-dir> --allow-empty-context",
            "default apply mode exits before",
            "does not patch",
            ".codex/hooks/inject-workflow-state.py",
        ],
        "research-workflow/skills/trellis-research-check/SKILL.md": [
            "execute the experiment once",
            "result-producing",
            "the experiment again",
            "does not require",
        ],
        "research-workflow/apply.sh": [
            "apply mode is deprecated and performs no writes",
            "this workflow targets Trellis",
            "--create-new",
            "workflow.md is user-managed",
        ],
        ".github/workflows/validate.yml": [
            "npm install -g @mindfoldhq/trellis@0.6.16",
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
            "Once a retained run or comparison starts",
            "does not approve a scientific claim",
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
            "Once a retained run or comparison starts",
            "does not approve a scientific claim",
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
            "A completed Trellis task does not approve a scientific claim",
        ],
        "marketplace/specs/dl-earth-research/guides/write-results.md": [
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


WORKFLOW_STATE_RE = re.compile(
    r"^\[(?P<close>/?)workflow-state:(?P<name>[A-Za-z0-9_-]+)\]$", re.M
)
WORKFLOW_MARKETPLACE_RE = re.compile(
    r"--marketplace\s+"
    r"gh:Zhou-Ruichen/trellis-for-research/marketplace#([^\s`]+)"
)
FORBIDDEN_SHELL_COMMANDS = {
    "bash",
    "chmod",
    "chown",
    "cp",
    "dd",
    "find",
    "git",
    "install",
    "ln",
    "mkdir",
    "mv",
    "node",
    "perl",
    "python",
    "python3",
    "rm",
    "rmdir",
    "rsync",
    "ruby",
    "sed",
    "sh",
    "tee",
    "touch",
    "truncate",
    "zsh",
}
FILE_REDIRECTION_TOKENS = {">", ">>", "<", "<<", "<<<", "<>"}


def validate_read_only_shell(path: Path, text: str) -> None:
    """Reject common mutation commands and file redirections in apply.sh."""
    for line_number, line in enumerate(text.splitlines(), start=1):
        lexer = shlex.shlex(
            line,
            posix=True,
            punctuation_chars="|&;()<>",
        )
        lexer.whitespace_split = True
        lexer.commenters = "#"
        try:
            tokens = list(lexer)
        except ValueError as exc:
            fail(f"{path.relative_to(ROOT)}:{line_number} is invalid shell: {exc}")

        for index, token in enumerate(tokens):
            if token in FORBIDDEN_SHELL_COMMANDS:
                fail(
                    f"{path.relative_to(ROOT)}:{line_number} contains "
                    f"forbidden command {token!r}"
                )
            if token not in FILE_REDIRECTION_TOKENS:
                continue
            target = tokens[index + 1] if index + 1 < len(tokens) else ""
            if token == ">" and target == "/dev/null":
                continue
            fail(
                f"{path.relative_to(ROOT)}:{line_number} contains "
                f"file redirection {token!r}"
            )


def validate_workflow_contract() -> None:
    if not WORKFLOW_SOURCE.is_file():
        fail("authoritative research workflow is missing")
    if not WORKFLOW_MIRROR.is_file():
        fail("marketplace workflow mirror is missing")
    if WORKFLOW_SOURCE.read_bytes() != WORKFLOW_MIRROR.read_bytes():
        fail("marketplace workflow mirror differs from authoritative source")

    text = WORKFLOW_SOURCE.read_text(encoding="utf-8")
    stack: list[str] = []
    opened: list[str] = []
    for match in WORKFLOW_STATE_RE.finditer(text):
        name = match.group("name")
        if not match.group("close"):
            if name in opened:
                fail(f"duplicate workflow-state block: {name}")
            opened.append(name)
            stack.append(name)
            continue
        if not stack or stack[-1] != name:
            fail(f"unbalanced workflow-state close: {name}")
        stack.pop()
    if stack:
        fail(f"unclosed workflow-state block: {stack[-1]}")
    if tuple(opened) != REQUIRED_WORKFLOW_STATES:
        fail(
            "workflow-state blocks must be exactly: "
            + ", ".join(REQUIRED_WORKFLOW_STATES)
        )

    malformed = []
    for line in text.splitlines():
        stripped = line.strip()
        if (
            "workflow-state:" in stripped
            and stripped.startswith("[")
            and stripped.endswith("]")
            and WORKFLOW_STATE_RE.fullmatch(line) is None
        ):
            malformed.append(line)
    if malformed:
        fail(f"malformed workflow-state block line: {malformed[0]}")

    if (ROOT / "research-workflow/agents/implement.md").exists():
        fail("custom research implement agent must remain removed")

    marker_match = re.search(r"trellis-compatibility:\s*([^\s]+)", text)
    if not marker_match or marker_match.group(1) != COMPATIBLE_TRELLIS_VERSION:
        fail("workflow compatibility marker differs from the validator version")

    apply_path = ROOT / "research-workflow/apply.sh"
    apply_text = apply_path.read_text(encoding="utf-8")
    version_match = re.search(
        r'^EXPECTED_TRELLIS_VERSION="([^"]+)"$', apply_text, re.M
    )
    if not version_match or version_match.group(1) != COMPATIBLE_TRELLIS_VERSION:
        fail("apply.sh Trellis version differs from the validator version")
    source_match = re.search(
        r"^MARKETPLACE_SOURCE='[^']+#(v\d+\.\d+\.\d+)'$", apply_text, re.M
    )
    latest = latest_release_version()
    if not source_match or source_match.group(1) != latest:
        fail(f"apply.sh marketplace source must pin latest release {latest}")
    validate_read_only_shell(apply_path, apply_text)


def latest_release_version() -> str:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"^## (v\d+\.\d+\.\d+) - \d{4}-\d{2}-\d{2}", changelog, re.M)
    if not match:
        fail("CHANGELOG.md has no versioned release heading")
    return match.group(1)


def validate_workflow_install_docs() -> None:
    latest = latest_release_version()
    expected_source = (
        "gh:Zhou-Ruichen/trellis-for-research/marketplace#" + latest
    )
    for rel_path in INSTALL_READMES:
        text = (ROOT / rel_path).read_text(encoding="utf-8")
        if "--template research" not in text:
            fail(f"{rel_path} lacks the official workflow template option")
        if "--workflow research" not in text:
            fail(f"{rel_path} lacks the combined new-project workflow option")
        if f"--workflow-source {expected_source}" not in text:
            fail(f"{rel_path} does not pin the new-project workflow source to {latest}")
        if "dispatch_mode: inline" not in text:
            fail(f"{rel_path} lacks the explicit Codex inline setting")
        english_default = re.search(
            r"defaults(?: Codex)? to `(?:codex\.dispatch_mode: )?auto`", text
        )
        chinese_default = "\u9ed8\u8ba4\u503c\u662f `auto`" in text
        if english_default is None and not chinese_default:
            fail(f"{rel_path} does not state the Trellis 0.6.16 Codex default")
        if f"--marketplace {expected_source}" not in text:
            fail(f"{rel_path} does not pin the workflow marketplace to {latest}")
        if "<release-tag>" in text:
            fail(f"{rel_path} still contains a release-tag placeholder")
        if re.search(
            r"--marketplace\s+"
            r"gh:Zhou-Ruichen/trellis-for-research/marketplace(?:\s|$)",
            text,
        ):
            fail(f"{rel_path} contains an unpinned workflow marketplace command")
        refs = WORKFLOW_MARKETPLACE_RE.findall(text)
        if not refs:
            fail(f"{rel_path} lacks a workflow marketplace release reference")
        for ref in refs:
            if ref != latest:
                fail(f"{rel_path} pins workflow ref {ref}; expected {latest}")


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
        # research-workflow/ and its exact marketplace workflow mirror keep
        # Trellis workflow punctuation. The spec marketplace stays ASCII.
        if any(part == "examples" for part in rel_path.parts):
            continue
        if rel_path == Path("README.zh-CN.md"):
            continue
        if "research-workflow" in rel_path.parts:
            continue
        if rel_path == Path("marketplace/workflows/research/workflow.md"):
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
    latest = latest_release_version()
    for rel_path in INSTALL_READMES:
        readme = (ROOT / rel_path).read_text(encoding="utf-8")
        pins = re.findall(r"marketplace#(v\d+\.\d+\.\d+)", readme)
        if not pins:
            fail(f"{rel_path} pins no version; expected {latest}")
        for pin in set(pins):
            if pin != latest:
                fail(f"{rel_path} pins {pin}; latest CHANGELOG release is {latest}")


def main() -> None:
    validate_index()
    validate_workflow_contract()
    validate_workflow_install_docs()
    validate_markdown_links()
    validate_required_content()
    validate_no_non_ascii()
    validate_readme_pins_latest_version()
    validate_trellis_spec_shape()
    print("trellis-for-research validation passed")


if __name__ == "__main__":
    main()
