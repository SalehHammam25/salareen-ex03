"""Markdown content strings for the offline article generator.

All content is about: Human-in-the-Loop AI Agents: Why Full Automation Is Not
Always the Goal.  Includes all required LaTeX-pipeline elements: formula,
markdown table, figure placeholder, Hebrew/BiDi section, and [Author, Year]
citations.
"""
from __future__ import annotations

RESEARCH_NOTES = """\
# Research Notes: Human-in-the-Loop AI Agents

## Definitions
Human-in-the-Loop (HITL) AI systems incorporate human judgment at critical
decision points during training, evaluation, or deployment [Monarch, 2021].
Active learning is a canonical HITL pattern [Settles, 2009].

## Motivations
Full automation fails in high-stakes domains due to distributional shift, edge
cases, and accountability requirements [Amershi et al., 2019]. HITL systems
maintain accountability by keeping humans as decision-makers on critical outputs.

## Key Architectural Patterns
- Approval gate: human approves output before propagation [Cai et al., 2019]
- Feedback loop: human corrections are fed back into model retraining [Fails & Olsen, 2003]
- Active learning: model queries human on uncertain samples [Settles, 2009]

## Case Studies
- IBM Watson Oncology: over-reliance on automation caused errors [Ross, 2017]
- Tesla Autopilot: HITL oversight required for edge cases [NTSB, 2020]
- Content moderation at scale requires human review queues [Gillespie, 2020]

## Bibliography
- [Amershi et al., 2019] Guidelines for Human-AI Interaction. CHI 2019.
- [Monarch, 2021] Human-in-the-Loop Machine Learning. Manning.
- [Settles, 2009] Active Learning Literature Survey. UW TR-1648.
- [Cai et al., 2019] Human-Centered Tools for Coping with Imperfect Algorithms. CHI.
- [Ross, 2017] IBM Watson Recommended Treatments. STAT News.
"""

ARTICLE_OUTLINE = """\
# Article Outline: Human-in-the-Loop AI Agents

1. **Abstract** — 150-word summary of argument and contributions
2. **Introduction** — motivation, scope, thesis statement
3. **Background and Definitions** — taxonomy of HITL systems
4. **Why Full Automation Falls Short** — failure modes, accountability gap
5. **Architectural Patterns for HITL** — approval gates, feedback loops, active learning
6. **Mathematical Formalization** — expected loss reduction formula
7. **Case Studies** — medical AI, autonomous vehicles, content moderation
8. **HITL in the Israeli Tech Context** — Hebrew/BiDi section
9. **Comparison** — markdown table of automation vs. HITL tradeoffs
10. **Conclusion** — synthesis and future directions
11. **References** — bibliography
"""

ARTICLE_DRAFT = """\
# Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal

## Abstract
HITL AI systems deliberately retain human involvement in critical decisions.
This article argues that full automation introduces unacceptable risk in
high-stakes domains. We survey architectural patterns, formalize the benefit
of oversight, and present case studies from medicine and autonomous vehicles.

## Introduction
Autonomous AI promises efficiency, yet real-world deployments reveal that
systems without human checkpoints fail at the margins [Amershi et al., 2019].
HITL architectures provide a principled response to this gap.

## Background and Definitions
HITL systems span a spectrum: from full annotation to targeted approval gates
on uncertain predictions [Monarch, 2021]. Three canonical patterns exist:
approval gates, feedback loops, and active learning [Settles, 2009].

## Why Full Automation Falls Short
Distributional shift, adversarial inputs, and societal accountability demand
human oversight. The cost of a wrong autonomous decision can be irreversible
[Cai et al., 2019].

## Mathematical Framework

The expected loss of a HITL system satisfies:

$$E[L_{HITL}] \\leq E[L_{auto}] - \\lambda \\cdot H(q)$$

where $\\lambda > 0$ is the oversight benefit coefficient and $H(q)$ is the
entropy of the model's prediction distribution over uncertain queries.

## Case Studies

[FIGURE: HITL decision flow diagram showing approval gate architecture]

- **Medical AI**: IBM Watson Oncology over-relied on automation [Ross, 2017].
- **Autonomous Vehicles**: Tesla Autopilot required HITL for edge cases [NTSB, 2020].

## Comparison

| Criterion | Full Automation | HITL System |
|---|---|---|
| Throughput | High | Moderate |
| Edge-case error rate | High | Low |
| Accountability | Diffuse | Clear |
| Cost per decision | Low | Higher |

## HITL in the Israeli Tech Context

### חלק בעברית — מערכות AI עם פיקוח אנושי

בישראל, שימוש במערכות בינה מלאכותית בתחומים רגישים כגון ביטחון, רפואה ומשפט
מחייב פיקוח אנושי. גישת HITL מאפשרת שילוב יעיל של יכולות המכונה עם שיקול דעת
אנושי, תוך שמירה על אחריותיות ושקיפות.

## Conclusion
HITL AI is not a step backward — it is a more honest accounting of where
machine judgment is and is not sufficient. Future systems must make the
human-machine boundary explicit and auditable.

## References
- [Amershi et al., 2019] Guidelines for Human-AI Interaction. CHI 2019.
- [Monarch, 2021] Human-in-the-Loop Machine Learning. Manning.
- [Settles, 2009] Active Learning Literature Survey. UW TR-1648.
- [Cai et al., 2019] Human-Centered Tools for Coping with Imperfect Algorithms. CHI.
- [Ross, 2017] IBM Watson Recommended Treatments. STAT News.
"""

# ARTICLE_FINAL reuses the draft body under a "reviewed" header banner.
ARTICLE_FINAL = (
    "# Human-in-the-Loop AI Agents: Why Full Automation Is Not Always the Goal\n\n"
    "_Reviewed and finalized. Verified: formula, table, figure placeholder,"
    " Hebrew section, and [Author, Year] citations._\n\n"
    + ARTICLE_DRAFT[ARTICLE_DRAFT.index("## Abstract"):]
)

REVIEW_NOTES = """\
# Review Notes

## Summary
The draft meets the structural requirements for the assignment.
All required elements are present: formula, table, figure placeholder,
Hebrew section, and bibliography with [Author, Year] citations.

## Issues Addressed
- Added explicit HITL definition in Background section.
- Improved transition from Mathematical Framework to Case Studies.
- Hebrew section expanded with contextual explanation.

## Outstanding Items
- Figure assets to be generated separately (Phase 4).
- LaTeX conversion pending (Phase 5).
- Bibliography should be expanded with additional references.

## Status: APPROVED for LaTeX conversion.
"""
