# TODO — salareen-ex03

**Project:** Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal  
**Last updated:** 2026-06-11 (Phase 2 complete)

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
- [x] Review all docs with team member (Areen)
- [x] Finalize agent roles and task descriptions in `config/agents.yaml` and `config/tasks.yaml`

---

## Phase 2: CrewAI Agents and Tasks

> Architecture decision: agents and tasks are config-driven (YAML → factory functions)
> rather than one file per agent. This keeps the code lean and under 150 lines/file.

- [x] Implement `src/tools/config_loader.py` — YAML loader with validation
- [x] Implement `src/agents/factory.py` — creates all 5 Agent objects from agents.yaml
- [x] Implement `src/tasks/factory.py` — creates all 5 Task objects with sequential context
- [x] Implement `src/pipeline/crew_builder.py` — assembles the Crew
- [x] Implement `src/main.py` — `--dry-run` and normal run modes
- [x] Add `tests/test_config_loader.py` — 8 tests, no API calls
- [x] Add `tests/test_pipeline_dry_run.py` — 11 tests, no API calls
- [x] All 19 tests passing (`uv run pytest`)
- [x] Dry-run verified: `uv run python -m src.main --dry-run`
- [x] Implement `src/tools/file_tools.py` — file read/write helpers
- [x] Implement `src/tools/search_tools.py` — web search wrapper

---

## Phase 3: Article Generation Pipeline

- [x] Implement `src/pipeline/article_pipeline.py` — expected_output_paths, validate_expected_outputs, run_article_pipeline (injectable crew_factory; 59 tests passing)
- [x] Implement `src/pipeline/main.py` — `--dry-run`, `--check-outputs`, normal run; registered as `run-pipeline` entry point (73 tests passing)
- [x] Load agent/task configs from `config/agents.yaml` and `config/tasks.yaml`
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
