"""Minimum meaningful smoke tests for the demo package."""

from research_demo import data as data_mod
from research_demo import evaluation as eval_mod
from research_demo import training as train_mod
from research_demo.model import LinearModel


def test_dataset_shapes_and_short_training():
    dataset = data_mod.generate_regression(
        n_samples=16,
        x_min=0.0,
        x_max=10.0,
        slope=2.0,
        intercept=1.0,
        noise_std=0.5,
        seed=42,
    )
    assert len(dataset["x"]) == 16
    assert len(dataset["x"]) == len(dataset["y"])

    model = LinearModel()
    history = train_mod.train(model, dataset["x"], dataset["y"], lr=0.01, epochs=5)
    assert history["final_loss"] == history["loss_history"][-1]

    metrics = eval_mod.evaluate(model, dataset["x"], dataset["y"])
    assert metrics["n_samples"] == 16
    assert metrics["rmse"] >= 0
    # finite check (not NaN)
    for key in ("mse", "rmse", "mae", "r2"):
        assert metrics[key] == metrics[key]
