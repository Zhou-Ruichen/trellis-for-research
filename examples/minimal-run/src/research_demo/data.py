"""Synthetic regression data generation and JSON I/O (no third-party deps)."""

from __future__ import annotations

import json
import random
from pathlib import Path
from typing import Any


def generate_regression(
    *,
    n_samples: int,
    x_min: float,
    x_max: float,
    slope: float,
    intercept: float,
    noise_std: float,
    seed: int,
) -> dict[str, Any]:
    """Generate ``y = slope * x + intercept + gaussian noise``.

    Deterministic for a fixed seed. Pure Python; no NumPy.
    """
    if n_samples <= 0:
        raise ValueError("n_samples must be positive")
    if x_max <= x_min:
        raise ValueError("x_max must be greater than x_min")
    if noise_std < 0:
        raise ValueError("noise_std must be non-negative")
    rng = random.Random(seed)
    if n_samples == 1:
        xs = [0.5 * (x_min + x_max)]
    else:
        step = (x_max - x_min) / (n_samples - 1)
        xs = [x_min + step * i for i in range(n_samples)]
    ys = [slope * x + intercept + rng.gauss(0.0, noise_std) for x in xs]
    return {
        "x": xs,
        "y": ys,
        "generator": {
            "n_samples": n_samples,
            "x_min": x_min,
            "x_max": x_max,
            "slope": slope,
            "intercept": intercept,
            "noise_std": noise_std,
            "seed": seed,
            "rng": "random.Random (Mersenne Twister)",
        },
    }


def save_dataset(path: str | Path, dataset: dict[str, Any]) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(dataset, indent=2), encoding="utf-8")


def load_dataset(path: str | Path) -> dict[str, Any]:
    src = Path(path)
    if not src.is_file():
        raise FileNotFoundError(f"dataset not found: {src}")
    data = json.loads(src.read_text(encoding="utf-8"))
    for key in ("x", "y"):
        if key not in data:
            raise ValueError(f"dataset missing required field {key!r}: {src}")
    if len(data["x"]) != len(data["y"]):
        raise ValueError(f"dataset x and y lengths differ: {src}")
    return data
