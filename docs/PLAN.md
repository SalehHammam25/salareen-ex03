# Implementation Plan

**Project:** salareen-ex03  
**Date:** 2026-06-11  
**Status:** Draft — architecture only, no implementation yet

---

## 1. Proposed Architecture

The system is a **sequential CrewAI pipeline** with 5 specialized agents. Each agent produces a structured output that becomes the input for the next. A shared context dictionary carries state across the crew.

```
┌─────────────────────────────────────────────────────────┐
│                    CrewAI Pipeline                       │
│                                                          │
│  [Research Agent]                                        │
│       │  produces: research_notes.md                     │
│       ▼                                                  │
│  [Outline Agent]                                         │
│       │  produces: article_outline.md                    │
│       ▼                                                  │
│  [Writer Agent]                                          │
│       │  produces: article_draft.md                      │
│       ▼                                                  │
│  [Reviewer Agent]                                        │
│       │  produces: article_final.md + review_notes.md    │
│       ▼                                                  │
│  [LaTeX Agent]                                           │
│       │  produces: latex/main.tex + latex/refs.bib       │
│       ▼                                                  │
│  [xelatex compiler]                                      │
│       │  produces: results/salareen-ex03.pdf             │
└─────────────────────────────────────────────────────────┘
```

---

## 2. Planned CrewAI Agents

### 2.1 Research Agent

| Field | Value |
|---|---|
| Role | Academic Researcher |
| Goal | Collect background knowledge, key concepts, and citations for HITL AI agents |
| Backstory | Expert in AI systems, human-computer interaction, and academic literature |
| Tools | Web search, file writer |
| Output | `results/research_notes.md` |

**Key topics to cover:**
- Definition and taxonomy of HITL systems
- Historical context and motivation
- Architectural patterns (approval gates, feedback loops, active learning)
- Real-world case studies (medical AI, autonomous vehicles, content moderation)
- Failure modes of fully autonomous systems
- Recent literature (2020–2025)

### 2.2 Outline Agent

| Field | Value |
|---|---|
| Role | Academic Editor |
| Goal | Structure the research into a coherent ~15-page article outline |
| Backstory | Senior academic editor with expertise in AI and HCI publications |
| Tools | File reader, file writer |
| Output | `results/article_outline.md` |

**Planned article sections:**
1. Abstract
2. Introduction
3. Background and Definitions
4. Why Full Automation Falls Short
5. Architectural Patterns for HITL
6. Case Studies
7. Mathematical Formalization (includes formula)
8. HITL in the Israeli Tech Context (includes Hebrew/BiDi section)
9. Discussion and Future Directions
10. Conclusion
11. References

### 2.3 Writer Agent

| Field | Value |
|---|---|
| Role | Academic Writer |
| Goal | Write full prose for each section based on the outline and research notes |
| Backstory | PhD-level science writer specializing in AI systems and HCI |
| Tools | File reader, file writer |
| Output | `results/article_draft.md` |

**Notes:**
- Must weave in citations using \cite{} notation (for later LaTeX use)
- Must include Hebrew text for the BiDi section
- Must flag where figures and tables should be inserted

### 2.4 Reviewer Agent

| Field | Value |
|---|---|
| Role | Peer Reviewer |
| Goal | Critique the draft for accuracy, completeness, flow, and academic tone |
| Backstory | Critical academic reviewer with high standards for AI and HCI papers |
| Tools | File reader, file writer |
| Output | `results/article_final.md`, `results/review_notes.md` |

**Review checklist:**
- Academic tone and vocabulary
- Citation completeness
- Section balance and flow
- Factual accuracy of HITL claims
- All required elements present (formula, table, BiDi, figures)

### 2.5 LaTeX Agent

| Field | Value |
|---|---|
| Role | LaTeX Typesetter |
| Goal | Convert the final approved article into well-structured LaTeX source |
| Backstory | Expert in academic LaTeX typesetting, XeLaTeX, and BiDi document formatting |
| Tools | File reader, file writer, LaTeX template loader |
| Output | `latex/main.tex`, `latex/refs.bib` |

