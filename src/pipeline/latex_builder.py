"""Generate latex/main.tex and latex/refs.bib for XeLaTeX compilation (Phase 5).

Invoke via CLI:
    uv run run-pipeline --build-latex
"""
from __future__ import annotations

from pathlib import Path

from src.pipeline.latex_templates import MAIN_TEX, REFS_BIB
from src.tools.file_tools import write_text

_PROJECT_ROOT = Path(__file__).parent.parent.parent
_LATEX_DIR = _PROJECT_ROOT / "latex"


def latex_file_names() -> list[str]:
    return ["main.tex", "refs.bib"]


def build_latex_files(latex_dir: Path | None = None) -> dict[str, Path]:
    """Write main.tex and refs.bib; return {filename: path}.

    Pass *latex_dir* in tests to redirect output away from the real latex/ dir.
    """
    out = Path(latex_dir) if latex_dir is not None else _LATEX_DIR
    return {
        "main.tex": write_text(out / "main.tex", MAIN_TEX),
        "refs.bib": write_text(out / "refs.bib", REFS_BIB),
    }
