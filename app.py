import streamlit as st
import pandas as pd
import plotly.express as px


from services.execution_profile_builder import ExecutionProfileBuilder
from services.analytics_engine import AnalyticsEngine
from intelligence.intelligence_engine import IntelligenceEngine
from services.analytics_engine import AnalyticsEngine
from intelligence.root_cause_engine import RootCauseEngine
from intelligence.recommendation_engine import RecommendationEngine
from intelligence.root_cause_chain import RootCauseChainBuilder
from analyzers.execution_analyzer import ExecutionAnalyzer
from ui.pages.memory_breakdown import render_memory_breakdown
from analyzers.findings import Finding


def format_duration(ms):

    if ms is None:
        return "00:00:00"

    try:
        ms = int(ms)
    except Exception:
        return str(ms)

    total_seconds = int(ms / 1000)

    hours = total_seconds // 3600

    minutes = (
        total_seconds % 3600
    ) // 60

    seconds = (
        total_seconds % 60
    )

    return (
        f"{hours:02d}:"
        f"{minutes:02d}:"
        f"{seconds:02d}"
    )

# ======================================================
# CONFIG
# ======================================================

st.set_page_config(
    page_title="Impala Query Intelligence",
    page_icon="🚀",
    layout="wide"
)


st.title(
    "🚀 Impala Query Intelligence Platform"
)



# ======================================================
# UPLOAD
# ======================================================

uploaded = st.file_uploader(
    "Upload Query Profile",
    type=[
        "txt",
        "profile"
    ]
)



if uploaded:
    profile_text = (
        uploaded
        .read()
        .decode(
            "utf-8",
            errors="ignore"
        )
    )
    # only reset when new file uploaded
    if (
        st.session_state.get(
            "profile_text"
        )
        != profile_text
    ):
        st.session_state.clear()

        st.session_state[
            "profile_text"
        ] = profile_text
if (
    "profile_text"
    not in st.session_state
):
    st.info(
        "Upload an Impala profile to begin."
    )
    st.stop()



# ======================================================
# BUILD PROFILE
# ======================================================

if (
    "profile"
    not in st.session_state
):
    profile = (
        ExecutionProfileBuilder()
        .build(
            st.session_state[
                "profile_text"
            ]
        )
    )
    st.session_state[
        "profile"
    ] = profile
else:
    profile = (
        st.session_state[
            "profile"
        ]
    )




# ======================================================
# ANALYTICS
# ======================================================

if (
    "analytics"
    not in st.session_state
):
    analytics = (
        AnalyticsEngine()
        .analyze(profile)
    )
    st.session_state[
        "analytics"
    ] = analytics
else:

    analytics = (
        st.session_state[
            "analytics"
        ]
    )

# ======================================================
# INTELLIGENCE
# ======================================================

if (
    "intelligence"
    not in st.session_state
):
    intelligence = (
        IntelligenceEngine()
        .run(
            profile,
            analytics
        )
    )
    st.session_state[
        "intelligence"
    ] = intelligence
else:
    intelligence = (
        st.session_state[
            "intelligence"
        ]
    )


# ======================================================
# ROOT CAUSE CHAIN
# ======================================================

chain = (
    RootCauseChainBuilder()
    .build(
        profile,
        analytics,
        intelligence
    )
)


# ======================================================
# MAIN LAYOUT
# ======================================================

left,right = st.columns(
    [
        1,
        3
    ],
    gap="large"
)



# ======================================================
# LEFT PANEL - PROFILE
# ======================================================

with left:
    st.subheader(
        "📄 Query Profile"
    )
    with st.expander(
        "View Raw Profile",
        expanded=False
    ):
        st.text_area(
            "Profile Text",
            st.session_state[
                "profile_text"
            ],
            height=700
        )



    st.subheader(
        "Query Info"
    )
    st.metric(
        "Query ID",
        profile.query_info.query_id
    )
    st.metric(
        "User",
        profile.query_info.user
    )
    st.metric(
        "State",
        profile.query_info.state
    )
    st.metric(
        "Coordinator",
        profile.query_info.coordinator
    )

# ======================================================
# RIGHT PANEL - ANALYSIS
# ======================================================

