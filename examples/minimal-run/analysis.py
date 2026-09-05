"""Fit a line to seeded synthetic observations and print in-sample results."""

import json
import math
import platform
import random
from statistics import linear_regression, mean

seed = 42
n_samples = 200
x_min, x_max = 0.0, 10.0
true_slope, true_intercept = 2.0, 1.0
noise_std = 0.5

rng = random.Random(seed)
step = (x_max - x_min) / (n_samples - 1)
x = [x_min + step * i for i in range(n_samples)]
y = [true_slope * value + true_intercept + rng.gauss(0.0, noise_std) for value in x]
slope, intercept = linear_regression(x, y)
errors = [slope * value + intercept - target for value, target in zip(x, y)]
squared_error = sum(error**2 for error in errors)
y_mean = mean(y)

print(json.dumps({
    "python": platform.python_version(),
    "data": {
        "kind": "synthetic",
        "seed": seed,
        "n_samples": n_samples,
        "x_range": [x_min, x_max],
        "true_slope": true_slope,
        "true_intercept": true_intercept,
        "noise_std": noise_std,
    },
    "method": "ordinary least squares (statistics.linear_regression)",
    "fit": {"slope": slope, "intercept": intercept},
    "in_sample": {
        "rmse": math.sqrt(squared_error / n_samples),
        "mae": mean(abs(error) for error in errors),
        "r2": 1.0 - squared_error / sum((value - y_mean)**2 for value in y),
    },
}, indent=2))
