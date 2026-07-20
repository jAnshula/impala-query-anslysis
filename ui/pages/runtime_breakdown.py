import pandas as pd
import plotly.express as px
import streamlit as st

def render_runtime_breakdown(runtime_breakdown):
    if not runtime_breakdown:
        return

    st.subheader("Runtime Breakdown")

    # Use combined labels for clarity
    df = pd.DataFrame([
        {"Phase": "Planning", "Runtime": runtime_breakdown["planning_label"]},
        {"Phase": "Admission", "Runtime": runtime_breakdown["admission_label"]},
        {"Phase": "Execution", "Runtime": runtime_breakdown["execution_label"]},
        {"Phase": "Total", "Runtime": runtime_breakdown["total_label"]},
    ])

    st.dataframe(df, use_container_width=True)

    # Pie chart with hover showing HH:MM:SS
    fig = px.pie(
        names=["Planning", "Admission", "Execution"],
        values=[
            runtime_breakdown["planning_pct"],
            runtime_breakdown["admission_pct"],
            runtime_breakdown["execution_pct"],
        ],
        title="Query Runtime Distribution",
        hover_data={"names": True}
    )
    fig.update_traces(
        textinfo="label+percent",
        hovertext=[
            runtime_breakdown["planning_label"],
            runtime_breakdown["admission_label"],
            runtime_breakdown["execution_label"],
        ]
    )

    st.plotly_chart(fig, use_container_width=True)