with right:
    score = analytics.get("health_score", 0)
    st.subheader("Health Score")
    st.progress(min(score, 100) / 100)
    st.metric(
        "Health Score",
        f"{score}/100"
    )
    timeline = getattr(profile, "timeline", {})
    planning_ms = timeline.get(
        "planning_ms",
        0
    )
    admission_ms = timeline.get(
        "admission_ms",
        0
    )
    execution_ms = timeline.get(
        "execution_ms",
        0
    )
    metadata_time = timeline.get(
        "metadata_ms",
        0
    )
    total_ms = (
        planning_ms +
        admission_ms +
        execution_ms
    )
    if total_ms > 0:
        planning_pct = round(
            planning_ms * 100 / total_ms,
            1
        )
        admission_pct = round(
            admission_ms * 100 / total_ms,
            1
        )
        execution_pct = round(
            execution_ms * 100 / total_ms,
            1
        )
        st.subheader(
            "Runtime Breakdown"
        )
        runtime_df = pd.DataFrame(
            [
                {
                    "Phase": "Planning",
                    "Duration":
                        format_duration(
                            planning_ms
                        ),
                    "Percent":
                        format_duration(planning_pct)
                },
                {
                    "Phase": "Admission",
                    "Duration":
                        format_duration(
                            admission_ms
                        ),
                    "Percent":
                        format_duration(admission_pct)
                },
                {
                    "Phase": "Execution",
                    "Duration":
                        format_duration(
                            execution_ms
                        ),
                    "Percent":
                        format_duration(execution_pct)
                }
            ]
        )
        st.dataframe(
            runtime_df,
            use_container_width=True
        )

    k1,k2,k3,k4,k5 = st.columns(5)

    memory = getattr(
        profile,
        "memory_metrics",
        {}
    ) or {}

    k1.metric(
        "Planning",
        format_duration(planning_ms)
    )
    k2.metric(
        "Admission",
        format_duration(admission_ms)
    )
    k3.metric(
        "Execution",
        format_duration(execution_ms)
    )
    k4.metric(
        "Peak Memory",
        f"{memory.get('peak_memory_gb',0):.2f} GB"
    )
    k5.metric(
        "Fragments",
        len(profile.fragment_instances)
    )
    st.divider()

    tab1,tab2,tab3,tab4,tab5,tab6 = st.tabs(
        [
            "Executive View",
            "Runtime Timeline",
            "Scan Analytics",
            "Memory Analysis",
            "Fragments Details",
            "Fragment Summary"
        ]
    )

    # ==================================================
    # OVERVIEW
    # ==================================================

    with tab1:
        raw_text = getattr(
            profile,
            "raw_profile",
            ""
        )
        if (
            "PARTITION_NOT_FOUND" in raw_text
            or
            "inconsistent metadata" in raw_text
        ):
            st.error(
                f"""
            🔴 CRITICAL ROOT CAUSE

            Catalog Metadata Inconsistency

            Planning Time : {format_duration(planning_ms)}
            Admission Time : {format_duration(admission_ms)}
            Execution Time : {format_duration(execution_ms)}

            Detected:
            • PARTITION_NOT_FOUND
            • Metadata planning retries
            • Catalog synchronization issue

            Impact:
            • Planning dominates query runtime
            • Execution itself is healthy
            """
            )
            st.markdown(
                """
        ### Evidence

        - PARTITION_NOT_FOUND detected
        - Query planning retried multiple times
        - Planning dominated total runtime
        - Execution phase itself was healthy

        ### Recommendation

        1. Refresh metadata
        2. Invalidate metadata
        3. Repair missing partitions
        4. Verify catalogd synchronization
        """
            )

        st.header("Executive Summary")
        st.info(
            intelligence.get(
                "summary",
                ""
            )
        )
        findings = analytics.get(
            "findings",
            []
        )
        if not findings:
            st.success(
                "No findings detected"
            )
        for finding in findings:
            if isinstance(finding, dict):
                severity = finding.get("severity", "medium")
                title = finding.get("title", "Finding")
                description = finding.get("description", "")
            elif isinstance(finding, Finding):
                severity = finding.severity or "medium"
                title = finding.title or "Finding"
                description = finding.description or ""
            else:
                severity, title, description = "medium", str(finding), ""

            if severity.lower() == "critical":
                st.error(title)
            elif severity.lower() == "high":
                st.warning(title)
            else:
                st.info(title)

            if description:
                st.write(description)

    # ==================================================
    # TIMELINE
    # ==================================================

    with tab2:
        st.header("Execution Timeline")
        timeline_rows = []
        for k,v in timeline.get("events",{}).items():
            timeline_rows.append(
                {
                    "Phase": k,
                    "Duration": format_duration(v),
                    "Duration_ms": v
                }
            )
        if timeline_rows:
            timeline_df = pd.DataFrame(
                timeline_rows
            )
            st.bar_chart(
                timeline_df
                .set_index("Phase")
                [["Duration_ms"]]
            )
            st.dataframe(
                timeline_df[
                    ["Phase","Duration"]
                ],
                use_container_width=True
            )

    # ==================================================
    # SCAN
    # ==================================================
    with tab3:
        st.header("Scan Analytics")

        scan = getattr(
            profile,
            "scan_metrics",
            {}
        ) or {}

        c1,c2,c3,c4 = st.columns(4)

        files_scanned = scan.get(
            "files_scanned",
            0
        )
        partitions_scanned = scan.get(
            "partitions_scanned",
            0
        )
        rows_read = scan.get(
            "rows_read",
            0
        )
        bytes_read = scan.get(
            "bytes_read",
            0
        )
        c1.metric(
            "Files Scanned",
            f"{files_scanned:,}"
        )
        c2.metric(
            "Bytes Read (GB)",
            round(
                bytes_read / 1024**3,
                2
            )
        )
        c3.metric(
            "Rows Read",
            f"{rows_read:,}"
        )
        c4.metric(
            "Partitions",
            partitions_scanned
        )

        # ====================================
        # Observations
        # ====================================

        st.subheader("Observations")
        if partitions_scanned > 300:
            st.warning(
                f"Large partition scan detected "
                f"({partitions_scanned} partitions scanned). "
                f"Partition pruning may be ineffective."
            )
        if files_scanned > 500:

            st.warning(
                f"Large file scan detected "
                f"({files_scanned} files). "
                f"Consider compaction."
            )
        if rows_read > 1_000_000:
            st.info(
                f"High volume scan detected"
                f"({rows_read:,} rows)."
            )
        st.divider()
        st.subheader("Raw Scan Metrics")
        st.json(scan)

    # ==================================================
    # MEMORY
    # ==================================================

    with tab4:
        render_memory_breakdown(
            profile
        )

    # ==================================================
    # FRAGMENTS
    # ==================================================

    with tab5:

        st.header("Fragment Analytics")

        instances = (
            profile.fragment_instances
        )

        if not instances:

            st.warning(
                "No fragment instances found"
            )

        else:

            rows = []

            for x in instances:

                rows.append(
                    {
                        "Fragment":
                            x.fragment,

                        "Operator":
                            x.operator,

                        "Host":
                            x.host,

                        "Runtime (s)":
                            round(
                                x.runtime_ms
                                / 1000,
                                2
                            ),

                        "Rows":
                            x.rows,

                        "Read MB":
                            x.read_mb,

                        "Write MB":
                            x.write_mb,

                        "Memory MB":
                            x.peak_memory_mb,

                        "Network ms":
                            x.total_network_ms,

                        "IO Wait ms":
                            x.io_wait_ms
                    }
                )
            df = pd.DataFrame(rows)
            avg_runtime = (
                df["Runtime (s)"]
                .mean()
            )
            max_runtime = (
                df["Runtime (s)"]
                .max()
            )
            skew_ratio = (
                max_runtime
                / avg_runtime
                if avg_runtime
                else 0
            )
            st.metric(
                "Runtime Skew Ratio",
                f"{skew_ratio:.2f}"
            )
            if skew_ratio > 3:
                st.error(
                    "Severe runtime skew detected"
                )
            st.subheader(
                "All Fragments"
            )
            st.dataframe(
                df,
                use_container_width=True
            )

    # ==================================================
    # FRAGMENT SUMMARY
    # ==================================================
    
    with tab6:
        st.header("Fragment Summary")

        summary = (
            ExecutionAnalyzer()
            .fragment_summary(
                profile.fragment_instances
            )
        )

        fragment_df = pd.DataFrame(
            summary.values()
        )
        st.dataframe(
            fragment_df,
            use_container_width=True
        )
        st.header(
            "Operator-Level Performance"
        )
        operator_df = pd.DataFrame(
            profile.operator_metrics
        )
        if not operator_df.empty:
            operator_df["Runtime"] = (
                operator_df[
                    "runtime_seconds"
                ]
                .apply(
                    lambda x:
                    format_duration(
                        x * 1000
                    )
                )
            )
            st.dataframe(
                operator_df,
                use_container_width=True
            )
        st.header(
            "Resource Consumption Ranking"
        )
        ranking_rows = []

        for op in profile.operator_metrics:

            runtime = op.get(
                "runtime_seconds",
                0
            )

            ranking_rows.append(
                {
                    "Operator": op.get("operator", "UNKNOWN"),
                    "Runtime": runtime,
                    "Peak Memory": op.get("peak_memory_gb", 0)
                }
            )
        ranking_df = pd.DataFrame(ranking_rows)

        if not ranking_df.empty and "Runtime" in ranking_df.columns:
            ranking_df = ranking_df.sort_values("Runtime", ascending=False)
            st.dataframe(ranking_df)
        else:
            st.info("No runtime metrics available to rank operators.")

        st.dataframe(
            ranking_df
        )
        st.header(
            "Scan Analysis"
        )
        scan_rows = [
            {
                "Files":
                    scan.get(
                        "files_scanned",
                        0
                    ),
                "Partitions":
                    scan.get(
                        "partitions_scanned",
                        0
                    ),
                "Rows":
                    scan.get(
                        "rows_read",
                        0
                    )
            }
        ]
        st.dataframe(
            pd.DataFrame(
                scan_rows
            )
        )
        st.subheader(
            "Runtime Distribution"
        )

        if total_ms > 0:

            st.dataframe(
                runtime_df,
                use_container_width=True
            )

            runtime_fig = px.pie(
                runtime_df,
                names="Phase",
                values="Percent",
                title="Query Runtime Distribution"
            )

            st.plotly_chart(
                runtime_fig,
                use_container_width=True
            )

        else:

            st.info(
                "Runtime breakdown unavailable."
            )
        st.header(
            "CPU Analysis"
        )
        cpu_df = pd.DataFrame(
            profile.cpu_metrics
        )
        if cpu_df.empty:
            st.info(
                "No CPU metrics extracted."
            )
        else:
            st.dataframe(
                cpu_df,
                use_container_width=True
            )
            st.bar_chart(
                cpu_df.set_index(
                    "host"
                )[
                    "cpu_seconds"
                ]
            )
            total_cpu = (
                cpu_df[
                    "cpu_seconds"
                ].sum()
            )
            cpu_df[
                "cpu_pct"
            ] = (
                cpu_df[
                    "cpu_seconds"
                ]
                / total_cpu
                * 100
            )
            coordinator_cpu = (
                cpu_df[
                    "cpu_pct"
                ].max()
            )
            if coordinator_cpu > 80:
                st.warning(
                    "CPU workload is highly concentrated on a single host."
                )
        st.header(
            "Network Analysis"
        )
        network = (
            profile.network_metrics
        )
        c1,c2,c3,c4 = st.columns(4)
        c1.metric(
            "Bytes Sent",
            f"{network.get('bytes_sent',0):.2f} MB"
        )
        c2.metric(
            "Bytes Received",
            f"{network.get('bytes_received',0):.2f} MB"
        )
        c3.metric(
            "RPC Write Time",
            f"{network.get('rpc_write_time',0):.2f}s"
        )
        c4.metric(
            "RPC Read Time",
            f"{network.get('rpc_read_time',0):.3f}s"
        )
        total_network = (
            network.get(
                "bytes_sent",
                0
            )
            +
            network.get(
                "bytes_received",
                0
            )
        )
        if total_network < 100:

            st.success(
                "Network is not a bottleneck."
            )
        elif total_network < 1000:
            st.info(
                "Moderate network utilization."
            )
        else:
            st.warning(
                "High network utilization detected."
            )
        st.divider()
        st.header(
            "Root Cause Chain"
        )
        if not chain:
            st.info(
                "No execution chain generated."
            )
        else:
            for idx, step in enumerate(chain):
                st.markdown(
                    f"### {step}"
                )
                if idx < len(chain) - 1:
                    st.markdown(
                        "<div style='text-align:center;font-size:28px'>⬇️</div>",
                        unsafe_allow_html=True
                    )

