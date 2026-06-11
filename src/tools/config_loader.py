"""Load and validate YAML configuration files from config/."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

# Two levels up from src/tools/ → project root
_PROJECT_ROOT = Path(__file__).parent.parent.parent

_REQUIRED_AGENT_KEYS = {"role", "goal", "backstory"}
_REQUIRED_TASK_KEYS = {"description", "expected_output"}


class ConfigError(Exception):
    """Raised when a config file is missing or fails validation."""


def _config_path(filename: str) -> Path:
    return _PROJECT_ROOT / "config" / filename


def load_yaml(filename: str) -> dict[str, Any]:
    """Load a YAML file from config/ by filename."""
    path = _config_path(filename)
    if not path.exists():
        raise ConfigError(f"Config file not found: {path}")
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ConfigError(f"Config file must be a YAML mapping: {path}")
    return data


def load_agents_config() -> dict[str, Any]:
    """Load config/agents.yaml and validate each agent entry."""
    data = load_yaml("agents.yaml")
    for name, cfg in data.items():
        missing = _REQUIRED_AGENT_KEYS - set(cfg.keys())
        if missing:
            raise ConfigError(
                f"Agent '{name}' is missing required keys: {sorted(missing)}"
            )
    return data


def load_tasks_config() -> dict[str, Any]:
    """Load config/tasks.yaml and validate each task entry."""
    data = load_yaml("tasks.yaml")
    for name, cfg in data.items():
        missing = _REQUIRED_TASK_KEYS - set(cfg.keys())
        if missing:
            raise ConfigError(
                f"Task '{name}' is missing required keys: {sorted(missing)}"
            )
    return data
