"""Assemble the CrewAI Crew from agents and tasks."""

from __future__ import annotations

from crewai import Crew, Process

from src.agents.factory import create_agents
from src.tasks.factory import create_tasks


def build_crew(verbose: bool = True) -> Crew:
    """Build and return the configured sequential CrewAI Crew.

    All five agents are created from config/agents.yaml and all five tasks
    from config/tasks.yaml.  The pipeline runs sequentially so each agent
    can read the output of the previous one.
    """
    agents = create_agents()
    tasks = create_tasks(agents)

    return Crew(
        agents=list(agents.values()),
        tasks=tasks,
        process=Process.sequential,
        verbose=verbose,
    )