**Responsibilities:**
- Apply the LaTeX template (cover, TOC, headers/footers)
- Insert figures at flagged positions
- Format the bibliography
- Ensure XeLaTeX compatibility for Hebrew text

---

## 3. Planned Workflow

```
Phase 1: Architecture & Docs     → This document + PRD + TODO
Phase 2: Agent & Task Skeletons  → src/agents/, src/tasks/ (no LLM calls yet)
Phase 3: Pipeline Integration    → src/pipeline/main.py wires agents into a Crew
Phase 4: Python Figures          → assets/generate_figures.py → assets/*.png
Phase 5: LaTeX Template          → latex/main.tex template + compilation script
Phase 6: End-to-end Run          → Full pipeline run → results/salareen-ex03.pdf
Phase 7: Validation & Cleanup    → Review checklist, final README, submission
```

---

## 4. Module Structure

```
src/
├── __init__.py
├── agents/
│   ├── __init__.py
│   ├── research_agent.py     — ResearchAgent definition
│   ├── outline_agent.py      — OutlineAgent definition
│   ├── writer_agent.py       — WriterAgent definition
│   ├── reviewer_agent.py     — ReviewerAgent definition
│   └── latex_agent.py        — LaTeXAgent definition
├── tasks/
│   ├── __init__.py
│   ├── research_tasks.py     — Tasks for the Research Agent
│   ├── outline_tasks.py      — Tasks for the Outline Agent
│   ├── writer_tasks.py       — Tasks for the Writer Agent
│   ├── reviewer_tasks.py     — Tasks for the Reviewer Agent
│   └── latex_tasks.py        — Tasks for the LaTeX Agent
├── tools/
│   ├── __init__.py
│   ├── file_tools.py         — Read/write helpers
│   └── search_tools.py       — Web search wrapper
└── pipeline/
    ├── __init__.py
    ├── main.py               — Entry point: assembles and runs the Crew
    └── context.py            — Shared context/state dataclass
```

---

## 5. Data Flow

```
config/agents.yaml  ──┐
config/tasks.yaml   ──┤──> pipeline/main.py
.env (API keys)     ──┘
                          │
                          ▼
                    ResearchAgent
                          │ research_notes.md
                          ▼
                    OutlineAgent
                          │ article_outline.md
                          ▼
                    WriterAgent
                          │ article_draft.md
                          ▼
                    ReviewerAgent
                          │ article_final.md
                          ▼
                    LaTeXAgent
                          │ latex/main.tex + latex/refs.bib
                          ▼
                    xelatex (subprocess)
                          │
                          ▼
                  results/salareen-ex03.pdf
```

---

## 6. Risk Analysis

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| LLM generates inaccurate citations | High | High | Reviewer Agent validates; manually verify bibliography |
| Hebrew/BiDi rendering broken in LaTeX | Medium | High | Test XeLaTeX + polyglossia setup early (Phase 5) |
| Generated article is too short (<15 pages) | Medium | Medium | Writer Agent prompted with explicit length targets per section |
| LaTeX compilation errors from generated code | Medium | High | LaTeX Agent uses a validated template; errors caught in Phase 6 |
| API rate limits or cost overruns | Low | Medium | Use smaller models for draft; run pipeline incrementally |
| File encoding issues (Hebrew text on Windows) | Medium | Medium | Enforce UTF-8 throughout; test on Windows early |

---

## 7. Validation Plan

1. **Unit tests** (`tests/`) — test each agent's output format in isolation with mocked LLM responses.
2. **Integration test** — run the full pipeline end-to-end on a short article (~3 pages) before the final run.
3. **Manual review** — read the generated `article_final.md` and verify all required elements are present.
4. **LaTeX compilation check** — `xelatex` must exit with code 0 and produce a non-empty PDF.
5. **PDF visual review** — open the PDF, verify cover page, TOC, figures, BiDi section, and bibliography.
6. **Submission checklist** — run through all acceptance criteria in `docs/PRD.md` before submission.
