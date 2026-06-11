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
