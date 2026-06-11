# TODO — salareen-ex03

**Project:** Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal  
**Last updated:** 2026-06-11

Status legend: `[ ]` = not started, `[~]` = in progress, `[x]` = done

---

## Phase 1: Documentation and Architecture

- [x] Create project skeleton and folder structure
- [x] Write `README.md` with full project overview
- [x] Write `docs/PRD.md` — product requirements
- [x] Write `docs/PLAN.md` — architecture and agent design
- [x] Write `docs/TODO.md` — this file
- [x] Write `docs/PROMPT_LOG.md` — first entry
- [x] Create `pyproject.toml` with planned dependencies
- [x] Create `.env-example`
- [ ] Review all docs with team member (Areen)
- [ ] Finalize agent roles and task descriptions in `config/agents.yaml` and `config/tasks.yaml`

---

## Phase 2: CrewAI Agents and Tasks

- [ ] Implement `src/agents/research_agent.py`
- [ ] Implement `src/agents/outline_agent.py`
- [ ] Implement `src/agents/writer_agent.py`
- [ ] Implement `src/agents/reviewer_agent.py`
- [ ] Implement `src/agents/latex_agent.py`
- [ ] Implement `src/tasks/research_tasks.py`
- [ ] Implement `src/tasks/outline_tasks.py`
- [ ] Implement `src/tasks/writer_tasks.py`
- [ ] Implement `src/tasks/reviewer_tasks.py`
- [ ] Implement `src/tasks/latex_tasks.py`
- [ ] Implement `src/tools/file_tools.py`
- [ ] Implement `src/tools/search_tools.py`
- [ ] Implement `src/pipeline/context.py`
- [ ] Add unit tests for agent/task output schemas in `tests/`

---

## Phase 3: Article Generation Pipeline

- [ ] Implement `src/pipeline/main.py` — crew assembly and execution
- [ ] Load agent/task configs from `config/agents.yaml` and `config/tasks.yaml`
- [ ] Test Research Agent independently — produces `results/research_notes.md`
- [ ] Test Outline Agent — produces `results/article_outline.md`
- [ ] Test Writer Agent — produces `results/article_draft.md`
- [ ] Test Reviewer Agent — produces `results/article_final.md`
- [ ] Test end-to-end pipeline for a short 3-page article
- [ ] Log all agent outputs to `results/`

---

## Phase 4: Python Graph and Table Generation

- [ ] Create `assets/generate_figures.py`
- [ ] Generate at least one matplotlib/seaborn figure (e.g., HITL decision flow, accuracy comparison)
- [ ] Save figures as `assets/hitl_figure_1.png` (and others as needed)
- [ ] Verify figures render correctly and have appropriate labels/titles
- [ ] Ensure figure generation is deterministic (set random seeds if applicable)

---

## Phase 5: LaTeX PDF Generation

- [ ] Create `latex/main.tex` with full document structure
- [ ] Create `latex/refs.bib` with bibliography entries
- [ ] Configure XeLaTeX preamble: `polyglossia`, `fontspec`, Hebrew/BiDi support
- [ ] Set up document class with headers and footers
- [ ] Add cover page in LaTeX
- [ ] Add table of contents
- [ ] Add figure inclusion commands for `assets/` images
- [ ] Add table environment
- [ ] Add mathematical formula
- [ ] Add Hebrew/BiDi section using `polyglossia` and `bidi`
- [ ] Add bibliography with `\cite{}` references
- [ ] Test compilation: `xelatex latex/main.tex` exits cleanly
- [ ] Verify PDF visual output: cover, TOC, figures, BiDi, bibliography
- [ ] Output final PDF to `results/salareen-ex03.pdf`

---

## Phase 6: Validation, README, and Final Submission

- [ ] Run full end-to-end pipeline: article generation + PDF compilation
- [ ] Complete all acceptance criteria from `docs/PRD.md`
- [ ] Final visual review of `results/salareen-ex03.pdf`
- [ ] Update `README.md` with actual setup and usage instructions
- [ ] Update `docs/PROMPT_LOG.md` with all prompts used during development
- [ ] Confirm no secrets in any committed files
- [ ] Confirm all source files are under 150 lines
- [ ] Run all tests: `uv run pytest`
- [ ] Final git commit and push
- [ ] Submit `salareen-ex03.pdf` on Moodle
