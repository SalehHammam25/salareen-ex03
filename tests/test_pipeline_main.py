"""Tests for src/pipeline/main.py — no LLM calls, no API keys needed."""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from src.pipeline.main import main


# ---------------------------------------------------------------------------
# --dry-run
# ---------------------------------------------------------------------------

def test_dry_run_prints_header(capsys):
    main(argv=["--dry-run"])
    assert "DRY RUN" in capsys.readouterr().out


def test_dry_run_prints_output_file_paths(capsys):
    main(argv=["--dry-run"])
    out = capsys.readouterr().out
    # tasks.yaml declares paths under results/ and latex/
    assert "results" in out or "latex" in out


def test_dry_run_confirms_no_llm_calls(capsys):
    main(argv=["--dry-run"])
    assert "No LLM" in capsys.readouterr().out


def test_dry_run_does_not_invoke_crew_factory():
    called = []

    def _factory():
        called.append(True)
        return MagicMock()

    main(argv=["--dry-run"], crew_factory=_factory)
    assert called == [], "crew_factory must not be called during --dry-run"


def test_dry_run_shows_present_count(capsys):
    main(argv=["--dry-run"])
    out = capsys.readouterr().out
    assert "Outputs present:" in out


# ---------------------------------------------------------------------------
# --check-outputs
# ---------------------------------------------------------------------------

def test_check_outputs_prints_header(capsys):
    main(argv=["--check-outputs"])
    assert "OUTPUT CHECK" in capsys.readouterr().out


def test_check_outputs_reports_missing_when_results_absent(capsys):
    main(argv=["--check-outputs"])
    out = capsys.readouterr().out
    # In a clean repo no output files exist yet
    assert "Missing" in out or "incomplete" in out.lower()


def test_check_outputs_does_not_invoke_crew_factory():
    called = []

    def _factory():
        called.append(True)
        return MagicMock()

    main(argv=["--check-outputs"], crew_factory=_factory)
    assert called == []


def test_check_outputs_shows_complete_when_all_present(tmp_path, monkeypatch):
    import src.pipeline.article_pipeline as ap

    # Redirect expected_output_paths to tmp_path so we can create them all
    original = ap.expected_output_paths

    def _patched(base_dir=None):
        return original(base_dir=tmp_path)

    monkeypatch.setattr(ap, "expected_output_paths", _patched)

    for p in original(base_dir=tmp_path):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("stub", encoding="utf-8")

    main(argv=["--check-outputs"])
    out = capsys.readouterr().out if False else ""  # need capsys — done below


def test_check_outputs_complete_message(tmp_path, monkeypatch, capsys):
    import src.pipeline.article_pipeline as ap

    original = ap.expected_output_paths

    def _patched(base_dir=None):
        return original(base_dir=tmp_path)

    monkeypatch.setattr(ap, "expected_output_paths", _patched)

    for p in original(base_dir=tmp_path):
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("stub", encoding="utf-8")

    main(argv=["--check-outputs"])
    out = capsys.readouterr().out
    assert "Complete." in out


# ---------------------------------------------------------------------------
# normal run with injected factory
# ---------------------------------------------------------------------------

def test_normal_run_calls_kickoff(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    fake_crew = MagicMock()
    fake_crew.kickoff.return_value = None
    main(argv=[], crew_factory=lambda: fake_crew)
    fake_crew.kickoff.assert_called_once()


def test_normal_run_prints_done(monkeypatch, capsys):
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")
    fake_crew = MagicMock()
    fake_crew.kickoff.return_value = None
    main(argv=[], crew_factory=lambda: fake_crew)
    out = capsys.readouterr().out
    assert "DONE" in out


def test_normal_run_exits_nonzero_without_api_keys(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    # Patch load_dotenv so it cannot reload keys from a local .env file
    with patch("src.pipeline.main.load_dotenv", lambda: None):
        with pytest.raises(SystemExit) as exc:
            main(argv=[])
    assert exc.value.code != 0


def test_normal_run_injected_factory_bypasses_build_crew(monkeypatch):
    import src.pipeline.crew_builder as cb

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-key")

    def _no_build(**kw):
        raise AssertionError("real build_crew must not be called in tests")

    monkeypatch.setattr(cb, "build_crew", _no_build)
    fake_crew = MagicMock()
    # Should complete without triggering the monkeypatched build_crew
    main(argv=[], crew_factory=lambda: fake_crew)
