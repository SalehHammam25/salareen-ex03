"""Create CrewAI Task objects from config/tasks.yaml."""

from __future__ import annotations

from crewai import Task

from src.tools.config_loader import load_tasks_config

# Pipeline execution order — each task feeds into the next.
TASK_ORDER: list[str] = [
    "research_task",
    "outline_task",
    "writer_task",
    "reviewer_task",
    "latex_task",
]

# Maps task key → which agent (key) is responsible for it.
TASK_AGENT_MAP: dict[str, str] = {
    "research_task": "research_agent",
    "outline_task": "outline_agent",
    "writer_task": "writer_agent",
    "reviewer_task": "reviewer_agent",
    "latex_task": "latex_agent",
}


def create_tasks(agents: dict) -> list[Task]:
    """Return an ordered list of Tasks wired to their agents.

    Each task receives all preceding tasks as `context` so its agent
    can read prior outputs during execution.

    Args:
        agents: Dict returned by ``src.agents.factory.create_agents``.
    """
    config = load_tasks_config()
    tasks: list[Task] = []

    for key in TASK_ORDER:
        if key not in config:
            raise KeyError(
                f"Expected task '{key}' not found in config/tasks.yaml. "
                f"Available keys: {list(config.keys())}"
            )
        cfg = config[key]
        agent_key = TASK_AGENT_MAP[key]

        if agent_key not in agents:
            raise KeyError(
                f"Task '{key}' requires agent '{agent_key}', "
                f"but it was not found in the agents dict."
            )

        task = Task(
            name=key,
            description=cfg["description"].strip(),
            expected_output=cfg["expected_output"].strip(),
            agent=agents[agent_key],
            context=list(tasks),          # all preceding task outputs
            output_file=cfg.get("output_file"),
        )
        tasks.append(task)

    return tasks
