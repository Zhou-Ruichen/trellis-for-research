"""sha256 helper for data-product checksums."""

from __future__ import annotations

import hashlib
from pathlib import Path


def sha256_file(path: str | Path) -> str:
    src = Path(path)
    if not src.is_file():
        raise FileNotFoundError(f"cannot checksum missing file: {src}")
    digest = hashlib.sha256()
    digest.update(src.read_bytes())
    return digest.hexdigest()
