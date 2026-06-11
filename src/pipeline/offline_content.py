"""Offline content generator — creates deterministic markdown result files.

Used for development, testing, and LaTeX pipeline testing without real LLM or
API calls.  Invoke via the CLI:

    uv run python -m src.pipeline.main --offline-generate
"""
from __future__ import annotations

from pathlib import Path

from src.pipeline.offline_templates import (
    ARTICLE_DRAFT,
    ARTICLE_FINAL,
    ARTICLE_OUTLINE,
    RESEARCH_NOTES,
    REVIEW_NOTES,
)
from src.tools.file_tools import write_text

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_RESULTS_DIR = _PROJECT_ROOT / "results"

# Ordered mapping: filename → content string
_FILES: dict[str, str] = {
    "research_notes.md": RESEARCH_NOTES,
    "article_outline.md": ARTICLE_OUTLINE,
    "article_draft.md": ARTICLE_DRAFT,
    "article_final.md": ARTICLE_FINAL,
    "review_notes.md": REVIEW_NOTES,
}


def file_names() -> list[str]:
    """Return the filenames that generate_all() will write, in pipeline order."""
    return list(_FILES.keys())


def generate_all(results_dir: Path | None = None) -> dict[str, Path]:
    """Write all offline article files and return {filename: absolute Path}.

    Args:
        results_dir: Directory to write into.  Defaults to ``results/`` under
                     the project root.  Pass ``tmp_path`` in tests.
    """
    out = Path(results_dir) if results_dir is not None else _RESULTS_DIR
    return {name: write_text(out / name, content) for name, content in _FILES.items()}
