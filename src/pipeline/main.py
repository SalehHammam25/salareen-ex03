"""Phase 3 pipeline entry point — registered as the 'run-pipeline' script.

Usage
-----
Show expected output paths, no LLM calls:
    uv run run-pipeline --dry-run

Report which output files are present / missing:
    uv run run-pipeline --check-outputs

Run the full pipeline (requires API keys in .env):
    uv run run-pipeline
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any, Callable

from dotenv import load_dotenv  # top-level so tests can patch it

from src.pipeline.article_pipeline import (
    expected_output_paths,
    run_article_pipeline,
    validate_expected_outputs,
)


def _missing_api_keys() -> list[str]:
    return [k for k in ("OPENAI_API_KEY", "ANTHROPIC_API_KEY") if not os.environ.get(k)]


def _print_output_paths() -> None:
    print("Expected output files (from config/tasks.yaml):")
    for p in expected_output_paths():
        print(f"  {p}")
    print()


def cmd_dry_run() -> None:
    result = run_article_pipeline(dry_run=True)
    print("\n=== DRY RUN — article pipeline ===\n")
    _print_output_paths()
    n_present = len(result.state.present)
    n_total = n_present + len(result.state.missing)
    print(f"Outputs present: {n_present}/{n_total}")
    print("No LLM calls were made.\n")


def cmd_check_outputs() -> None:
    state = validate_expected_outputs()
    print("\n=== OUTPUT CHECK ===\n")
    if state.present:
        print(f"Present ({len(state.present)}):")
        for p in state.present:
            print(f"  [OK]  {p}")
    if state.missing:
        print(f"Missing ({len(state.missing)}):")
        for p in state.missing:
            print(f"  [--]  {p}")
    print()
    print("Complete." if state.is_complete else "Pipeline outputs incomplete.")
    print()


def cmd_run(crew_factory: Callable[[], Any] | None = None) -> None:
    load_dotenv()
    missing = _missing_api_keys()
    if missing:
        print(
            f"[ERROR] Missing API keys: {', '.join(missing)}\n"
            "  Copy .env-example to .env and add your credentials."
        )
        sys.exit(1)

    print("[INFO] Starting article generation pipeline…\n")
    result = run_article_pipeline(dry_run=False, crew_factory=crew_factory)

    n_present = len(result.state.present)
    n_total = n_present + len(result.state.missing)
    print(f"\n[DONE] Pipeline finished. Outputs present: {n_present}/{n_total}")
    if result.state.missing:
        print("  Still missing:")
        for p in result.state.missing:
            print(f"    {p}")
    if result.kickoff_result:
        print(f"\n{result.kickoff_result}")


def main(
    argv: list[str] | None = None,
    crew_factory: Callable[[], Any] | None = None,
) -> None:
    """Parse *argv* (defaults to sys.argv) and dispatch to the right command."""
    parser = argparse.ArgumentParser(
        prog="run-pipeline",
        description="salareen-ex03: article generation pipeline",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print expected output paths and current file state; no LLM calls.",
    )
    parser.add_argument(
        "--check-outputs",
        action="store_true",
        help="Report which expected output files are present or missing.",
    )
    args = parser.parse_args(argv)

    if args.dry_run:
        cmd_dry_run()
    elif args.check_outputs:
        cmd_check_outputs()
    else:
        cmd_run(crew_factory=crew_factory)


if __name__ == "__main__":
    main()
