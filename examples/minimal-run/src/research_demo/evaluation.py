"""Evaluation metrics for LinearModel (pure Python)."""

from __future__ import annotations

import math

from .model import LinearModel, mse


def evaluate(model: LinearModel, x: list[float], y: list[float]) -> dict[str, float | int]:
    n = len(y)
    if n == 0:
        raise ValueError("empty evaluation set")
    preds = model.predict_list(x)
    errors = [p - t for p, t in zip(preds, y)]
    mse_value = mse(preds, y)
    y_mean = sum(y) / n
    ss_res = sum(e * e for e in errors)
    ss_tot = sum((t - y_mean) ** 2 for t in y)
    r2 = 1.0 - (ss_res / ss_tot) if ss_tot > 0 else float("nan")
    return {
        "n_samples": n,
        "mse": mse_value,
        "rmse": math.sqrt(mse_value),
        "mae": sum(abs(e) for e in errors) / n,
        "r2": r2,
        "fitted_slope": model.slope,
        "fitted_intercept": model.intercept,
    }
