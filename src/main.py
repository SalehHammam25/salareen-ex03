"""Pipeline entry point.

Usage
-----
Inspect configuration without LLM calls:
    uv run python -m src.main --dry-run

Run the full pipeline (requires API keys in .env):
    uv run python -m src.main
"""

from __future__ import annotations

import argparse
import os
import sys


def _missing_api_keys() -> list[str]:
    return [k for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY") if not os.environ.get(k)]


def dry_run() -> None:
    """Print a human-readable summary of all agents and tasks without calling any LLM."""
    from src.agents.factory import create_agents
    from src.tasks.factory import create_tasks

    print("\n=== DRY RUN — salareen-ex03 pipeline ===\n")

    agents = create_agents()
    print(f"Agents ({len(agents)} configured):")
    for key, agent in agents.items():
        goal_preview = agent.goal[:90].replace("\n", " ")
        print(f"  [{key}]")
        print(f"    Role : {agent.role}")
        print(f"    Goal : {goal_preview}...")
        print()

    tasks = create_tasks(agents)
    print(f"Tasks ({len(tasks)} total, sequential order):")
    for i, task in enumerate(tasks, 1):
        ctx_names = [t.name for t in (task.context or [])]
        ctx_str = f"  depends on: {', '.join(ctx_names)}" if ctx_names else "  (no dependencies)"
        out_str = task.output_file or "(in-memory only)"
        expected_preview = task.expected_output[:90].replace("\n", " ")
        print(f"  {i}. {task.name}")
        print(f"     Agent  : {task.agent.role}")
        print(f"     Output : {out_str}")
        print(f"     Expects: {expected_preview}...")
        print(f"    {ctx_str}")
        print()

    print("=== Config is valid. No LLM calls were made. ===\n")


def run_pipeline() -> None:
    """Run the full CrewAI pipeline. Requires API keys in the environment."""
    from dotenv import load_dotenv
    load_dotenv()

    missing = _missing_api_keys()
    if missing:
        print(
            f"[ERROR] No API keys found. Missing: {', '.join(missing)}\n"
            "  Copy .env-example to .env and add your credentials, then retry."
        )
        sys.exit(1)

    from src.pipeline.crew_builder import build_crew

    print("[INFO] Building crew…")
    crew = build_crew(verbose=True)
    print(f"[INFO] Crew ready — {len(crew.agents)} agents, {len(crew.tasks)} tasks.")
    print("[INFO] Starting pipeline (LLM calls will be made)…\n")

    result = crew.kickoff()

    print("\n[DONE] Pipeline complete.")
    print(result)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="src.main",
        description="salareen-ex03: Human-in-the-Loop article generation pipeline",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print pipeline configuration without making any LLM API calls.",
    )
    args = parser.parse_args()

    if args.dry_run:
        dry_run()
    else:
        run_pipeline()


if __name__ == "__main__":
    main()
