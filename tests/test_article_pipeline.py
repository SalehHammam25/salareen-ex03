"""Tests for src/pipeline/article_pipeline.py — no LLM calls, no API keys needed."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock

import pytest

from src.pipeline.article_pipeline import (
    PipelineResult,
    PipelineState,
    expected_output_paths,
    run_article_pipeline,
    validate_expected_outputs,
)
from src.tasks.factory import TASK_ORDER
from src.tools.config_loader import load_tasks_config


# ---------------------------------------------------------------------------
# expected_output_paths
# ---------------------------------------------------------------------------

def test_expected_output_paths_count_matches_tasks():
    paths = expected_output_paths()
    assert len(paths) == len(TASK_ORDER)


def test_expected_output_paths_are_path_objects():
    for p in expected_output_paths():
        assert isinstance(p, Path)


def test_expected_output_paths_match_tasks_yaml():
    config = load_tasks_config()
    for key, path in zip(TASK_ORDER, expected_output_paths()):
        declared = config[key]["output_file"]
        assert path.as_posix().endswith(declared.replace("\\", "/"))


def test_expected_output_paths_respects_base_dir(tmp_path):
    for p in expected_output_paths(base_dir=tmp_path):
        assert p.is_relative_to(tmp_path)


def test_expected_output_paths_base_dir_string_accepted(tmp_path):
    paths = expected_output_paths(base_dir=str(tmp_path))
    assert all(p.is_relative_to(tmp_path) for p in paths)


# ---------------------------------------------------------------------------
# validate_expected_outputs
# ---------------------------------------------------------------------------

def test_validate_all_missing(tmp_path):
    paths = expected_output_paths(base_dir=tmp_path)
    state = validate_expected_outputs(paths=paths)
    assert isinstance(state, PipelineState)
    assert len(state.missing) == len(paths)
    assert len(state.present) == 0
    assert not state.is_complete


def test_validate_one_file_present(tmp_path):
    paths = expected_output_paths(base_dir=tmp_path)
    paths[0].parent.mkdir(parents=True, exist_ok=True)
    paths[0].write_text("stub", encoding="utf-8")
    state = validate_expected_outputs(paths=paths)
    assert paths[0] in state.present
    assert len(state.missing) == len(paths) - 1
    assert not state.is_complete


def test_validate_all_present(tmp_path):
    paths = expected_output_paths(base_dir=tmp_path)
    for p in paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("stub", encoding="utf-8")
    state = validate_expected_outputs(paths=paths)
    assert state.is_complete
    assert state.missing == []


def test_validate_uses_base_dir_when_paths_not_given(tmp_path):
    state = validate_expected_outputs(base_dir=tmp_path)
    assert isinstance(state, PipelineState)


# ---------------------------------------------------------------------------
# PipelineState.is_complete
# ---------------------------------------------------------------------------

def test_pipeline_state_complete_when_no_missing():
    s = PipelineState(present=[Path("a")], missing=[])
    assert s.is_complete is True


def test_pipeline_state_incomplete_when_missing():
    s = PipelineState(present=[], missing=[Path("b")])
    assert s.is_complete is False


# ---------------------------------------------------------------------------
# run_article_pipeline
# ---------------------------------------------------------------------------

def test_dry_run_returns_pipeline_result():
    result = run_article_pipeline(dry_run=True)
    assert isinstance(result, PipelineResult)
    assert result.dry_run is True


def test_dry_run_does_not_call_factory():
    called = []

    def _factory():
        called.append(True)
        return MagicMock()

    run_article_pipeline(dry_run=True, crew_factory=_factory)
    assert called == [], "crew_factory must not be called in dry-run mode"


def test_dry_run_kickoff_result_is_none():
    result = run_article_pipeline(dry_run=True)
    assert result.kickoff_result is None


def test_live_run_calls_kickoff():
    fake_crew = MagicMock()
    fake_crew.kickoff.return_value = "done"
    result = run_article_pipeline(crew_factory=lambda: fake_crew)
    fake_crew.kickoff.assert_called_once()
    assert result.kickoff_result == "done"
    assert result.dry_run is False


def test_live_run_result_has_pipeline_state():
    fake_crew = MagicMock()
    result = run_article_pipeline(crew_factory=lambda: fake_crew)
    assert isinstance(result.state, PipelineState)


def test_injected_factory_prevents_real_build_crew(monkeypatch):
    """Verify that providing crew_factory bypasses the real build_crew."""
    import src.pipeline.crew_builder as cb

    def _no_build(**kw):
        raise AssertionError("real build_crew must not be called in tests")

    monkeypatch.setattr(cb, "build_crew", _no_build)

    fake_crew = MagicMock()
    result = run_article_pipeline(crew_factory=lambda: fake_crew)
    assert result is not None
