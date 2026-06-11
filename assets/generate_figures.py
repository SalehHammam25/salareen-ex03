"""Generate deterministic figures and comparison table for the HITL article.

Produces three assets:
    assets/hitl_decision_flow.png        — confidence-based routing flow diagram
    assets/automation_risk_tradeoff.png  — grouped bar chart, risk by domain
    assets/hitl_comparison_table.csv     — comparison data (also used by LaTeX)

Run directly:
    uv run python assets/generate_figures.py
"""
from __future__ import annotations

import csv
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # non-interactive backend; must precede pyplot import
import matplotlib.pyplot as plt

_ASSETS_DIR = Path(__file__).parent


def asset_names() -> list[str]:
    """Return the filenames that generate_all() will write."""
    return [
        "hitl_decision_flow.png",
        "automation_risk_tradeoff.png",
        "hitl_comparison_table.csv",
    ]


def generate_hitl_flow(assets_dir: Path | None = None) -> Path:
    """Draw a HITL confidence-based routing flow diagram and save as PNG."""
    out = Path(assets_dir) if assets_dir is not None else _ASSETS_DIR
    out.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(8, 7))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    def _box(x, y, text, fc, ec):
        ax.text(x, y, text, ha="center", va="center", fontsize=10,
                bbox=dict(boxstyle="round,pad=0.35", facecolor=fc, edgecolor=ec, lw=1.5))

    def _arrow(x0, y0, x1, y1, color="steelblue"):
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=color, lw=1.8))

    _box(0.50, 0.88, "Input Data",                    "#AED6F1", "navy")
    _box(0.50, 0.70, "ML Model Prediction",            "#AED6F1", "navy")
    _box(0.50, 0.52, "Confidence ≥ θ?",     "#FAD7A0", "darkorange")
    _box(0.20, 0.32, "AUTO-APPROVE\n(High Confidence)","#A9DFBF", "darkgreen")
    _box(0.80, 0.32, "HUMAN REVIEW\n(Low Confidence)", "#F1948A", "darkred")
    _box(0.50, 0.12, "Final Output + Feedback Loop",   "#AED6F1", "navy")

    _arrow(0.50, 0.84, 0.50, 0.74)
    _arrow(0.50, 0.66, 0.50, 0.56)
    _arrow(0.44, 0.49, 0.26, 0.37, "darkgreen")
    _arrow(0.56, 0.49, 0.74, 0.37, "darkred")
    _arrow(0.23, 0.27, 0.44, 0.16)
    _arrow(0.77, 0.27, 0.56, 0.16)

    ax.text(0.34, 0.455, "Yes", color="darkgreen", fontsize=9, ha="center")
    ax.text(0.65, 0.455, "No",  color="darkred",   fontsize=9, ha="center")
    ax.set_title("HITL Decision Flow: Confidence-Based Routing",
                 fontsize=13, fontweight="bold", pad=12)

    path = out / "hitl_decision_flow.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_risk_tradeoff(assets_dir: Path | None = None) -> Path:
    """Draw a grouped bar chart comparing risk scores by domain."""
    out = Path(assets_dir) if assets_dir is not None else _ASSETS_DIR
    out.mkdir(parents=True, exist_ok=True)

    domains   = ["Medical\nDiagnosis", "Content\nModeration",
                 "Autonomous\nVehicles", "Email\nTriage"]
    auto_risk = [8.5, 7.0, 9.0, 3.5]
    hitl_risk = [2.5, 3.0, 2.0, 1.5]
    width = 0.35
    xs = range(len(domains))

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar([i - width / 2 for i in xs], auto_risk, width,
           label="Full Automation", color="#E74C3C", alpha=0.85)
    ax.bar([i + width / 2 for i in xs], hitl_risk, width,
           label="HITL System",      color="#2ECC71", alpha=0.85)

    ax.set_xlabel("Domain", fontsize=12)
    ax.set_ylabel("Risk Score (0–10)", fontsize=12)
    ax.set_title("Risk Score: Full Automation vs. HITL by Domain",
                 fontsize=13, fontweight="bold")
    ax.set_xticks(list(xs))
    ax.set_xticklabels(domains, fontsize=10)
    ax.set_ylim(0, 11)
    ax.legend(fontsize=11)
    ax.grid(axis="y", alpha=0.3, linestyle="--")
    fig.tight_layout()

    path = out / "automation_risk_tradeoff.png"
    fig.savefig(path, dpi=150, bbox_inches="tight")
    plt.close(fig)
    return path


def generate_comparison_table(assets_dir: Path | None = None) -> Path:
    """Write a CSV comparison table: Full Automation vs. HITL."""
    out = Path(assets_dir) if assets_dir is not None else _ASSETS_DIR
    out.mkdir(parents=True, exist_ok=True)
    rows = [
        ["Criterion",            "Full Automation", "HITL System"],
        ["Throughput",           "High",            "Moderate"],
        ["Edge-case error rate", "High",            "Low"],
        ["Accountability",       "Diffuse",         "Clear"],
        ["Cost per decision",    "Low",             "Higher"],
        ["Auditability",         "Poor",            "Strong"],
        ["Human oversight",      "None",            "Selective"],
    ]
    path = out / "hitl_comparison_table.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(rows)
    return path


def generate_all(assets_dir: Path | None = None) -> dict[str, Path]:
    """Generate all figures and the comparison table; return {filename: path}."""
    out = Path(assets_dir) if assets_dir is not None else _ASSETS_DIR
    return {
        "hitl_decision_flow.png":       generate_hitl_flow(out),
        "automation_risk_tradeoff.png": generate_risk_tradeoff(out),
        "hitl_comparison_table.csv":    generate_comparison_table(out),
    }


if __name__ == "__main__":
    written = generate_all()
    for name, path in written.items():
        print(f"  [GENERATED]  {name}  ({path.stat().st_size:,} bytes)")
    print(f"\n{len(written)} assets generated in: assets/")
