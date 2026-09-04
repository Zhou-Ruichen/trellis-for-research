# Python Style

Use simple, readable Python that is easy to inspect during research.

## Language

- Code, identifiers, docstrings, comments, filenames, and commit messages are
  written in English.
- The language of prose documents (notes, reports, notebook text) is a
  per-project choice: declare it in this project's spec and stay consistent.

## Project Style

- Keep exploratory calculations in their script or notebook. Use the project's
  source area for components explicitly maintained across tasks.
- Use type hints for public functions and tensor-heavy interfaces when they clarify shape or dtype.
- Keep tensor shape comments close to non-obvious transformations.
- Follow [research-minimal.md](./research-minimal.md) for input checks and errors.

## Imports

Preferred order:

```python
import os
from pathlib import Path

import numpy as np
import torch

from research_project.data.dataset import ResearchDataset
```

Do not mutate `sys.path` in durable code. Use an editable install or project
package layout instead.

## Paths

Use `pathlib.Path` for filesystem paths. A one-off script may declare its paths
and parameters directly. Record their values when retaining the result; reuse
existing configuration when the project has it.

## Tensor And Array Code

- Be explicit about expected dimensions for non-trivial tensors.
- At the data boundary, check only shape, dtype, units, and missing-value
  assumptions that affect the calculation.
- Keep device and dtype ownership obvious. Avoid hidden `.cuda()` calls inside low-level helpers.

Example:

```python
def normalize_batch(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    """Normalize a batch of channel-first arrays.

    Args:
        x: Tensor with shape [batch, channels, height, width].
    """
    return (x - mean[None, :, None, None]) / std[None, :, None, None]
```

## Tests

Follow [research-minimal.md](./research-minimal.md) for when to add or run tests.
This style guide adds no minimum test suite for exploratory or durable code.
