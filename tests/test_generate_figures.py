"""Tests for assets/generate_figures.py — no LLM calls, no network required."""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

from assets.generate_figures import (
    asset_names,
    generate_all,
    generate_comparison_table,
    generate_hitl_flow,
    generate_risk_tradeoff,
)


# ---------------------------------------------------------------------------
# asset_names
# ---------------------------------------------------------------------------

def test_asset_names_returns_three_entries():
    assert len(asset_names()) == 3


def test_asset_names_includes_png_and_csv():
    names = asset_names()
    assert any(n.endswith(".png") for n in names)
    assert any(n.endswith(".csv") for n in names)


# ---------------------------------------------------------------------------
# generate_hitl_flow
# ---------------------------------------------------------------------------

def test_hitl_flow_creates_png(tmp_path):
    path = generate_hitl_flow(tmp_path)
    assert path.exists()
    assert path.suffix == ".png"


def test_hitl_flow_is_real_png(tmp_path):
    path = generate_hitl_flow(tmp_path)
    # PNG files start with the 8-byte PNG signature
    assert path.read_bytes()[:4] == b"\x89PNG"


def test_hitl_flow_is_non_empty(tmp_path):
    assert generate_hitl_flow(tmp_path).stat().st_size > 5_000


def test_hitl_flow_creates_parent_dirs(tmp_path):
    path = generate_hitl_flow(tmp_path / "nested" / "assets")
    assert path.exists()


# ---------------------------------------------------------------------------
# generate_risk_tradeoff
# ---------------------------------------------------------------------------

def test_risk_tradeoff_creates_png(tmp_path):
    path = generate_risk_tradeoff(tmp_path)
    assert path.exists()
    assert path.suffix == ".png"


def test_risk_tradeoff_is_real_png(tmp_path):
    assert generate_risk_tradeoff(tmp_path).read_bytes()[:4] == b"\x89PNG"


def test_risk_tradeoff_is_non_empty(tmp_path):
    assert generate_risk_tradeoff(tmp_path).stat().st_size > 5_000


# ---------------------------------------------------------------------------
# generate_comparison_table
# ---------------------------------------------------------------------------

def test_comparison_table_creates_csv(tmp_path):
    path = generate_comparison_table(tmp_path)
    assert path.exists()
    assert path.suffix == ".csv"


def test_comparison_table_header_row(tmp_path):
    path = generate_comparison_table(tmp_path)
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert rows[0] == ["Criterion", "Full Automation", "HITL System"]


def test_comparison_table_has_data_rows(tmp_path):
    path = generate_comparison_table(tmp_path)
    with path.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.reader(fh))
    assert len(rows) >= 5  # header + at least 4 criteria


def test_comparison_table_is_deterministic(tmp_path):
    p1 = generate_comparison_table(tmp_path)
    p2 = generate_comparison_table(tmp_path)
    assert p1.read_bytes() == p2.read_bytes()


# ---------------------------------------------------------------------------
# generate_all
# ---------------------------------------------------------------------------

def test_generate_all_creates_all_assets(tmp_path):
    result = generate_all(assets_dir=tmp_path)
    assert set(result.keys()) == set(asset_names())
    for path in result.values():
        assert path.exists(), f"{path.name} was not created"


def test_generate_all_returns_absolute_paths(tmp_path):
    for path in generate_all(assets_dir=tmp_path).values():
        assert path.is_absolute()


def test_generate_all_all_non_empty(tmp_path):
    for name, path in generate_all(assets_dir=tmp_path).items():
        assert path.stat().st_size > 0, f"{name} is empty"


def test_generate_all_creates_nested_dirs(tmp_path):
    result = generate_all(assets_dir=tmp_path / "a" / "b")
    for path in result.values():
        assert path.exists()


def test_generate_all_csv_repeatable(tmp_path):
    r1 = generate_all(assets_dir=tmp_path)
    r2 = generate_all(assets_dir=tmp_path)
    csv_name = "hitl_comparison_table.csv"
    assert r1[csv_name].read_bytes() == r2[csv_name].read_bytes()
