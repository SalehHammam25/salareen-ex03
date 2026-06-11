"""Create CrewAI Agent objects from config/agents.yaml."""

from __future__ import annotations

from crewai import Agent

from src.tools.config_loader import load_agents_config

# Canonical order — must match keys present in config/agents.yaml
AGENT_KEYS: list[str] = [
    "research_agent",
    "outline_agent",
    "writer_agent",
    "reviewer_agent",
    "latex_agent",
]


def create_agents() -> dict[str, Agent]:
    """Return {agent_key: Agent} for every agent defined in agents.yaml.

    Agents are intentionally created without tools here; tools are attached
    in Phase 3 when the full pipeline is wired up.
    """
    config = load_agents_config()
    agents: dict[str, Agent] = {}

    for key in AGENT_KEYS:
        if key not in config:
            raise KeyError(
                f"Expected agent '{key}' not found in config/agents.yaml. "
                f"Available keys: {list(config.keys())}"
            )
        cfg = config[key]
        agents[key] = Agent(
            role=cfg["role"],
            goal=cfg["goal"].strip(),
            backstory=cfg["backstory"].strip(),
            verbose=bool(cfg.get("verbose", True)),
            allow_delegation=bool(cfg.get("allow_delegation", False)),
        )

    return agents
