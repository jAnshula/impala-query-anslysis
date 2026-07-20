from core.time_util import ms_to_hms

class RuntimeBreakdownAnalyzer:
    def analyze(self, profile):
        timeline = getattr(profile, "timeline", None)
        if not timeline:
            return {}

        events = getattr(timeline, "events", {})

        planning = events.get("planning_ms", 0) or 0
        admission = events.get("admission_ms", 0) or 0
        execution = events.get("execution_ms", 0) or 0

        # Clamp negatives immediately
        planning = max(planning, 0)
        admission = max(admission, 0)
        execution = max(execution, 0)

        total = planning + admission + execution

        # If execution is still zero but total is larger, recompute safely
        if execution == 0 and total > 0:
            derived = total - planning - admission
            execution = max(derived, 0)

        # Recompute total after adjustments
        total = planning + admission + execution
        if total <= 0:
            return {}

        def pct(part, total):
            return round(part * 100 / total, 1) if total > 0 else 0.0

        return {
            "planning_ms": planning,
            "admission_ms": admission,
            "execution_ms": execution,
            "total_ms": total,

            "planning_pct": pct(planning, total),
            "admission_pct": pct(admission, total),
            "execution_pct": pct(execution, total),

            "planning_hms": ms_to_hms(planning),
            "admission_hms": ms_to_hms(admission),
            "execution_hms": ms_to_hms(execution),
            "total_hms": ms_to_hms(total),

            "planning_label": f"{ms_to_hms(planning)} ({pct(planning, total)}%)",
            "admission_label": f"{ms_to_hms(admission)} ({pct(admission, total)}%)",
            "execution_label": f"{ms_to_hms(execution)} ({pct(execution, total)}%)",
            "total_label": f"{ms_to_hms(total)} (100%)"
        }

