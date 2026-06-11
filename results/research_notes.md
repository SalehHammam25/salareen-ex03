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
