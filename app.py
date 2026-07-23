# ============================================================
# Impala Query Intelligence Platform
# app.py
# ============================================================

import logging
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# Performance thresholds (configurable)
PLANNING_PERCENT_THRESHOLD = 50
ADMISSION_PERCENT_THRESHOLD = 20
EXECUTION_PERCENT_THRESHOLD = 80
FILES_SCANNED_THRESHOLD = 500
PEAK_MEMORY_THRESHOLD_GB = 50
NETWORK_THRESHOLD_MB = 1000
CPU_THRESHOLD_SECONDS = 3600

# Optional Components
try:
    from st_aggrid import (
        AgGrid,
        GridOptionsBuilder,
        GridUpdateMode,
    )

    AGGRID_AVAILABLE = True

except ImportError:
    AGGRID_AVAILABLE = False

try:
    from reportlab.lib.styles import getSampleStyleSheet
    from reportlab.platypus import Paragraph, SimpleDocTemplate

    PDF_AVAILABLE = True

except ImportError:
    PDF_AVAILABLE = False


# ============================================================
# Project Imports
# ============================================================

from services.execution_profile_builder import (
    ExecutionProfileBuilder,
)

from services.analytics_engine import (
    AnalyticsEngine,
)

from intelligence.intelligence_engine import (
    IntelligenceEngine,
)

from intelligence.root_cause_chain import (
    RootCauseChainBuilder,
)

from analyzers.execution_analyzer import (
    ExecutionAnalyzer,
)

from analyzers.findings import Finding

from ui.pages.memory_breakdown import (
    render_memory_breakdown,
)

# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(
    page_title="Impala Query Intelligence Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# Theme
# ============================================================

