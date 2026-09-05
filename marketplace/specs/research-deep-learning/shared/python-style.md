# Python Style

Use simple, readable Python that is easy to inspect during research.

Code, identifiers, docstrings, comments, filenames, and commit messages use
English; the language of notes, reports, and notebook text follows the
project.

Keep exploratory calculations in their script or notebook, and the project's
source area for code maintained across tasks. Use type hints and shape
comments when they clarify a public interface or a non-obvious tensor
transformation, not mechanically. Use `pathlib.Path` for filesystem paths; a
one-off script may declare paths and parameters directly. Keep device and
dtype ownership visible, avoiding hidden `.cuda()` calls inside low-level
helpers.

```python
def normalize_batch(x: torch.Tensor, mean: torch.Tensor, std: torch.Tensor) -> torch.Tensor:
    """Normalize a batch of channel-first arrays."""
    return (x - mean[None, :, None, None]) / std[None, :, None, None]
```
