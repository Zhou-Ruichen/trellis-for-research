"""Run-manifest, config, and environment-freeze helpers.

These functions show how a retained-run manifest is produced for real: load and
merge configs, capture git state, capture the environment, and write the
artifacts next to the run outputs.
"""

from __future__ import annotations

import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from importlib import metadata
from pathlib import Path
from typing import Any

import yaml


def load_config(path: str | Path) -> dict[str, Any]:
    src = Path(path)
    if not src.is_file():
        raise FileNotFoundError(f"config not found: {src}")
    return yaml.safe_load(src.read_text(encoding="utf-8")) or {}


def merge_configs(base: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    """Merge an experiment override on top of the base config.

    Merges per section: override keys win, missing keys fall back to base.
    """
    if not override:
        return dict(base)
    merged: dict[str, Any] = {}
    for key, value in base.items():
        merged[key] = dict(value) if isinstance(value, dict) else value
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = {**merged[key], **value}
        else:
            merged[key] = value
    return merged


def resolve_config(base_path: str | Path, override_path: str | Path | None) -> dict[str, Any]:
    return merge_configs(load_config(base_path), load_config(override_path) if override_path else None)


def repo_relative(path: str | Path, root: str | Path) -> str:
    try:
        return str(Path(path).relative_to(root))
    except ValueError:
        return str(path)


def timestamp_run_id(name: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"{stamp}-{name}"


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git_state(repo_root: str | Path) -> dict[str, Any]:
    try:
        commit = subprocess.run(
            ["git", "-C", str(repo_root), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        status = subprocess.run(
            ["git", "-C", str(repo_root), "status", "--porcelain"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return {"commit": commit, "dirty": bool(status)}
    except (subprocess.CalledProcessError, FileNotFoundError):
        return {"commit": "unknown", "dirty": True}


def python_env() -> dict[str, Any]:
    packages: dict[str, str] = {}
    for dist in ("pyyaml", "research-demo"):
        try:
            packages[dist] = metadata.version(dist)
        except metadata.PackageNotFoundError:
            packages[dist] = "not-installed"
    return {
        "manager": "pip (editable install)",
        "python": platform.python_version(),
        "implementation": sys.implementation.name,
        "platform": platform.platform(),
        "packages": packages,
    }


def write_environment_freeze(path: str | Path, env: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Environment freeze captured for this retained run.",
        "# This is a minimal snapshot; real projects use `pip freeze`,",
        "# `uv pip freeze`, `conda env export`, or an equivalent lockfile.",
        f"python: {env['python']}",
        f"implementation: {env['implementation']}",
        f"platform: {env['platform']}",
        "packages:",
    ]
    for name, version in env["packages"].items():
        lines.append(f"  {name}: {version}")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_json(path: str | Path, payload: Any) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def write_config_snapshot(path: str | Path, config: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
