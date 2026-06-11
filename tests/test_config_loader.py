"""Tests for src/tools/config_loader.py — no LLM calls, no API keys needed."""

from __future__ import annotations

import pytest
import yaml


# ---------------------------------------------------------------------------
# Tests against the real config files
# ---------------------------------------------------------------------------

def test_load_agents_config_has_all_five_agents():
    from src.tools.config_loader import load_agents_config
    config = load_agents_config()
    expected = {"research_agent", "outline_agent", "writer_agent", "reviewer_agent", "latex_agent"}
    assert expected.issubset(set(config.keys()))


def test_every_agent_has_required_fields():
    from src.tools.config_loader import load_agents_config
    config = load_agents_config()
    for name, cfg in config.items():
        assert "role" in cfg, f"Agent '{name}' missing 'role'"
        assert "goal" in cfg, f"Agent '{name}' missing 'goal'"
        assert "backstory" in cfg, f"Agent '{name}' missing 'backstory'"


def test_agent_fields_are_non_empty_strings():
    from src.tools.config_loader import load_agents_config
    config = load_agents_config()
    for name, cfg in config.items():
        for field in ("role", "goal", "backstory"):
            value = cfg[field]
            assert isinstance(value, str) and value.strip(), (
                f"Agent '{name}' field '{field}' is empty or not a string"
            )


def test_load_tasks_config_has_all_five_tasks():
    from src.tools.config_loader import load_tasks_config
    config = load_tasks_config()
    expected = {"research_task", "outline_task", "writer_task", "reviewer_task", "latex_task"}
    assert expected.issubset(set(config.keys()))


def test_every_task_has_required_fields():
    from src.tools.config_loader import load_tasks_config
    config = load_tasks_config()
    for name, cfg in config.items():
        assert "description" in cfg, f"Task '{name}' missing 'description'"
        assert "expected_output" in cfg, f"Task '{name}' missing 'expected_output'"


# ---------------------------------------------------------------------------
# Error-path tests using temp files
# ---------------------------------------------------------------------------

def test_config_error_on_missing_file():
    from src.tools.config_loader import ConfigError, load_yaml
    with pytest.raises(ConfigError, match="not found"):
        load_yaml("does_not_exist.yaml")


def test_config_error_on_agent_missing_required_keys(tmp_path, monkeypatch):
    import src.tools.config_loader as loader

    bad = {"broken_agent": {"role": "Only Role"}}  # missing goal + backstory
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "agents.yaml").write_text(yaml.dump(bad), encoding="utf-8")

    monkeypatch.setattr(loader, "_PROJECT_ROOT", tmp_path)

    with pytest.raises(loader.ConfigError, match="missing required keys"):
        loader.load_agents_config()


def test_config_error_on_task_missing_required_keys(tmp_path, monkeypatch):
    import src.tools.config_loader as loader

    bad = {"broken_task": {"description": "only description"}}  # missing expected_output
    config_dir = tmp_path / "config"
    config_dir.mkdir()
    (config_dir / "tasks.yaml").write_text(yaml.dump(bad), encoding="utf-8")

    monkeypatch.setattr(loader, "_PROJECT_ROOT", tmp_path)

    with pytest.raises(loader.ConfigError, match="missing required keys"):
        loader.load_tasks_config()
