# salareen-ex03

**Homework Assignment 03 — AI Agents Architecture Course**

| Field | Value |
|---|---|
| Group code | salareen |
| Students | Saleh Hammam, Areen Tarabeh |
| Submission file | `salareen-ex03.pdf` |
| Course | AI Agents Architecture |

---

## Topic

**Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal**

An academic-style article (~15 pages) exploring the theoretical basis, practical benefits, and architectural patterns of Human-in-the-Loop (HITL) systems in modern AI agent pipelines.

---

## Assignment Goal

Build a **CrewAI-based multi-agent system** that:

1. Researches and drafts a full academic article on the HITL topic.
2. Structures the article with proper academic formatting.
3. Generates supporting figures and tables via Python code.
4. Compiles the final document to a polished PDF using LaTeX.

---

## Planned Architecture

```
User
 └─> CrewAI Pipeline (src/)
       ├── Research Agent     — collects background, sources, key concepts
       ├── Outline Agent      — structures the article into sections
       ├── Writer Agent       — drafts each section in full
       ├── Reviewer Agent     — critiques and refines the draft
       └── LaTeX Agent        — converts the approved draft into LaTeX
                                and triggers PDF compilation
```

Agents share a common context object. The pipeline is sequential with optional human-in-the-loop checkpoints before each major stage.

---

## Required Article Elements

- Cover page
- Table of contents
- Multiple chapters/sections with headers and footers
- At least one image (`assets/`)
- At least one Python-generated graph (`assets/`)
- At least one table
- At least one mathematical formula
- A section with Hebrew-English BiDi text
- Bibliography with linked citations

---

## Project Structure

```
salareen-ex03/
├── README.md
├── pyproject.toml
├── .env-example
├── .gitignore
│
├── docs/
│   ├── PRD.md          — Product Requirements Document
│   ├── PLAN.md         — Architecture and implementation plan
│   ├── TODO.md         — Phased task checklist
│   └── PROMPT_LOG.md   — Log of all prompts used in development
│
├── src/
│   ├── agents/         — CrewAI agent definitions
│   ├── tasks/          — Task definitions per agent
│   ├── tools/          — Custom tools (web search, file I/O, etc.)
│   └── pipeline/       — Orchestration and crew assembly
│
├── latex/              — LaTeX source files (.tex, .bib, style files)
│
├── assets/             — Images and Python-generated figures
│
├── results/            — Generated outputs (article drafts, final PDF)
│
├── config/             — YAML configuration for agents and tasks
│
└── tests/              — Unit and integration tests
```

---

## Setup Instructions

> Full setup instructions will be added after the implementation phase.

**Prerequisites (planned):**
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) package manager
- A LaTeX distribution (MiKTeX or TeX Live) with `xelatex`
- API key for OpenAI or Anthropic (see `.env-example`)

**Install (planned):**
```powershell
uv sync
copy .env-example .env
# Edit .env with your real API keys
```

---

## Usage Instructions

> Will be completed after implementation.

```powershell
# Run the full pipeline
uv run python -m src.pipeline.main

# Compile LaTeX manually
xelatex latex/main.tex
```

---

## Submission Notes

- Final Moodle submission filename: `salareen-ex03.pdf`
- The PDF is generated inside `results/` and should be copied/renamed for submission.
- No API keys or secrets should be committed — use `.env-example` only.
