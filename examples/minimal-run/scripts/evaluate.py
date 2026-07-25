#!/usr/bin/env python3
"""Re-evaluate a saved checkpoint and rewrite metrics for a retained run.

Thin entrypoint: read the run manifest, load the checkpoint and the recorded
data product, recompute metrics, and overwrite ``metrics.json``.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from research_demo import data as data_mod
from research_demo import evaluation as eval_mod
from research_demo import manifest as manifest_mod
from research_demo.model import LinearModel

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Re-evaluate a saved run checkpoint.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--output-root", default="outputs")
    args = parser.parse_args()

    run_dir = REPO_ROOT / args.output_root / args.run_id
    manifest_path = run_dir / "manifest.json"
    if not manifest_path.is_file():
        raise SystemExit(f"manifest not found: {manifest_path}")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    processed_path = REPO_ROOT / manifest["data"]["processed"]
    dataset = data_mod.load_dataset(processed_path)

    checkpoint_path = REPO_ROOT / manifest["outputs"]["checkpoint"]
    checkpoint = json.loads(checkpoint_path.read_text(encoding="utf-8"))
    model = LinearModel(slope=checkpoint["slope"], intercept=checkpoint["intercept"])

    metrics = eval_mod.evaluate(model, dataset["x"], dataset["y"])
    payload = {"run_id": args.run_id, "split": "all", **metrics}
    manifest_mod.write_json(run_dir / "metrics.json", payload)

    print(
        f"rmse={metrics['rmse']:.4f} mae={metrics['mae']:.4f} "
        f"r2={metrics['r2']:.4f} slope={metrics['fitted_slope']:.4f} "
        f"intercept={metrics['fitted_intercept']:.4f}"
    )


if __name__ == "__main__":
    main()