st.markdown(
    """
<style>

.block-container{
    padding-top:1rem;
    padding-bottom:1rem;
}

.metric-card{
    border-radius:8px;
    padding:12px;
    background:#fafafa;
}

.small-font{
    font-size:0.85rem;
}

</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# Utility Functions
# ============================================================

def format_duration(ms):
    if ms is None:
        return "00:00:00"
    try:
        ms = int(ms)
    except (ValueError, TypeError):
        # Only catch conversion errors, not unexpected exceptions
        return str(ms)
    except Exception as e:
        import logging
        logging.warning(f"Unexpected error formatting duration {ms}: {e}")
        return str(ms)

    seconds = ms // 1000
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60

    return f"{h:02d}:{m:02d}:{s:02d}"


def bytes_to_mb(value):

    return round(value / (1024 ** 2), 2)


def bytes_to_gb(value):

    return round(value / (1024 ** 3), 2)


def severity_color(level):

    level = str(level).lower()

    if level == "critical":
        return "🔴"

    if level == "high":
        return "🟠"

    if level == "medium":
        return "🟡"

    return "🟢"


# ============================================================
# Cached Builders
# ============================================================

@st.cache_data(show_spinner=True)
def build_profile(profile_text):

    builder = ExecutionProfileBuilder()

    return builder.build(profile_text)


@st.cache_data(show_spinner=False)
def run_analytics(profile):

    return AnalyticsEngine().analyze(profile)


@st.cache_data(show_spinner=False)
def run_intelligence(profile, analytics):

    return IntelligenceEngine().run(
        profile,
        analytics,
    )


@st.cache_data(show_spinner=False)
def build_root_chain(
    profile,
    analytics,
    intelligence,
):

    return RootCauseChainBuilder().build(
        profile,
        analytics,
        intelligence,
    )


# ============================================================
# Page Title
# ============================================================

st.title("🚀 Impala Query Intelligence Platform")

st.caption(
    "Interactive Apache Impala Query Profile Analyzer"
)

# ============================================================
# Sidebar
# ============================================================

with st.sidebar:

    st.header("Navigation")

    page = st.radio(
        "",
        [
            "🏠 Query Overview",
            "⏱ Runtime Timeline",
            "🧩 Fragment Analytics",
            "📈 Resource Utilization",
            "🗺️ Query Plan",
            "🔍 Findings",
            "📤 Export",
        ],
    )

    st.divider()

    st.header("Input")

    uploaded_file = st.file_uploader(
        "Upload Query Profile",
        type=[
            "txt",
            "profile",
            "log",
        ],
    )

    profile_text_area = st.text_area(
        "Or Paste Query Profile",
        height=250,
        placeholder="Paste complete Impala Query Profile here...",
    )

    # ============================================================
    # Resolve Input Source
    # ============================================================

    profile_text = ""

    if uploaded_file is not None:

        profile_text = uploaded_file.read().decode(
            "utf-8",
            errors="ignore",
        )

    elif profile_text_area.strip():

        profile_text = profile_text_area

    else:

        st.info(
            "Upload an Impala Query Profile or paste it into the text area."
        )

        st.stop()


    # ============================================================
    # Detect Profile Change
    # ============================================================

    if (
        "current_profile_text"
        not in st.session_state
    ):

        st.session_state.current_profile_text = profile_text

    elif (
        st.session_state.current_profile_text
        != profile_text
    ):

        st.session_state.current_profile_text = profile_text

        for key in [
            "profile",
            "analytics",
            "intelligence",
            "chain",
        ]:

            if key in st.session_state:
                del st.session_state[key]

    # ============================================================
    # Build Execution Profile
    # ============================================================

    if "profile" not in st.session_state:

        with st.spinner("Parsing Query Profile..."):

            st.session_state.profile = build_profile(
                profile_text
            )

    profile = st.session_state.profile


    # ============================================================
    # Analytics
    # ============================================================

    if "analytics" not in st.session_state:

        with st.spinner("Running Analytics..."):

            st.session_state.analytics = run_analytics(
                profile
            )

    analytics = st.session_state.analytics


    # ============================================================
    # Intelligence
    # ============================================================

    if "intelligence" not in st.session_state:

        with st.spinner("Generating Intelligence..."):

            st.session_state.intelligence = run_intelligence(
                profile,
                analytics,
            )

    intelligence = st.session_state.intelligence


    # ============================================================
    # Root Cause Chain
    # ============================================================

    if "chain" not in st.session_state:

        st.session_state.chain = build_root_chain(
            profile,
            analytics,
            intelligence,
        )

    chain = st.session_state.chain

    # ============================================================
    # Query Overview
    # ============================================================
    
    if page == "🏠 Query Overview":

        st.title("🏠 Query Overview")

        # Validate profile exists
        if not profile or not hasattr(profile, 'query_info'):
            st.error("Failed to parse query profile. Please check the input.")
            st.stop()

        query = profile.query_info
        
        if not query:
            st.error("Failed to extract query information.")
            st.stop()
        
        timeline = profile.timeline or {}
        memory = profile.memory_metrics or {}
        scan = profile.scan_metrics or {}

        # Safe dict access with defaults
        planning_ms = timeline.get("planning_ms", 0) if isinstance(timeline, dict) else 0
        admission_ms = timeline.get("admission_ms", 0) if isinstance(timeline, dict) else 0
        execution_ms = timeline.get("execution_ms", 0) if isinstance(timeline, dict) else 0
        total_ms = timeline.get("total_ms", 0) if isinstance(timeline, dict) else 0

        if total_ms == 0:
            total_ms = (
                planning_ms +
                admission_ms +
                execution_ms
            )

        # =====================================================
        # Query Metadata
        # =====================================================

        st.subheader("Query Information")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**Query ID**  \n`{getattr(query, 'query_id', 'N/A')}`")
            st.markdown(f"**User**  \n{getattr(query, 'user', 'N/A')}")
            st.markdown(f"**Coordinator**  \n{getattr(query, 'coordinator', 'N/A')}")
            st.markdown(f"**Pool**  \n{getattr(query, 'pool', 'N/A')}")
        with c2:
            st.markdown(f"**State**  \n{getattr(query, 'state', 'N/A')}")
            st.markdown(f"**Query Type**  \n{getattr(query, 'query_type', 'N/A')}")
            st.markdown(f"**Start Time**  \n{getattr(query, 'start_time', 'N/A')}")
            st.markdown(f"**End Time**  \n{getattr(query, 'end_time', 'N/A')}")
        st.divider()

        # =====================================================
        # Health Score
        # =====================================================

        score = analytics.get("health_score", 100)

        st.subheader("Overall Query Health")

        st.progress(score / 100)

        cols = st.columns(5)

        cols[0].metric(
            "Health Score",
            f"{score}/100"
        )

        cols[1].metric(
            "Peak Memory",
            f"{memory.get('peak_memory_gb',0):.2f} GB"
        )

        cols[2].metric(
            "Fragments",
            len(profile.fragment_instances)
        )

        cols[3].metric(
            "Files Scanned",
            f"{scan.get('files_scanned',0):,}"
        )

        cols[4].metric(
            "Rows Read",
            f"{scan.get('rows_read',0):,}"
        )

        st.divider()

        # =====================================================
        # Executive Summary
        # =====================================================

        st.subheader("Executive Summary")

        st.info(
            intelligence.get(
                "summary",
                "No executive summary available."
            )
        )

        st.divider()

        # =====================================================
        # Runtime Breakdown
        # =====================================================

        st.subheader("Runtime Breakdown")

        runtime_df = pd.DataFrame(

            [

                {
                    "Phase": "Planning",
                    "Duration (ms)": planning_ms
                },

                {
                    "Phase": "Admission",
                    "Duration (ms)": admission_ms
                },

                {
                    "Phase": "Execution",
                    "Duration (ms)": execution_ms
                }

            ]

        )

        left, right = st.columns([2, 1])

        with left:

            st.bar_chart(

                runtime_df.set_index("Phase")

            )

        with right:

            if total_ms > 0:

                runtime_df["Percent"] = (

                    runtime_df["Duration (ms)"]

                    / total_ms

                    * 100

                )

                fig = px.pie(

                    runtime_df,

                    names="Phase",

                    values="Duration (ms)",

                    hole=0.45,

                    title="Runtime Distribution"

                )

                st.plotly_chart(

                    fig,

                    use_container_width=True

                )

        st.dataframe(

            runtime_df,

            use_container_width=True,

            hide_index=True

        )

        st.divider()

        # =====================================================
        # Timeline Details
        # =====================================================

        st.subheader("Timeline Events")

        event_rows = []

        # Handle both dict and object timeline
        timeline_dict = (
            timeline.to_dict() 
            if hasattr(timeline, 'to_dict') 
            else (timeline if isinstance(timeline, dict) else {})
        )

        for name, value in timeline_dict.items():

            if name == "events":
                continue

            if isinstance(value, (int, float)):

                event_rows.append(

                    {

                        "Event": name,

                        "Duration (ms)": value,

                        "Duration":

                            format_duration(value)

                    }

                )

        if event_rows:

            event_df = pd.DataFrame(event_rows)

            st.dataframe(

                event_df,

                use_container_width=True,

                hide_index=True

            )

        else:

            st.info(

                "No timeline events available."

            )

        st.divider()

        # =====================================================
        # Runtime Observations
        # =====================================================

        st.subheader("Observations")

        if total_ms > 0:

            planning_pct = planning_ms * 100 / total_ms
            admission_pct = admission_ms * 100 / total_ms
            execution_pct = execution_ms * 100 / total_ms

            if planning_pct > PLANNING_PERCENT_THRESHOLD:
                st.warning(
                    f"Planning consumed {planning_pct:.1f}% of total runtime."
                )

            if admission_pct > ADMISSION_PERCENT_THRESHOLD:
                st.warning(
                    f"Admission wait consumed {admission_pct:.1f}%."
                )

            if execution_pct > EXECUTION_PERCENT_THRESHOLD:
                st.success(
                    "Execution phase dominates runtime."
                )

        if scan.get("files_scanned", 0) > FILES_SCANNED_THRESHOLD:
            st.warning(
                f"{scan.get('files_scanned'):,} files were scanned."
            )

        if memory.get("spill_detected"):
            st.error(
                "Memory spill detected."
            )

        if profile.query_info.state.upper() != "FINISHED":
            st.error(
                f"Query finished with state {profile.query_info.state}"
            )


    # ============================================================
    # Fragment Analytics
    # ============================================================

    elif page == "🧩 Fragment Analytics":

        st.title("🧩 Fragment Analytics")

        instances = profile.fragment_instances

        if not instances:

            st.warning("No fragment instances extracted.")

            st.stop()

        # --------------------------------------------------------
        # Build dataframe
        # --------------------------------------------------------

        rows = []

        for f in instances:

            rows.append(
                {
                    "Fragment": getattr(f, "fragment", "UNKNOWN"),
                    "Instance": getattr(f, "instance_id", ""),
                    "Host": getattr(f, "host", "UNKNOWN"),
                    "Operator": getattr(f, "operator", "UNKNOWN"),  # May not exist
                    "Runtime (s)": round(
                        getattr(f, "runtime_ms", 0) / 1000,
                        2
                    ),
                    "Rows": getattr(f, "rows", 0),
                    "Read MB": round(
                        getattr(f, "read_bytes", 0) / (1024**2),
                        2
                    ),
                    "Write MB": round(
                        getattr(f, "write_bytes", 0) / (1024**2),
                        2
                    ),
                    "Peak Memory MB": round(
                        getattr(f, "peak_memory", 0) / (1024**2),
                        2
                    ),
                    "Network ms": getattr(f, "network_send_ms", 0) + getattr(f, "network_receive_ms", 0),
                    "IO Wait ms": getattr(f, "io_wait_ms", 0)
                }
            )

        fragment_df = pd.DataFrame(rows)

        # --------------------------------------------------------
        # KPIs
        # --------------------------------------------------------

        total_fragments = len(fragment_df)
        total_hosts = fragment_df["Host"].nunique()
        avg_runtime = fragment_df["Runtime (s)"].mean()
        max_runtime = fragment_df["Runtime (s)"].max()

        # Safely compute skew ratio
        if pd.isna(avg_runtime) or avg_runtime <= 0:
            skew_ratio = 0.0
        else:
            skew_ratio = max_runtime / avg_runtime if pd.notna(max_runtime) else 0.0

        c1, c2, c3, c4 = st.columns(4)
        c1.metric(
            "Fragment Instances",
            total_fragments
        )
        c2.metric(
            "Hosts",
            total_hosts
        )
        c3.metric(
            "Average Runtime",
            f"{avg_runtime:.2f}s" if pd.notna(avg_runtime) else "N/A"
        )
        c4.metric(
            "Runtime Skew",
            f"{skew_ratio:.2f}x" if not pd.isna(skew_ratio) else "N/A"
        )

        if skew_ratio > 3:

            st.error(
                "Severe runtime skew detected."
            )

        elif skew_ratio > 2:

            st.warning(
                "Moderate runtime skew detected."
            )

        else:

            st.success(
                "Runtime distribution is balanced."
            )

        st.divider()

        # --------------------------------------------------------
        # Runtime Distribution
        # --------------------------------------------------------

        st.subheader("Fragment Runtime")

        runtime_df = (

            fragment_df

            .groupby("Fragment")["Runtime (s)"]

            .max()

            .reset_index()

            .sort_values(

                "Runtime (s)",

                ascending=False

            )

        )

        st.bar_chart(

            runtime_df.set_index("Fragment")

        )

        # --------------------------------------------------------
        # Host Distribution
        # --------------------------------------------------------

        st.subheader("Fragment Distribution by Host")

        host_df = (

            fragment_df

            .groupby("Host")

            .size()

            .reset_index(name="Fragments")

            .sort_values(

                "Fragments",

                ascending=False

            )

        )

        st.bar_chart(

            host_df.set_index("Host")

        )

        # --------------------------------------------------------
        # Memory Distribution
        # --------------------------------------------------------

        st.subheader("Peak Memory by Fragment")

        mem_df = (

            fragment_df

            .groupby("Fragment")["Peak Memory MB"]

            .max()

            .reset_index()

            .sort_values(

                "Peak Memory MB",

                ascending=False

            )

        )

        st.bar_chart(

            mem_df.set_index("Fragment")

        )

        # --------------------------------------------------------
        # Runtime vs Memory
        # --------------------------------------------------------

        st.subheader("Runtime vs Memory")

        scatter = px.scatter(

            fragment_df,

            x="Runtime (s)",

            y="Peak Memory MB",

            color="Fragment",

            hover_data=[

                "Host",

                "Operator"

            ],

            size="Rows"

        )

        st.plotly_chart(

            scatter,

            use_container_width=True

        )

        # --------------------------------------------------------
        # Operator Distribution
        # --------------------------------------------------------

        st.subheader("Operator Distribution")

        operator_df = (

            fragment_df

            .groupby("Operator")

            .size()

            .reset_index(name="Count")

            .sort_values(

                "Count",

                ascending=False

            )

        )

        fig = px.bar(

            operator_df,

            x="Operator",

            y="Count"

        )

        st.plotly_chart(

            fig,

            use_container_width=True

        )

        # --------------------------------------------------------
        # Top Runtime Fragments
        # --------------------------------------------------------

        st.subheader("Top Runtime Fragments")

        st.dataframe(

            runtime_df.head(15),

            use_container_width=True,

            hide_index=True

        )

        # --------------------------------------------------------
        # Largest Memory Consumers
        # --------------------------------------------------------

        st.subheader("Largest Memory Consumers")

        st.dataframe(

            mem_df.head(15),

            use_container_width=True,

            hide_index=True

        )

        # --------------------------------------------------------
        # Fragment Leaderboard
        # --------------------------------------------------------

        st.subheader("Fragment Leaderboard")

        leaderboard = (

            fragment_df

            .sort_values(

                "Runtime (s)",

                ascending=False

            )

        )

        # Optional AgGrid

        try:

            from st_aggrid import AgGrid

            from st_aggrid import GridOptionsBuilder

            gb = GridOptionsBuilder.from_dataframe(
                leaderboard
            )

            gb.configure_pagination()

            gb.configure_default_column(
                sortable=True,
                filter=True,
                resizable=True
            )

            gb.configure_selection(
                "single"
            )

            AgGrid(

                leaderboard,

                gridOptions=gb.build(),

                height=500,

                fit_columns_on_grid_load=True

            )

        except ImportError as e:
            
            import logging
            logger = logging.getLogger(__name__)
            logger.warning(f"AgGrid not available: {e}. Falling back to standard dataframe.")

            st.dataframe(

                leaderboard,

                use_container_width=True,

                height=500

            )
        
        except Exception as e:
            
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Error rendering AgGrid: {e}", exc_info=True)
            
            st.error(f"Error rendering advanced table: {e}")
            
            st.dataframe(

                leaderboard,

                use_container_width=True,

                height=500

            )

        # --------------------------------------------------------
        # Raw Fragment JSON
        # --------------------------------------------------------

        with st.expander("Raw Fragment Objects"):

            st.json(

                [

                    f.to_dict()

                    for f in instances

                ]

            )

    # ============================================================
    # Resource Utilization Dashboard
    # ============================================================

    elif page == "📈 Resource Utilization":

        st.title("📈 Resource Utilization Dashboard")

        memory = profile.memory_metrics or {}
        cpu = profile.cpu_metrics or []
        network = profile.network_metrics or {}
        scan = profile.scan_metrics or {}
        fragments = profile.fragment_instances or []

        # =========================================================
        # Resource KPIs
        # =========================================================

        peak_memory = memory.get(
            "peak_memory_gb",
            0
        )

        cpu_seconds = sum(
            x.get("cpu_seconds", 0)
            for x in cpu
        )

        bytes_sent = network.get(
            "bytes_sent",
            0
        )

        bytes_received = network.get(
            "bytes_received",
            0
        )

        rows_read = scan.get(
            "rows_read",
            0
        )

        c1, c2, c3, c4, c5 = st.columns(5)

        c1.metric(
            "Peak Memory",
            f"{peak_memory:.2f} GB"
        )

        c2.metric(
            "CPU Time",
            f"{cpu_seconds:.2f}s"
        )

        c3.metric(
            "Bytes Sent",
            f"{bytes_sent:.2f} MB"
        )

        c4.metric(
            "Bytes Received",
            f"{bytes_received:.2f} MB"
        )

        c5.metric(
            "Rows Read",
            f"{rows_read:,}"
        )

        st.divider()

        # =========================================================
        # CPU Analysis
        # =========================================================

        st.header("CPU Utilization")

        if cpu and len(cpu) > 0:

            try:
                cpu_df = pd.DataFrame(cpu)
                
                # Validate required columns exist
                required_columns = ["host", "cpu_seconds"]
                if not all(col in cpu_df.columns for col in required_columns):
                    st.warning("CPU metrics are incomplete. Required columns: host, cpu_seconds")
                    st.stop()

                st.dataframe(
                    cpu_df,
                    use_container_width=True,
                    hide_index=True
                )

                st.bar_chart(
                    cpu_df.set_index("host")[
                        "cpu_seconds"
                    ]
                )

                total_cpu = cpu_df[
                    "cpu_seconds"
                ].sum()

                if total_cpu > 0:
                    cpu_df["CPU %"] = (
                        cpu_df["cpu_seconds"] / total_cpu * 100
                        )

                    fig = px.pie(
                        cpu_df,
                        names="host",
                        values="CPU %",
                        hole=0.4,
                        title="CPU Distribution"
                    )

                    st.plotly_chart(
                        fig,
                        use_container_width=True
                    )

                    max_cpu = cpu_df["CPU %"].max()

                    if max_cpu > 80:
                        st.warning(
                            "CPU workload is highly concentrated on one executor."
                        )
            
            except Exception as e:
                import logging
                logging.error(f"Error processing CPU metrics: {e}", exc_info=True)
                st.error(f"Error processing CPU metrics: {e}")

        else:

            st.info(
                "No CPU metrics available."
            )

        # =========================================================
        # Network Analysis
        # =========================================================

        st.header("Network Utilization")

        nc1, nc2, nc3, nc4 = st.columns(4)

        nc1.metric(
            "Bytes Sent",
            f"{bytes_sent:.2f} MB"
        )

        nc2.metric(
            "Bytes Received",
            f"{bytes_received:.2f} MB"
        )

        nc3.metric(
            "RPC Write Time",
            f"{network.get('rpc_write_time',0):.2f}s"
        )

        nc4.metric(
            "RPC Read Time",
            f"{network.get('rpc_read_time',0):.2f}s"
        )

        network_df = pd.DataFrame(
            [

                {
                    "Metric":"Bytes Sent",
                    "Value":bytes_sent
                },

                {
                    "Metric":"Bytes Received",
                    "Value":bytes_received
                }

            ]

        )

        st.bar_chart(
            network_df.set_index("Metric")
        )

        total_network = (
            bytes_sent +
            bytes_received
        )

        if total_network < 100:

            st.success(
                "Network utilization is low."
            )

        elif total_network < 1000:

            st.info(
                "Moderate network activity."
            )

        else:

            st.warning(
                "Heavy network traffic detected."
            )

        st.divider()

        # =========================================================
        # Host Memory Distribution
        # =========================================================

        st.header("Host Memory Distribution")

        host_memory = {}

        for inst in fragments:

            host = inst.host

            peak = inst.peak_memory_mb

            host_memory[host] = max(

                host_memory.get(host, 0),

                peak

            )

        if host_memory:

            host_df = pd.DataFrame(

                {

                    "Host": list(host_memory.keys()),

                    "Peak Memory MB": list(host_memory.values())

                }

            )

            st.bar_chart(

                host_df.set_index("Host")

            )

            fig = px.bar(

                host_df,

                x="Host",

                y="Peak Memory MB",

                color="Peak Memory MB",

                title="Peak Memory by Host"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        st.divider()

        # =========================================================
        # Fragment Memory Distribution
        # =========================================================

        st.header("Fragment Memory Distribution")

        frag_rows = []

        for f in fragments:

            frag_rows.append(

                {

                    "Fragment": f.fragment,

                    "Memory MB": f.peak_memory_mb,

                    "Runtime": round(
                        f.runtime_ms / 1000,
                        2
                    )

                }

            )

        if frag_rows:

            frag_df = pd.DataFrame(frag_rows)

            fig = px.scatter(

                frag_df,

                x="Runtime",

                y="Memory MB",

                color="Fragment",

                size="Memory MB"

            )

            st.plotly_chart(

                fig,

                use_container_width=True

            )

        st.divider()

        # =========================================================
        # Operator Memory Ranking
        # =========================================================

        st.header("Operator Memory Ranking")

        if profile.operator_metrics:

            operator_df = pd.DataFrame(
                profile.operator_metrics
            )

            memory_column = None

            for c in operator_df.columns:

                if "memory" in c.lower():

                    memory_column = c

                    break

            if memory_column:

                operator_df = operator_df.sort_values(

                    memory_column,

                    ascending=False

                )

            st.dataframe(

                operator_df,

                use_container_width=True

            )

        else:

            st.info(
                "No operator metrics available."
            )

        st.divider()

        # =========================================================
        # Detailed Memory Dashboard
        # =========================================================

        render_memory_breakdown(profile)

        st.divider()

        # =========================================================
        # Resource Health Summary
        # =========================================================

        st.header("Resource Health")

        issues = []

        if peak_memory > 50:

            issues.append(
                "Very high memory consumption."
            )

        if memory.get(
            "spill_detected",
            False
        ):

            issues.append(
                "Memory spill detected."
            )

        if total_network > 1000:

            issues.append(
                "High network utilization."
            )

        if cpu_seconds > 3600:

            issues.append(
                "Large CPU consumption."
            )

        if not issues:

            st.success(
                "No obvious resource bottlenecks detected."
            )

        else:

            for issue in issues:

                st.warning(issue)

        st.divider()

        # =========================================================
        # Raw Metrics
        # =========================================================

        with st.expander("Raw Resource Metrics"):

            st.json({

                "memory": memory,

                "cpu": cpu,

                "network": network,

                "scan": scan

            })

    # ============================================================
    # Query Plan Summary
    # ============================================================

    elif page == "🗺️ Query Plan":

        st.title("🗺️ Query Plan Summary")

        exec_summary = profile.exec_summary

        if (
            exec_summary is None
            or
            not exec_summary.fragments
        ):
            st.warning(
                "ExecSummary not available."
            )
            st.stop()

        # ========================================================
        # Executive KPIs
        # ========================================================

        operator_count = sum(
            f.operator_count
            for f in exec_summary.fragments
        )

        fragment_count = exec_summary.fragment_count

        instance_count = exec_summary.total_instances

        host_count = exec_summary.total_hosts

        peak_memory = sum(
            f.total_peak_memory_mb
            for f in exec_summary.fragments
        )

        longest_runtime = max(
            (
                f.max_operator_time_ms
                for f in exec_summary.fragments
            ),
            default=0
        )

        c1, c2, c3, c4, c5, c6 = st.columns(6)

        c1.metric(
            "Fragments",
            fragment_count
        )

        c2.metric(
            "Operators",
            operator_count
        )

        c3.metric(
            "Instances",
            instance_count
        )

        c4.metric(
            "Hosts",
            host_count
        )

        c5.metric(
            "Peak Memory",
            f"{peak_memory:.1f} MB"
        )

        c6.metric(
            "Longest Operator",
            format_duration(longest_runtime)
        )

        st.divider()

        # ========================================================
        # Fragment Overview
        # ========================================================

        st.subheader(
            "Fragment Overview"
        )

        fragment_rows = []

        for fragment in exec_summary.fragments:

            fragment_rows.append(

                {

                    "Fragment":
                        fragment.fragment_id,

                    "Operators":
                        fragment.operator_count,

                    "Hosts":
                        fragment.host_count,

                    "Instances":
                        fragment.instance_count,

                    "Rows":
                        fragment.total_rows,

                    "Peak Memory MB":
                        fragment.total_peak_memory_mb,

                    "Longest Operator":
                        round(
                            fragment.max_operator_time_ms
                            / 1000,
                            2
                        )

                }

            )

        fragment_df = pd.DataFrame(
            fragment_rows
        )

        st.dataframe(
            fragment_df,
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            fragment_df.set_index(
                "Fragment"
            )[
                "Peak Memory MB"
            ]
        )

        st.divider()

        # ========================================================
        # Query Plan Tree
        # ========================================================

        st.subheader(
            "Fragment Topology"
        )

        for fragment in exec_summary.fragments:

            with st.expander(
                f"{fragment.fragment_id} "
                f"({fragment.operator_count} operators)"
            ):

                for operator in fragment.operators:

                    cols = st.columns(
                        [4, 2, 2, 2]
                    )

                    cols[0].markdown(
                        f"**{operator.operator_type}**"
                    )

                    cols[1].write(
                        format_duration(
                            operator.max_time_ms
                        )
                    )

                    cols[2].write(
                        f"{operator.peak_memory_mb:.1f} MB"
                    )

                    cols[3].write(
                        f"{operator.rows_produced:,}"
                    )

        st.divider()

        # ========================================================
        # Operator Leaderboard
        # ========================================================

        st.subheader(
            "Operator Leaderboard"
        )

        operators = []

        for fragment in exec_summary.fragments:

            for operator in fragment.operators:

                operators.append(

                    {

                        "Fragment":
                            fragment.fragment_id,

                        "Operator":
                            operator.operator_type,

                        "Runtime ms":
                            operator.max_time_ms,

                        "Rows":
                            operator.rows_produced,

                        "Peak Memory MB":
                            operator.peak_memory_mb,

                        "Estimated MB":
                            operator.est_peak_memory_mb

                    }

                )

        operator_df = pd.DataFrame(
            operators
        )

        operator_df = operator_df.sort_values(
            "Runtime ms",
            ascending=False
        )

        st.dataframe(
            operator_df,
            use_container_width=True,
            hide_index=True
        )

        st.divider()

        # ========================================================
        # Runtime Heatmap
        # ========================================================

        st.subheader(
            "Runtime by Operator"
        )

        runtime_chart = px.bar(

            operator_df,

            x="Runtime ms",

            y="Operator",

            color="Fragment",

            orientation="h"

        )

        st.plotly_chart(
            runtime_chart,
            use_container_width=True
        )

        # ========================================================
        # Memory Heatmap
        # ========================================================

        st.subheader(
            "Peak Memory by Operator"
        )

        memory_chart = px.bar(

            operator_df.sort_values(
                "Peak Memory MB",
                ascending=False
            ),

            x="Peak Memory MB",

            y="Operator",

            color="Fragment",

            orientation="h"

        )

        st.plotly_chart(
            memory_chart,
            use_container_width=True
        )

        st.divider()

        # ========================================================
        # Operator Mix
        # ========================================================

        st.subheader(
            "Operator Distribution"
        )

        mix = (

            operator_df

            .groupby("Operator")

            .size()

            .reset_index(
                name="Count"
            )

        )

        pie = px.pie(

            mix,

            names="Operator",

            values="Count",

            hole=.45

        )

        st.plotly_chart(
            pie,
            use_container_width=True
        )

        st.divider()

        # ========================================================
        # Fragment Balance
        # ========================================================

        st.subheader(
            "Fragment Balance"
        )

        fig = px.scatter(

            fragment_df,

            x="Rows",

            y="Peak Memory MB",

            color="Fragment",

            size="Longest Operator"

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.divider()

        # ========================================================
        # Complexity Score
        # ========================================================

        joins = (
            operator_df.Operator
            .str.contains(
                "JOIN",
                case=False,
                na=False
            )
            .sum()
        )

        scans = (
            operator_df.Operator
            .str.contains(
                "SCAN",
                case=False,
                na=False
            )
            .sum()
        )

        exchanges = (
            operator_df.Operator
            .str.contains(
                "EXCHANGE",
                case=False,
                na=False
            )
            .sum()
        )

        sorts = (
            operator_df.Operator
            .str.contains(
                "SORT",
                case=False,
                na=False
            )
            .sum()
        )

        complexity = min(

            100,

            (
                fragment_count * 6
                +
                operator_count * 2
                +
                joins * 10
                +
                scans * 3
                +
                exchanges * 5
                +
                sorts * 6
            )

        )

        st.subheader(
            "Query Complexity"
        )

        st.progress(
            complexity / 100
        )

        st.metric(
            "Complexity Score",
            f"{complexity}/100"
        )

        reasons = []

        reasons.append(
            f"{fragment_count} fragments"
        )

        reasons.append(
            f"{operator_count} operators"
        )

        reasons.append(
            f"{joins} joins"
        )

        reasons.append(
            f"{exchanges} exchanges"
        )

        reasons.append(
            f"{sorts} sorts"
        )

        reasons.append(
            f"{scans} scans"
        )

        for r in reasons:

            st.write("•", r)

        st.divider()

        # ========================================================
        # Raw ExecSummary
        # ========================================================

        with st.expander(
            "Raw ExecSummary"
        ):

            st.json(
                exec_summary.to_dict()
            )

    # ============================================================
    # Findings • Root Cause Analysis • Recommendations
    # ============================================================

    elif page == "🔍 Findings":

        st.header("AI Findings & Root Cause Analysis")

        findings = analytics.get("findings", [])

        intelligence_result = intelligence

        root_causes = intelligence_result.get(
            "root_causes",
            []
        )

        recommendations = intelligence_result.get(
            "recommendations",
            []
        )

        summary = intelligence_result.get(
            "summary",
            ""
        )

        # --------------------------------------------------
        # Executive Summary
        # --------------------------------------------------

        if summary:

            st.subheader("Executive Summary")

            st.info(summary)

        # --------------------------------------------------
        # Findings
        # --------------------------------------------------

        st.divider()

        st.subheader("Detected Findings")

        if not findings:

            st.success(
                "No performance issues detected."
            )

        else:

            for finding in findings:

                if isinstance(finding, dict):

                    severity = finding.get(
                        "severity",
                        "medium"
                    ).lower()

                    title = finding.get(
                        "title",
                        "Finding"
                    )

                    description = finding.get(
                        "description",
                        ""
                    )

                else:

                    severity = getattr(
                        finding,
                        "severity",
                        "medium"
                    ).lower()

                    title = getattr(
                        finding,
                        "title",
                        "Finding"
                    )

                    description = getattr(
                        finding,
                        "description",
                        ""
                    )

                if severity == "critical":

                    st.error(f"🚨 {title}")

                elif severity == "high":

                    st.warning(f"⚠️ {title}")

                else:

                    st.info(f"ℹ️ {title}")

                if description:

                    st.write(description)

        # --------------------------------------------------
        # Root Cause Chain
        # --------------------------------------------------

        st.divider()

        st.subheader("Root Cause Chain")

        if chain:

            for index, step in enumerate(chain):

                st.markdown(f"### {step}")

                if index < len(chain) - 1:

                    st.markdown(
                        "<div style='text-align:center;font-size:26px;'>⬇️</div>",
                        unsafe_allow_html=True
                    )

        else:

            st.success(
                "No root cause chain generated."
            )

        # --------------------------------------------------
        # Root Causes
        # --------------------------------------------------

        st.divider()

        st.subheader("Root Causes")

        if not root_causes:

            st.success(
                "No root causes detected."
            )

        else:

            for cause in root_causes:

                with st.expander(
                    cause.title,
                    expanded=False
                ):

                    c1, c2, c3 = st.columns(3)

                    c1.metric(
                        "Severity",
                        cause.severity
                    )

                    c2.metric(
                        "Confidence",
                        f"{cause.confidence*100:.0f}%"
                    )

                    c3.metric(
                        "Impact Score",
                        cause.impact_score
                    )

                    if cause.evidence:

                        st.markdown(
                            "**Evidence**"
                        )

                        for evidence in cause.evidence:

                            st.write(
                                f"• {evidence}"
                            )

        # --------------------------------------------------
        # Recommendations
        # --------------------------------------------------

        st.divider()

        st.subheader("Recommendations")

        if not recommendations:

            st.success(
                "No recommendations."
            )

        else:

            for rec in recommendations:

                with st.container():

                    st.markdown(
                        f"### ✅ {rec.title}"
                    )

                    st.write(
                        rec.description
                    )

                    st.caption(
                        f"Priority : {rec.priority}"
                    )

        # --------------------------------------------------
        # Playbooks
        # --------------------------------------------------

        playbooks = intelligence_result.get(
            "playbooks",
            []
        )

        if playbooks:

            st.divider()

            st.subheader("Operational Playbooks")

            for pb in playbooks:

                with st.expander(
                    pb.title,
                    expanded=False
                ):

                    st.write(
                        pb.description
                    )

                    if hasattr(pb, "steps"):

                        for step in pb.steps:

                            st.markdown(
                                f"- {step}"
                            )

    # ============================================================
    # Export Center
    # ============================================================

    elif page == "📤 Export":

        st.header("Export Center")

        st.write(
            "Export analysis results, metrics and reports."
        )

        import json
        import io

        # -------------------------------------------------------
        # Build Report Dictionary
        # -------------------------------------------------------

        report = {

            "query_info": {

                "query_id": profile.query_info.query_id,

                "user": profile.query_info.user,

                "state": profile.query_info.state,

                "coordinator": profile.query_info.coordinator,

                "start_time": profile.query_info.start_time,

                "end_time": profile.query_info.end_time,

                "duration": profile.query_info.duration,

                "pool": profile.query_info.pool,

                "query_type": profile.query_info.query_type
            },

            "timeline": profile.timeline.to_dict(),

            "scan_metrics": profile.scan_metrics,

            "memory_metrics": profile.memory_metrics,

            "network_metrics": profile.network_metrics,

            "analytics": analytics,

            "intelligence": {

                "summary":
                    intelligence.get(
                        "summary",
                        ""
                    ),

                "root_causes": [

                    {

                        "title": (
                            rc.get("title") if isinstance(rc, dict) 
                            else getattr(rc, "title", "Unknown")
                        ),

                        "severity": (
                            rc.get("severity") if isinstance(rc, dict)
                            else getattr(rc, "severity", "medium")
                        ),

                        "confidence": (
                            rc.get("confidence") if isinstance(rc, dict)
                            else getattr(rc, "confidence", 0.0)
                        ),

                        "impact_score": (
                            rc.get("impact_score") if isinstance(rc, dict)
                            else getattr(rc, "impact_score", 0)
                        ),

                        "evidence": (
                            rc.get("evidence") if isinstance(rc, dict)
                            else getattr(rc, "evidence", [])
                        )

                    }

                    for rc in intelligence.get(
                        "root_causes",
                        []
                    )

                ],

                "recommendations": [

                    {

                        "title": (
                            rec.get("title") if isinstance(rec, dict)
                            else getattr(rec, "title", "Unknown")
                        ),

                        "priority": (
                            rec.get("priority") if isinstance(rec, dict)
                            else getattr(rec, "priority", "medium")
                        ),

                        "description": (
                            rec.get("description") if isinstance(rec, dict)
                            else getattr(rec, "description", "")
                        )

                    }

                    for rec in intelligence.get(
                        "recommendations",
                        []
                    )

                ]

            }

        }

        # -------------------------------------------------------
        # Downloads
        # -------------------------------------------------------

        c1, c2 = st.columns(2)

        with c1:

            st.subheader("Export JSON")

            json_bytes = json.dumps(

                report,

                indent=2,

                default=str

            ).encode("utf-8")

            st.download_button(

                "⬇ Download JSON",

                data=json_bytes,

                file_name=f"{profile.query_info.query_id}.json",

                mime="application/json"

            )

        with c2:

            st.subheader("Export Query Summary")

            summary_text = intelligence.get(
                "summary",
                ""
            )

            st.download_button(

                "⬇ Download Summary",

                data=summary_text,

                file_name="executive_summary.txt",

                mime="text/plain"

            )

        st.divider()

        # -------------------------------------------------------
        # Fragment CSV
        # -------------------------------------------------------

        st.subheader("Fragment Metrics")

        fragment_rows = [

            x.to_dict()

            for x in profile.fragment_instances

        ]

        if fragment_rows:

            fragment_df = pd.DataFrame(

                fragment_rows

            )

            csv = fragment_df.to_csv(

                index=False

            ).encode()

            st.download_button(

                "⬇ Download Fragment CSV",

                csv,

                "fragment_metrics.csv",

                "text/csv"

            )

            st.dataframe(

                fragment_df,

                use_container_width=True

            )

        st.divider()

        # -------------------------------------------------------
        # Operator CSV
        # -------------------------------------------------------

        st.subheader("Operator Metrics")

        operator_df = pd.DataFrame(

            profile.operator_metrics

        )

        if not operator_df.empty:

            csv = operator_df.to_csv(

                index=False

            ).encode()

            st.download_button(

                "⬇ Download Operator CSV",

                csv,

                "operator_metrics.csv",

                "text/csv"

            )

            st.dataframe(

                operator_df,

                use_container_width=True

            )

        st.divider()

        # -------------------------------------------------------
        # CPU Metrics
        # -------------------------------------------------------

        st.subheader("CPU Metrics")

        cpu_df = pd.DataFrame(

            profile.cpu_metrics

        )

        if not cpu_df.empty:

            csv = cpu_df.to_csv(

                index=False

            ).encode()

            st.download_button(

                "⬇ Download CPU Metrics",

                csv,

                "cpu_metrics.csv",

                "text/csv"

            )

            st.dataframe(

                cpu_df,

                use_container_width=True

            )

        st.divider()

        # -------------------------------------------------------
        # Network Metrics
        # -------------------------------------------------------

        st.subheader("Network Metrics")

        network = profile.network_metrics

        network_df = pd.DataFrame(

            [

                network

            ]

        )

        csv = network_df.to_csv(

            index=False

        ).encode()

        st.download_button(

            "⬇ Download Network Metrics",

            csv,

            "network_metrics.csv",

            "text/csv"

        )

        st.dataframe(

            network_df,

            use_container_width=True

        )

        st.divider()

        # -------------------------------------------------------
        # Complete Profile
        # -------------------------------------------------------

        st.subheader("Raw Query Profile")

        st.download_button(

            "⬇ Download Original Profile",

            profile.raw_profile,

            "query.profile",

            "text/plain"

        )

        with st.expander(

            "View Original Profile",

            expanded=False

        ):

            st.text_area(

                "",

                profile.raw_profile,

                height=500

            )