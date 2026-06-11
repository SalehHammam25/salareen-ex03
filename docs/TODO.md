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
- [x] Implement `src/pipeline/main.py` — `--dry-run`, `--check-outputs`, `--offline-generate`, normal run; registered as `run-pipeline` entry point (96 tests passing)
- [x] Load agent/task configs from `config/agents.yaml` and `config/tasks.yaml`
- [x] Implement `src/pipeline/offline_content.py` + `offline_templates.py` — deterministic offline markdown generation (no API keys needed)
- [x] `results/research_notes.md` — produced via `--offline-generate`; includes [Author, Year] citations and bibliography
- [x] `results/article_outline.md` — produced via `--offline-generate`; numbered sections through Conclusion
- [x] `results/article_draft.md` — produced via `--offline-generate`; includes formula, table, [FIGURE:…] placeholder, Hebrew BiDi section
- [x] `results/article_final.md` — produced via `--offline-generate`; reviewed/finalized version of draft
- [x] `results/review_notes.md` — produced via `--offline-generate` (bonus file, not in tasks.yaml output_file)
- [ ] Real CrewAI end-to-end run (requires API keys) — produces same files via LLM agents
- [ ] Test end-to-end pipeline with real agents
- [x] Log all agent outputs to `results/` (offline mode; real-agent outputs pending)

---

## Phase 4: Python Graph and Table Generation

- [x] Create `assets/generate_figures.py` — matplotlib only, Agg backend, pathlib, all under 150 lines
- [x] Generate `assets/hitl_decision_flow.png` — confidence-based routing flow diagram (57 KB)
- [x] Generate `assets/automation_risk_tradeoff.png` — grouped bar chart, risk by domain (40 KB)
- [x] Generate `assets/hitl_comparison_table.csv` — 7-row comparison table (214 bytes)
- [x] Figures have clear titles, axis labels, and readable layout
- [x] Generation is deterministic (fixed data, no random elements; CSV byte-identical across runs)
- [x] Add `tests/test_generate_figures.py` — 18 tests; verifies PNG signature, size, CSV header/rows, determinism (114 tests total passing)

---

## Phase 5: LaTeX PDF Generation

- [x] Create `latex/main.tex` with full document structure (via `src/pipeline/latex_builder.py`)
- [x] Create `latex/refs.bib` with bibliography entries
- [x] Configure XeLaTeX preamble: `polyglossia`, `fontspec`, Hebrew/BiDi support
- [x] Set up document class with headers and footers
- [x] Add cover page in LaTeX (`\maketitle`)
- [x] Add table of contents (`\tableofcontents`)
- [x] Add figure inclusion commands for `assets/` images (hitl_decision_flow, automation_risk_tradeoff)
- [x] Add table environment (`\begin{tabular}`)
- [x] Add mathematical formula (`\begin{equation}` with HITL loss bound)
- [x] Add Hebrew/BiDi section using `\begin{otherlanguage}{hebrew}`
- [x] Add bibliography with `\cite{}` references and `\bibliography{refs}`
- [x] Add `--build-latex` CLI flag to `run-pipeline` (137 tests passing)
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
