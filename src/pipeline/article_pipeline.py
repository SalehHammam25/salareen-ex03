"""Article generation pipeline — thin orchestration layer over CrewAI.

Provides three public helpers:
    expected_output_paths()       — list of output Paths from tasks.yaml
    validate_expected_outputs()   — PipelineState (present / missing)
    run_article_pipeline()        — kick off (or skip) the crew
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

from src.tasks.factory import TASK_ORDER
from src.tools.config_loader import load_tasks_config

_PROJECT_ROOT = Path(__file__).parent.parent.parent


@dataclass
class PipelineState:
    present: list[Path]
    missing: list[Path]

    @property
    def is_complete(self) -> bool:
        return len(self.missing) == 0


@dataclass
class PipelineResult:
    dry_run: bool
    state: PipelineState
    kickoff_result: Any = field(default=None)


def expected_output_paths(base_dir: Path | None = None) -> list[Path]:
    """Return the output file Paths declared in config/tasks.yaml, in pipeline order.

    Args:
        base_dir: Root directory for resolving relative output_file paths.
                  Defaults to the project root.  Pass tmp_path in tests.
    """
    root = Path(base_dir) if base_dir is not None else _PROJECT_ROOT
    config = load_tasks_config()
    paths: list[Path] = []
    for key in TASK_ORDER:
        output_file = config[key].get("output_file")
        if output_file:
            paths.append(root / output_file)
    return paths


def validate_expected_outputs(
    paths: list[Path] | None = None,
    base_dir: Path | None = None,
) -> PipelineState:
    """Return a PipelineState describing which expected output files exist.

    Args:
        paths:    Explicit list of Paths to check.  If None, uses
                  expected_output_paths(base_dir).
        base_dir: Forwarded to expected_output_paths when paths is None.
    """
    if paths is None:
        paths = expected_output_paths(base_dir=base_dir)
    present = [p for p in paths if p.exists()]
    missing = [p for p in paths if not p.exists()]
    return PipelineState(present=present, missing=missing)


def run_article_pipeline(
    dry_run: bool = False,
    crew_factory: Callable[[], Any] | None = None,
) -> PipelineResult:
    """Run (or skip) the article-generation CrewAI pipeline.

    Args:
        dry_run:      If True, validate current file state and return without
                      calling kickoff — no LLM calls are made.
        crew_factory: Zero-argument callable that returns a crew object with a
                      .kickoff() method.  If None, defaults to build_crew().
                      Inject a fake in tests to avoid real API calls.
    """
    if dry_run:
        return PipelineResult(dry_run=True, state=validate_expected_outputs())

    if crew_factory is None:
        from src.pipeline.crew_builder import build_crew
        crew_factory = build_crew

    crew = crew_factory()
    kickoff_result = crew.kickoff()
    return PipelineResult(
        dry_run=False,
        state=validate_expected_outputs(),
        kickoff_result=kickoff_result,
    )
