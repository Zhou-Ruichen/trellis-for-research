"""A one-feature linear model and a mean-squared-error loss (pure Python)."""

from __future__ import annotations


class LinearModel:
    """``y = slope * x + intercept``."""

    def __init__(self, slope: float = 0.0, intercept: float = 0.0) -> None:
        self.slope = float(slope)
        self.intercept = float(intercept)

    def predict(self, x: float) -> float:
        return self.slope * x + self.intercept

    def predict_list(self, xs: list[float]) -> list[float]:
        return [self.predict(x) for x in xs]

    def params(self) -> dict[str, float]:
        return {"slope": self.slope, "intercept": self.intercept}


def mse(y_pred: list[float], y_true: list[float]) -> float:
    if len(y_pred) != len(y_true):
        raise ValueError("length mismatch between predictions and targets")
    if not y_pred:
        raise ValueError("empty inputs")
    n = len(y_true)
    return sum((p - t) ** 2 for p, t in zip(y_pred, y_true)) / n
