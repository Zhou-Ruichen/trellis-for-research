# Python Style

Use simple, readable Python that is easy to inspect during research.

Code, identifiers, docstrings, comments, filenames, and commit messages use
English. The language of notes, reports, and notebook text follows the project.

Keep exploratory calculations in their script or notebook. Use the project's
source area for code maintained across tasks. Use type hints and shape comments
when they clarify a public interface or a non-obvious tensor transformation;
do not add them mechanically.

Use `pathlib.Path` for filesystem paths. A one-off script may declare paths and
parameters directly. Reuse existing configuration when it exists, and record
the actual values when the result needs to be reproduced.

At data boundaries, check only shape, dtype, units, missing values, or coordinate
assumptions that affect the calculation. Let actual failures determine further
debugging. Do not add a generic input validator or preflight layer.

Keep device and dtype ownership visible. Avoid hidden `.cuda()` calls inside
low-level helpers. Do not add tests for exploratory code unless the task or the
user explicitly requests them.

```python
def normalize_batch(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    """Normalize a batch of channel-first arrays."""
    return (x - mean[None, :, None, None]) / std[None, :, None, None]
```
