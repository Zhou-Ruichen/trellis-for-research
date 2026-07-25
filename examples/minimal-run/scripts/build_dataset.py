#!/usr/bin/env python3
"""Regenerate the synthetic dataset and refresh its manifest.

Thin entrypoint: parse config, generate deterministic synthetic data, write the
processed product and its data manifest with a sha256 checksum.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from research_demo import data as data_mod
from research_demo import manifest as manifest_mod
from research_demo.checksum import sha256_file

REPO_ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the synthetic dataset and its manifest.")
    parser.add_argument("--config", default="configs/base.yaml")
    args = parser.parse_args()

    config_path = Path(args.config) if Path(args.config).is_absolute() else REPO_ROOT / args.config
    cfg = manifest_mod.load_config(config_path)
    gen = cfg["data"]["generate"]

    dataset = data_mod.generate_regression(
        n_samples=int(gen["n_samples"]),
        x_min=float(gen["x_min"]),
        x_max=float(gen["x_max"]),
        slope=float(gen["slope"]),
        intercept=float(gen["intercept"]),
        noise_std=float(gen["noise_std"]),
        seed=int(cfg["seed"]),
    )

    processed_path = REPO_ROOT / cfg["data"]["processed"]
    data_mod.save_dataset(processed_path, dataset)

    rel_processed = manifest_mod.repo_relative(processed_path, REPO_ROOT)
    manifest = {
        "name": cfg["data"]["version"],
        "created_at": manifest_mod.now_iso(),
        "created_by": f"python scripts/build_dataset.py --config {manifest_mod.repo_relative(config_path, REPO_ROOT)}",
        "source_paths": ["synthetic gaussian noise generated in-process"],
        "source_versions": {"rng": "python random.Random (Mersenne Twister)"},
        "processing_config": manifest_mod.repo_relative(config_path, REPO_ROOT),
        "output_paths": [rel_processed],
        "checksums": {rel_processed: sha256_file(processed_path)},
        "schema": {"x": "list[float]", "y": "list[float]", "generator": "dict"},
        "split_policy": None,
        "assumptions": [
            "Synthetic data for the runnable example. Not a real measurement.",
        ],
    }

    manifest_path = REPO_ROOT / cfg["data"]["manifest"]
    manifest_mod.write_json(manifest_path, manifest)
    print(f"wrote {rel_processed}")
    print(f"wrote {manifest_mod.repo_relative(manifest_path, REPO_ROOT)}")


if __name__ == "__main__":
    main()
