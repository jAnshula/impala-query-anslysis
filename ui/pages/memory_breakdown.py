import profile

import pandas as pd
import streamlit as st


def render_memory_breakdown(profile):

    st.subheader("Memory Analytics")

    # --------------------------------------------------
    # Memory Metrics
    # --------------------------------------------------
    memory_metrics = getattr(
        profile,
        "memory_metrics",
        {}
    ) or {}

    fragment_instances = getattr(
        profile,
        "fragment_instances",
        []
    ) or []

    operator_metrics = getattr(
        profile,
        "operator_metrics",
        []
    ) or []

    peak_mb = memory_metrics.get(
        "peak_memory_mb",
        0
    )

    estimate_gb = memory_metrics.get(
        "per_host_memory_estimate_gb",
        0
    )

    reservation_mb = memory_metrics.get(
        "max_per_host_resource_reservation_mb",
        0
    )

    health = memory_metrics.get(
        "memory_health",
        "UNKNOWN"
    )

    utilization = memory_metrics.get(
        "memory_utilization_pct",
        0
    )

    st.divider()

    st.subheader(
        "Cluster-wide Peak Memory by Host"
    )

    host_memory = {}

    for inst in fragment_instances:

        host = getattr(
            inst,
            "host",
            "unknown"
        )

        instance_peak_mb = (
            getattr(
                inst,
                "peak_memory",
                0
            )
            / (1024 * 1024)
        )

        host_memory[host] = max(
            host_memory.get(host, 0),
            instance_peak_mb
        )

    if host_memory:

        host_df = pd.DataFrame(
            list(host_memory.items()),
            columns=[
                "Host",
                "Peak MB"
            ]
        )

        st.bar_chart(
            host_df.set_index(
                "Host"
            )
        )

    st.divider()

    st.subheader(
        "Top Memory Consuming Operators"
    )

    if operator_metrics:

        ops_df = pd.DataFrame(
            operator_metrics
        )

        memory_col = None

        for col in ops_df.columns:

            if "memory" in col.lower():
                memory_col = col
                break

        if memory_col:

            ops_df = (
                ops_df
                .sort_values(
                    memory_col,
                    ascending=False
                )
                .head(10)
            )

        st.dataframe(
            ops_df,
            use_container_width=True
        )

    # --------------------------------------------------
    # Empty State
    # --------------------------------------------------

    if peak_mb <= 0 and estimate_gb <= 0:

        st.warning(
            "No memory information available in profile."
        )

        return

    # --------------------------------------------------
    # KPI Cards
    # --------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Per-Host Memory Estimate",
            f"{estimate_gb:.2f} GB"
        )

    with col2:
        st.metric(
            "Resource Reservation",
            f"{reservation_mb:.2f} MB"
        )

    with col3:
        st.metric(
            "Peak Actual Memory",
            f"{peak_mb:.0f} MB"
        )

    with col4:
        st.metric(
            "Memory Health",
            health
        )

    st.caption(
        f"Memory Utilization: {utilization:.1f}%"
    )

    st.divider()

    # --------------------------------------------------
    # Fragment Memory Breakdown
    # --------------------------------------------------

    components = memory_metrics.get(
        "components",
        []
    )

    if components:

        st.subheader(
            "Fragment Memory Breakdown"
        )

        df = pd.DataFrame(
            components
        )

        rename_map = {
            "Fragment": "Fragment ID",
            "Peak Memory (MB)": "Peak Memory MB",
            "Peak Memory (GB)": "Peak Memory GB",
            "Instances": "Instances",
            "Runtime (HH:MM:SS)": "Runtime"
        }

        df = df.rename(
            columns=rename_map
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        # Chart

        memory_column = None

        for col in df.columns:

            if "Peak Memory MB" in col:
                memory_column = col
                break

        if memory_column:

            chart_df = (
                df[
                    ["Fragment ID", memory_column]
                ]
                .set_index(
                    "Fragment ID"
                )
            )

            st.subheader(
                "Memory Distribution by Fragment"
            )

            st.bar_chart(
                chart_df
            )

    # --------------------------------------------------
    # Spill Analysis
    # --------------------------------------------------

    spill_detected = memory_metrics.get(
        "spill_detected",
        False
    )

    spill_count = memory_metrics.get(
        "spill_count",
        0
    )

    scratch_bytes = memory_metrics.get(
        "scratch_bytes_written",
        0
    )

    st.divider()

    st.subheader(
        "Spill Analysis"
    )

    if spill_detected:

        st.error(
            f"Disk spill detected ({spill_count} spill events)"
        )

        st.write(
            f"Scratch Bytes Written: "
            f"{scratch_bytes:,}"
        )

    else:

        st.success(
            "No memory spill detected."
        )

    # --------------------------------------------------
    # Raw Metrics
    # --------------------------------------------------

    with st.expander(
        "Memory Metrics (Raw)"
    ):

        st.json(
            memory_metrics
        )

