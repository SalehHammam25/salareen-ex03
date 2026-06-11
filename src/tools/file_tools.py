"""UTF-8 file helpers used by pipeline agents."""

from __future__ import annotations

from pathlib import Path


class FileToolError(Exception):
    """Raised when a required file is not found."""


def ensure_parent_dir(path: str | Path) -> Path:
    """Create all parent directories for *path* and return it as a Path."""
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


def read_text(path: str | Path) -> str:
    """Read and return the UTF-8 contents of *path*.

    Raises FileToolError if the file does not exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileToolError(f"File not found: {p}")
    return p.read_text(encoding="utf-8")


def write_text(path: str | Path, content: str) -> Path:
    """Write *content* to *path* (UTF-8), creating parent dirs as needed.

    Overwrites any existing content.
    """
    p = ensure_parent_dir(path)
    p.write_text(content, encoding="utf-8")
    return p


def append_text(path: str | Path, content: str) -> Path:
    """Append *content* to *path* (UTF-8), creating parent dirs as needed."""
    p = ensure_parent_dir(path)
    with p.open("a", encoding="utf-8") as fh:
        fh.write(content)
    return p
