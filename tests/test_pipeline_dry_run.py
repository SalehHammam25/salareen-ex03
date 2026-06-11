"""Tests for agent/task factory and dry-run mode — no LLM calls, no API keys needed."""

from __future__ import annotations

import sys
from unittest.mock import patch

import pytest


# ---------------------------------------------------------------------------
# Agent factory
# ---------------------------------------------------------------------------

def test_create_agents_returns_five_entries():
    from src.agents.factory import AGENT_KEYS, create_agents
    agents = create_agents()
    assert len(agents) == len(AGENT_KEYS)
    assert set(agents.keys()) == set(AGENT_KEYS)


def test_agent_roles_match_config():
    from src.agents.factory import create_agents
    agents = create_agents()
    assert agents["research_agent"].role == "Academic Researcher"
    assert agents["outline_agent"].role == "Academic Editor"
    assert agents["writer_agent"].role == "Academic Writer"
    assert agents["reviewer_agent"].role == "Peer Reviewer"
    assert agents["latex_agent"].role == "LaTeX Typesetter"


def test_agents_have_delegation_disabled():
    from src.agents.factory import create_agents
    agents = create_agents()
    for key, agent in agents.items():
        assert agent.allow_delegation is False, f"{key} should not allow delegation"


# ---------------------------------------------------------------------------
# Task factory
# ---------------------------------------------------------------------------

def test_create_tasks_returns_five_tasks():
    from src.agents.factory import create_agents
    from src.tasks.factory import TASK_ORDER, create_tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    assert len(tasks) == len(TASK_ORDER)


def test_tasks_are_in_correct_order():
    from src.agents.factory import create_agents
    from src.tasks.factory import TASK_ORDER, create_tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    assert [t.name for t in tasks] == TASK_ORDER


def test_first_task_has_no_context():
    from src.agents.factory import create_agents
    from src.tasks.factory import create_tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    assert not tasks[0].context  # empty list or None


def test_each_task_context_contains_preceding_tasks():
    from src.agents.factory import create_agents
    from src.tasks.factory import create_tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    for i in range(1, len(tasks)):
        ctx = tasks[i].context or []
        assert tasks[i - 1] in ctx, (
            f"Task '{tasks[i].name}' context should include '{tasks[i-1].name}'"
        )


def test_tasks_have_output_file_set():
    from src.agents.factory import create_agents
    from src.tasks.factory import create_tasks
    agents = create_agents()
    tasks = create_tasks(agents)
    for task in tasks:
        assert task.output_file, f"Task '{task.name}' should have output_file configured"


# ---------------------------------------------------------------------------
# Dry-run integration
# ---------------------------------------------------------------------------

def test_dry_run_prints_agents_and_tasks(capsys):
    from src.main import dry_run
    dry_run()
    out = capsys.readouterr().out
    assert "DRY RUN" in out
    assert "Agents" in out
    assert "Tasks" in out
    assert "research_agent" in out
    assert "latex_task" in out


def test_main_dry_run_via_argv(capsys):
    with patch.object(sys, "argv", ["src.main", "--dry-run"]):
        from src.main import main
        main()
    out = capsys.readouterr().out
    assert "Config is valid" in out


def test_main_without_keys_exits_nonzero(monkeypatch):
    """Without API keys, normal mode should exit with a non-zero code."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    with patch.object(sys, "argv", ["src.main"]):
        from src.main import main
        with pytest.raises(SystemExit) as exc_info:
            main()
    assert exc_info.value.code != 0
