# Prompt Log — salareen-ex03

This file documents every significant prompt used to drive development of this project.
It serves as an audit trail for the assignment and enables reproducibility.

---

## Entry 001 — Project Skeleton and Planning

**Date:** 2026-06-11  
**Phase:** Phase 1 — Documentation and Architecture  
**Author:** Saleh Hammam  
**Tool:** Claude Code (claude-sonnet-4-6)

### Purpose

Initialize the project repository with a professional skeleton and all planning documents before any implementation begins.

### Prompt Summary

> We are starting Homework Assignment 03 for an AI Agents Architecture course.
>
> Project identity: Group code `salareen`, Homework `ex03`, Topic: "Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal", Students: Saleh Hammam and Areen Tarabeh.
>
> Build a CrewAI-based multi-agent system that generates an academic-style article of about 15 pages, then produces a polished PDF using LaTeX.
>
> Do NOT implement the full project yet. Create only the initial professional project skeleton and planning documents, including: `README.md`, `docs/PRD.md`, `docs/PLAN.md`, `docs/TODO.md`, `docs/PROMPT_LOG.md`, `pyproject.toml`, `.env-example`, and placeholder folders/files for `src/`, `latex/`, `assets/`, `results/`, `config/`, `tests/`.

### Files Created / Modified

| File | Action |
|---|---|
| `README.md` | Updated with full project overview, architecture, structure |
| `docs/PRD.md` | Created — problem statement, goals, requirements, acceptance criteria |
| `docs/PLAN.md` | Created — architecture, 5 agents, workflow, data flow, risks |
| `docs/TODO.md` | Created — 6-phase task checklist |
| `docs/PROMPT_LOG.md` | Created — this file |
| `pyproject.toml` | Created — project metadata and planned dependencies |
| `.env-example` | Created — API key placeholders |
| `src/__init__.py` | Created — placeholder |
| `src/agents/__init__.py` | Created — placeholder |
| `src/tasks/__init__.py` | Created — placeholder |
| `src/tools/__init__.py` | Created — placeholder |
| `src/pipeline/__init__.py` | Created — placeholder |
| `config/agents.yaml` | Created — placeholder YAML |
| `config/tasks.yaml` | Created — placeholder YAML |
| `latex/.gitkeep` | Created — preserves empty folder in git |
| `assets/.gitkeep` | Created — preserves empty folder in git |
| `results/.gitkeep` | Created — preserves empty folder in git |
| `tests/__init__.py` | Created — placeholder |

### Key Decisions Recorded

- **XeLaTeX** chosen over pdflatex for Hebrew/BiDi support via `polyglossia` + `bidi`.
- **Sequential crew** chosen over hierarchical for simplicity and traceability at this stage.
- **uv** chosen as the package manager (Windows-friendly, fast).
- **Python 3.11+** required for modern type hint syntax used in CrewAI.
- **No real API keys** to be committed; `.env-example` provides the template.

---

<!-- Add new entries below this line in the same format -->

---

## Entry 002 — Phase 2: CrewAI Pipeline Foundation

**Date:** 2026-06-11  
**Phase:** Phase 2 — CrewAI Agents and Tasks  
**Author:** Saleh Hammam  
**Tool:** Claude Code (claude-sonnet-4-6)

### Purpose

Implement the minimal but professional CrewAI pipeline foundation: config loading, agent factory, task factory, crew builder, main entry point, and a full test suite — all without triggering real LLM calls.

### Prompt Summary

> Implement Phase 2 only. Create: config loader (`src/tools/config_loader.py`), agent factory (`src/agents/factory.py`), task factory (`src/tasks/factory.py`), pipeline builder (`src/pipeline/crew_builder.py`), main entry point (`src/main.py`) with `--dry-run` mode, and two test files. Update README, TODO, and PROMPT_LOG. Do NOT generate the article or PDF.

### Files Created / Modified

| File | Action |
|---|---|
| `src/tools/config_loader.py` | Created — YAML loader with `ConfigError` validation |
| `src/agents/factory.py` | Created — `create_agents()` factory from agents.yaml |
| `src/tasks/factory.py` | Created — `create_tasks()` factory with sequential context chaining |
| `src/pipeline/crew_builder.py` | Created — `build_crew()` assembles Crew with sequential Process |
| `src/main.py` | Created — `--dry-run` (no LLM) and normal run (requires API keys) |
| `tests/test_config_loader.py` | Created — 8 tests: happy path + error paths with monkeypatching |
| `tests/test_pipeline_dry_run.py` | Created — 11 tests: factory assertions + dry-run integration |
| `README.md` | Updated — real setup/usage/test commands |
| `docs/TODO.md` | Updated — Phase 1 complete, Phase 2 complete |
| `docs/PROMPT_LOG.md` | Updated — this entry |

### Key Decisions Recorded

- **Config-driven factory pattern** chosen over one-file-per-agent: keeps every file under 150 lines and centralizes agent/task parameters in YAML.
- **Sequential context chaining**: each task receives all preceding tasks as `context`, so later agents (Writer, Reviewer) can read earlier outputs.
- **`--dry-run` mode** constructs all Agent and Task objects (no LLM calls) and prints a readable pipeline summary.
- **CrewAI version**: 1.14.6 — `Task.output_file` and `Task.context` both exist; `Process.sequential` confirmed.
- **Python version on this machine**: 3.13.9 (despite `requires-python = ">=3.11"`).
- **19/19 tests pass** with zero API calls required.

---

## Entry 003 - Documentation Update and Final Review

**Date:** 2026-06-11  
**Phase:** Documentation, prompt log, and final validation  
**Author:** Areen Tarabeh  
**Tool:** Codex / ChatGPT

### Purpose

Update the project documentation after the latest implementation was pushed, while avoiding code conflicts by editing documentation files only.

### Prompt Summary

> I finished and pushed the latest code. Please pull the latest repo and work only on documentation so we avoid conflicts. Update README.md with setup and run instructions, update docs/PROMPT_LOG.md with the prompts/workflow we used, add a short contribution section, run tests, commit, and push.

### Files Created / Modified

| File | Action |
|---|---|
| README.md | Updated with contribution section and verified setup/run/test instructions |
| docs/PROMPT_LOG.md | Updated with Areen documentation workflow entry |

### Key Decisions Recorded

- Worked only on README.md and docs/PROMPT_LOG.md to reduce merge conflicts with implementation changes.
- Verified setup and test flow: plain uv sync installs runtime dependencies, while tests require uv sync --extra dev before uv run pytest.
- Recorded team contributions clearly: Saleh handled implementation, testing, pipeline, LaTeX/figures; Areen handled documentation, prompt log, review, and final validation.
- Ran the test suite before committing the documentation update.
