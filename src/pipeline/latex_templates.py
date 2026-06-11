"""XeLaTeX template strings for the HITL article (Phase 5).

MAIN_TEX — complete XeLaTeX source with polyglossia, bidi, formula, table,
           two figures, Hebrew section, and bibliography.
REFS_BIB  — BibTeX bibliography for all cite{} keys used in MAIN_TEX.
"""
from __future__ import annotations

MAIN_TEX = r"""\documentclass[12pt,a4paper]{article}
\usepackage{fontspec}
\usepackage{polyglossia}
\setmainlanguage{english}
\setotherlanguage{hebrew}
\usepackage{bidi}
\usepackage[a4paper,margin=2.5cm]{geometry}
\usepackage{fancyhdr}
\pagestyle{fancy}\fancyhf{}
\rhead{HITL AI Agents}\lhead{salareen-ex03}\cfoot{\thepage}
\usepackage{graphicx}
\usepackage{booktabs}
\usepackage{amsmath}
\usepackage[colorlinks=true,linkcolor=blue,citecolor=blue]{hyperref}
\title{Human-in-the-Loop AI Agents:\\
       Why Full Automation Is Not Always the Goal}
\author{Saleh Hammam \and Areen Tarabeh}
\date{\today}
\begin{document}
\maketitle\thispagestyle{empty}\newpage
\tableofcontents\newpage
\section{Abstract}
Human-in-the-Loop (HITL) AI systems retain human involvement at critical
decision points. This article argues that full automation introduces
unacceptable risk in high-stakes domains. We survey architectural patterns,
formalize the benefit of oversight, and present real-world case studies.
\section{Introduction}
Autonomous AI promises efficiency, yet systems without human checkpoints
fail at the margins \cite{amershi2019guidelines}.
HITL architectures provide a principled response \cite{monarch2021human}.
\section{Background and Definitions}
HITL systems span a spectrum from full annotation to targeted approval
gates \cite{monarch2021human}. Canonical patterns include approval gates,
feedback loops, and active learning \cite{settles2009active}.
\section{Why Full Automation Falls Short}
Distributional shift and accountability gaps demand oversight. A wrong
autonomous decision can be irreversible \cite{cai2019human}.
\section{Mathematical Framework}
The expected loss of a HITL system satisfies:
\begin{equation}
  E\!\left[L_{\mathrm{HITL}}\right] \leq
  E\!\left[L_{\mathrm{auto}}\right] - \lambda \cdot H(q)
  \label{eq:hitl_loss}
\end{equation}
where $\lambda>0$ is the oversight benefit coefficient and $H(q)$ is the
entropy of the model's prediction distribution over uncertain queries.
\section{Case Studies}
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{../assets/hitl_decision_flow.png}
  \caption{HITL Decision Flow: Confidence-Based Routing}
  \label{fig:hitl_flow}
\end{figure}
IBM Watson Oncology over-relied on automation \cite{ross2017ibm}; Tesla
Autopilot required HITL oversight for edge cases \cite{ntsb2020tesla}.
\begin{figure}[htbp]
  \centering
  \includegraphics[width=0.85\textwidth]{../assets/automation_risk_tradeoff.png}
  \caption{Risk Score: Full Automation vs.\ HITL by Domain}
  \label{fig:risk}
\end{figure}
\section{Comparison}
\begin{table}[htbp]
\centering
\begin{tabular}{lcc}
\toprule
Criterion & Full Automation & HITL System \\
\midrule
Throughput           & High    & Moderate \\
Edge-case error rate & High    & Low      \\
Accountability       & Diffuse & Clear    \\
Cost per decision    & Low     & Higher   \\
Auditability         & Poor    & Strong   \\
\bottomrule
\end{tabular}
\caption{Comparison: Full Automation vs.\ HITL Systems}
\label{tab:comparison}
\end{table}
\section{HITL in the Israeli Tech Context}
\begin{otherlanguage}{hebrew}
\subsection*{מערכות AI עם פיקוח אנושי}
בישראל, שימוש במערכות בינה מלאכותית בתחומים רגישים כגון ביטחון, רפואה
ומשפט מחייב פיקוח אנושי. גישת HITL מאפשרת שילוב יעיל של יכולות המכונה
עם שיקול דעת אנושי, תוך שמירה על אחריותיות ושקיפות.
\end{otherlanguage}
\section{Conclusion}
HITL AI is not a step backward --- it is a more honest accounting of where
machine judgment is and is not sufficient. Future systems must make the
human-machine boundary explicit and auditable.
\bibliographystyle{plain}
\bibliography{refs}
\end{document}
"""

REFS_BIB = """\
@article{amershi2019guidelines,
  author  = {Amershi, Saleema and others},
  title   = {Software Engineering for Machine Learning: A Case Study},
  journal = {Proceedings of CHI},
  year    = {2019}
}
@book{monarch2021human,
  author    = {Monarch, Robert Munro},
  title     = {Human-in-the-Loop Machine Learning},
  publisher = {Manning Publications},
  year      = {2021}
}
@techreport{settles2009active,
  author      = {Settles, Burr},
  title       = {Active Learning Literature Survey},
  institution = {University of Wisconsin--Madison},
  number      = {TR-1648},
  year        = {2009}
}
@inproceedings{cai2019human,
  author    = {Cai, Carrie and others},
  title     = {Human-Centered Tools for Coping with Imperfect Algorithms},
  booktitle = {Proceedings of CHI},
  year      = {2019}
}
@article{ross2017ibm,
  author  = {Ross, Casey and Swetlitz, Ike},
  title   = {{IBM} Watson and Cancer Care},
  journal = {{STAT} News},
  year    = {2017}
}
@misc{ntsb2020tesla,
  author = {{NTSB}},
  title  = {Automated Vehicle Collision Investigation},
  year   = {2020}
}
"""
