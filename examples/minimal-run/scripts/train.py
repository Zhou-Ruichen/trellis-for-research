#!/usr/bin/env python3
"""Train the demo linear model and write a retained run directory.

Thin entrypoint: resolve config, load the processed dataset, train, evaluate,
and write the retained-run artifacts (config snapshot, metrics, checkpoint,
environment freeze, and manifest).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from research_demo import data as data_mod
from research_demo import evaluation as eval_mod
from research_demo import manifest as manifest_mod
from research_demo import training as train_mod
from research_demo.model import LinearModel

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Train the demo linear model.")
    parser.add_argument("--config", default="configs/exp/linear.yaml")
    parser.add_argument("--base", default="configs/base.yaml")
    parser.add_argument("--run-id", default=None, help="Override the generated run id.")
    args = parser.parse_args()

    config_path = Path(args.config) if Path(args.config).is_absolute() else REPO_ROOT / args.config
    base_path = Path(args.base) if Path(args.base).is_absolute() else REPO_ROOT / args.base
    cfg = manifest_mod.resolve_config(base_path, config_path)

    processed_path = REPO_ROOT / cfg["data"]["processed"]
    dataset = data_mod.load_dataset(processed_path)

    model = LinearModel()
    history = train_mod.train(
        model,
        dataset["x"],
        dataset["y"],
        lr=float(cfg["optimizer"]["lr"]),
        epochs=int(cfg["training"]["epochs"]),
    )
    metrics = eval_mod.evaluate(model, dataset["x"], dataset["y"])

    retention = cfg["run"].get("retention", "retained")
    run_id = args.run_id or manifest_mod.timestamp_run_id(cfg["run"]["name"])
    run_dir = REPO_ROOT / cfg["run"]["output_root"] / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    rel_config = manifest_mod.repo_relative(config_path, REPO_ROOT)
    rel_base = manifest_mod.repo_relative(base_path, REPO_ROOT)
    rel_processed = manifest_mod.repo_relative(processed_path, REPO_ROOT)

    snapshot_path = run_dir / "config.yaml"
    metrics_path = run_dir / "metrics.json"
    checkpoint_path = run_dir / "checkpoint.json"
    freeze_path = run_dir / "environment.freeze.txt"

    manifest_mod.write_config_snapshot(snapshot_path, cfg)
    manifest_mod.write_json(
        metrics_path,
        {
            "run_id": run_id,
            "split": "all",
            **metrics,
            "loss_history": history["loss_history"],
        },
    )
    manifest_mod.write_json(checkpoint_path, {"run_id": run_id, **model.params()})

    env = manifest_mod.python_env()
    environment_field: dict
    if retention == "retained":
        manifest_mod.write_environment_freeze(freeze_path, env)
        environment_field = {
            **env,
            "freeze": manifest_mod.repo_relative(freeze_path, REPO_ROOT),
        }
    else:
        environment_field = {
            "manager": env["manager"],
            "note": "scratch run; no environment freeze written unless promoted to retained",
        }

    manifest = {
        "run_id": run_id,
        "created_at": manifest_mod.now_iso(),
        "command": f"python scripts/train.py --config {rel_config}",
        "retention": retention,
        "retention_reason": cfg["run"].get("retention_reason") if retention == "retained" else None,
        "git": manifest_mod.git_state(REPO_ROOT),
        "parameters": {
            "base_config": rel_base,
            "config_path": rel_config,
            "config_snapshot": manifest_mod.repo_relative(snapshot_path, REPO_ROOT),
            "data_seed": int(cfg["seed"]),
            "lr": float(cfg["optimizer"]["lr"]),
            "epochs": int(cfg["training"]["epochs"]),
        },
        "randomness": {
            "used": True,
            "seed": int(cfg["seed"]),
            "scope": "data generation only",
            "note": (
                "Gaussian observation noise is seeded by parameters.data_seed. "
                "Training is full-batch gradient descent and is deterministic."
            ),
        },
        "environment": environment_field,
        "data": {
            "manifest": cfg["data"]["manifest"],
            "processed": rel_processed,
        },
        "outputs": {
            "metrics": manifest_mod.repo_relative(metrics_path, REPO_ROOT),
            "checkpoint": manifest_mod.repo_relative(checkpoint_path, REPO_ROOT),
        },
        "assumptions": cfg.get("assumptions", []),
    }
    manifest_mod.write_json(run_dir / "manifest.json", manifest)

    print(f"run_id: {run_id}")
    print(f"retention: {retention}")
    print(
        f"metrics: rmse={metrics['rmse']:.4f} mae={metrics['mae']:.4f} "
        f"r2={metrics['r2']:.4f} slope={metrics['fitted_slope']:.4f} "
        f"intercept={metrics['fitted_intercept']:.4f}"
    )
    print(f"manifest: {manifest_mod.repo_relative(run_dir / 'manifest.json', REPO_ROOT)}")


if __name__ == "__main__":
    main()
