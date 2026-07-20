import streamlit as st


def render_root_cause_summary(
    profile,
    runtime_breakdown
):

    if not runtime_breakdown:
        return

    text = getattr(
        profile,
        "raw_profile",
        ""
    )

    planning_pct = runtime_breakdown.get(
        "planning_pct",
        0
    )

    if (
        "PARTITION_NOT_FOUND" in text
        and planning_pct > 80
    ):

        st.error(
            "ROOT CAUSE: Catalog Metadata Inconsistency"
        )

        st.markdown(
            f"""
### Evidence

- PARTITION_NOT_FOUND detected
- Planning retried due to inconsistent metadata
- Planning consumed {planning_pct:.1f}% of runtime
- Execution phase itself was healthy

### Recommendation

1. Refresh metadata
2. Invalidate metadata
3. Repair missing partitions
4. Investigate catalogd synchronization
"""
        )

