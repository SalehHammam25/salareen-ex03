"""Tests for src/pipeline/latex_builder.py — no LLM calls, no API keys required."""
from __future__ import annotations

from pathlib import Path

import pytest

from src.pipeline.latex_builder import build_latex_files, latex_file_names


# Helpers

def _tex(tmp_path: Path) -> str:
    build_latex_files(latex_dir=tmp_path)
    return (tmp_path / "main.tex").read_text(encoding="utf-8")


def _bib(tmp_path: Path) -> str:
    build_latex_files(latex_dir=tmp_path)
    return (tmp_path / "refs.bib").read_text(encoding="utf-8")


# File creation

def test_creates_main_tex(tmp_path):
    build_latex_files(latex_dir=tmp_path)
    assert (tmp_path / "main.tex").exists()


def test_creates_refs_bib(tmp_path):
    build_latex_files(latex_dir=tmp_path)
    assert (tmp_path / "refs.bib").exists()


def test_creates_parent_dirs(tmp_path):
    build_latex_files(latex_dir=tmp_path / "nested" / "latex")
    assert (tmp_path / "nested" / "latex" / "main.tex").exists()


def test_returns_expected_keys(tmp_path):
    result = build_latex_files(latex_dir=tmp_path)
    assert set(result.keys()) == set(latex_file_names())


def test_returns_absolute_paths(tmp_path):
    for p in build_latex_files(latex_dir=tmp_path).values():
        assert p.is_absolute()


def test_latex_file_names_returns_two():
    assert len(latex_file_names()) == 2


# main.tex structure

def test_main_tex_has_documentclass(tmp_path):
    assert r"\documentclass" in _tex(tmp_path)


def test_main_tex_has_tableofcontents(tmp_path):
    assert r"\tableofcontents" in _tex(tmp_path)


def test_main_tex_has_maketitle(tmp_path):
    assert r"\maketitle" in _tex(tmp_path)


def test_main_tex_has_fontspec(tmp_path):
    assert "fontspec" in _tex(tmp_path)


def test_main_tex_has_polyglossia(tmp_path):
    assert "polyglossia" in _tex(tmp_path)


def test_main_tex_has_bidi(tmp_path):
    assert "bidi" in _tex(tmp_path)


def test_main_tex_has_otherlanguage_hebrew(tmp_path):
    assert "otherlanguage" in _tex(tmp_path) and "hebrew" in _tex(tmp_path)


def test_main_tex_has_equation(tmp_path):
    assert r"\begin{equation}" in _tex(tmp_path)


def test_main_tex_has_includegraphics(tmp_path):
    assert r"\includegraphics" in _tex(tmp_path)


def test_main_tex_has_hitl_flow_figure(tmp_path):
    assert "hitl_decision_flow" in _tex(tmp_path)


def test_main_tex_has_risk_figure(tmp_path):
    assert "automation_risk_tradeoff" in _tex(tmp_path)


def test_main_tex_has_tabular(tmp_path):
    assert r"\begin{tabular}" in _tex(tmp_path)


def test_main_tex_has_bibliography(tmp_path):
    assert r"\bibliography{refs}" in _tex(tmp_path)


# refs.bib

def test_refs_bib_has_bibtex_entries(tmp_path):
    assert "@" in _bib(tmp_path)


def test_refs_bib_is_non_empty(tmp_path):
    build_latex_files(latex_dir=tmp_path)
    assert (tmp_path / "refs.bib").stat().st_size > 100


# CLI

def test_build_latex_cli_creates_files(tmp_path, monkeypatch):
    import src.pipeline.latex_builder as lb
    monkeypatch.setattr(lb, "_LATEX_DIR", tmp_path)
    from src.pipeline.main import main
    main(argv=["--build-latex"])
    assert (tmp_path / "main.tex").exists()
    assert (tmp_path / "refs.bib").exists()


def test_build_latex_cli_prints_header(tmp_path, monkeypatch, capsys):
    import src.pipeline.latex_builder as lb
    monkeypatch.setattr(lb, "_LATEX_DIR", tmp_path)
    from src.pipeline.main import main
    main(argv=["--build-latex"])
    assert "BUILD LATEX" in capsys.readouterr().out
