"""Full-batch gradient-descent training for LinearModel (pure Python).

Full-batch descent is deterministic: given the same data and initial weights it
produces the same trajectory every time. The data generator is the only source
of randomness in the demo, and it is seeded.
"""

from __future__ import annotations

from .model import LinearModel, mse


def train(
    model: LinearModel,
    x: list[float],
    y: list[float],
    *,
    lr: float,
    epochs: int,
) -> dict[str, list[float] | float]:
    """Train ``model`` in place and return a loss history."""
    if lr <= 0:
        raise ValueError("lr must be positive")
    if epochs <= 0:
        raise ValueError("epochs must be positive")
    n = len(x)
    if n == 0:
        raise ValueError("empty training data")

    history: list[float] = []
    for _ in range(epochs):
        preds = model.predict_list(x)
        errors = [p - t for p, t in zip(preds, y)]
        # Gradient of MSE = mean(err * x) for slope, mean(err) for intercept.
        grad_slope = sum(e * xi for e, xi in zip(errors, x)) / n
        grad_intercept = sum(errors) / n
        model.slope -= lr * grad_slope
        model.intercept -= lr * grad_intercept
        history.append(mse(model.predict_list(x), y))
    return {"final_loss": history[-1], "loss_history": history}
