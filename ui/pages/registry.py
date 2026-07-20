# ui/page_registry.py

from ui.pages import (
    memory_breakdown,
    runtime_breakdown,
    root_cause_summary,
    history,
    comparison
)

PAGES = {
    "Memory Breakdown": memory_breakdown.render_memory_breakdown,
    "Runtime Breakdown": runtime_breakdown.render_runtime_breakdown,
    "Root Cause Summary": root_cause_summary.render_root_cause_summary,
    "History": history.render_history,
    "Comparison": comparison.render_comparison,
}

