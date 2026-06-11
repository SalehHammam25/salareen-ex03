"""Tests for src/pipeline/offline_content.py and the --offline-generate CLI flag.

No LLM calls, no API keys, no network access required.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from src.pipeline.offline_content import file_names, generate_all


# ---------------------------------------------------------------------------
# generate_all — file creation
# ---------------------------------------------------------------------------

def test_generates_all_expected_files(tmp_path):
    written = generate_all(results_dir=tmp_path)
    assert set(written.keys()) == set(file_names())
    for path in written.values():
        assert path.exists(), f"{path} was not created"


def test_all_generated_files_are_non_empty(tmp_path):
    for path in generate_all(results_dir=tmp_path).values():
        assert path.stat().st_size > 0, f"{path.name} is empty"


def test_creates_parent_directories(tmp_path):
    nested = tmp_path / "deep" / "nested" / "results"
    generate_all(results_dir=nested)
    assert (nested / "research_notes.md").exists()


def test_generate_all_is_deterministic(tmp_path):
    first = {n: p.read_text(encoding="utf-8") for n, p in generate_all(results_dir=tmp_path).items()}
    second = {n: p.read_text(encoding="utf-8") for n, p in generate_all(results_dir=tmp_path).items()}
    assert first == second


def test_returns_absolute_paths(tmp_path):
    for path in generate_all(results_dir=tmp_path).values():
        assert path.is_absolute()


# ---------------------------------------------------------------------------
# research_notes.md
# ---------------------------------------------------------------------------

def _read(tmp_path: Path, name: str) -> str:
    generate_all(results_dir=tmp_path)
    return (tmp_path / name).read_text(encoding="utf-8")


def test_research_notes_has_author_year_citations(tmp_path):
    content = _read(tmp_path, "research_notes.md")
    assert "[" in content and ", 20" in content


def test_research_notes_has_bibliography_section(tmp_path):
    assert "Bibliography" in _read(tmp_path, "research_notes.md")


# ---------------------------------------------------------------------------
# article_outline.md
# ---------------------------------------------------------------------------

def test_outline_has_numbered_sections(tmp_path):
    content = _read(tmp_path, "article_outline.md")
    assert "1." in content and "2." in content


def test_outline_mentions_conclusion(tmp_path):
    assert "Conclusion" in _read(tmp_path, "article_outline.md")


# ---------------------------------------------------------------------------
# article_draft.md
# ---------------------------------------------------------------------------

def test_draft_has_latex_formula(tmp_path):
    assert "$$" in _read(tmp_path, "article_draft.md")


def test_draft_has_markdown_table(tmp_path):
    content = _read(tmp_path, "article_draft.md")
    assert "|" in content and "---" in content


def test_draft_has_figure_placeholder(tmp_path):
    assert "[FIGURE:" in _read(tmp_path, "article_draft.md")


def test_draft_has_hebrew_characters(tmp_path):
    content = _read(tmp_path, "article_draft.md")
    assert any(0x0590 <= ord(c) <= 0x05FF for c in content), "No Hebrew characters found"


def test_draft_has_citations(tmp_path):
    content = _read(tmp_path, "article_draft.md")
    assert "[" in content and ", 20" in content


# ---------------------------------------------------------------------------
# article_final.md
# ---------------------------------------------------------------------------

def test_final_has_review_marker(tmp_path):
    content = _read(tmp_path, "article_final.md")
    assert "Reviewed" in content or "finalized" in content.lower()


def test_final_has_formula(tmp_path):
    assert "$$" in _read(tmp_path, "article_final.md")


def test_final_has_table(tmp_path):
    content = _read(tmp_path, "article_final.md")
    assert "|" in content and "---" in content


def test_final_has_figure_placeholder(tmp_path):
    assert "[FIGURE:" in _read(tmp_path, "article_final.md")


def test_final_has_hebrew_characters(tmp_path):
    content = _read(tmp_path, "article_final.md")
    assert any(0x0590 <= ord(c) <= 0x05FF for c in content)


# ---------------------------------------------------------------------------
# review_notes.md
# ---------------------------------------------------------------------------

def test_review_notes_has_status(tmp_path):
    content = _read(tmp_path, "review_notes.md")
    assert "APPROVED" in content or "Status" in content


def test_review_notes_has_summary(tmp_path):
    assert "Summary" in _read(tmp_path, "review_notes.md")


# ---------------------------------------------------------------------------
# CLI — --offline-generate
# ---------------------------------------------------------------------------

def test_offline_generate_cli_creates_files(tmp_path, monkeypatch):
    import src.pipeline.offline_content as oc
    monkeypatch.setattr(oc, "_RESULTS_DIR", tmp_path)
    from src.pipeline.main import main
    main(argv=["--offline-generate"])
    for name in file_names():
        assert (tmp_path / name).exists(), f"{name} not created by CLI"


def test_offline_generate_cli_prints_written_paths(tmp_path, monkeypatch, capsys):
    import src.pipeline.offline_content as oc
    monkeypatch.setattr(oc, "_RESULTS_DIR", tmp_path)
    from src.pipeline.main import main
    main(argv=["--offline-generate"])
    out = capsys.readouterr().out
    assert "OFFLINE GENERATE" in out
    assert "WRITTEN" in out
