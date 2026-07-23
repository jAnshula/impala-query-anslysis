"""
Chart rendering helper functions to reduce code duplication.
Provides consistent, reusable components for common visualization patterns.
"""

import pandas as pd
import plotly.express as px
import streamlit as st
from typing import Optional, List, Dict, Any


def render_bar_chart(
    df: pd.DataFrame,
    index_col: str,
    value_col: str,
    title: Optional[str] = None,
    use_plotly: bool = False,
    color_col: Optional[str] = None,
    orientation: str = "v"
) -> None:
    """
    Render a bar chart with consistent styling.
    
    Args:
        df: DataFrame containing the data
        index_col: Column name to use as index/x-axis
        value_col: Column name to use as values/y-axis
        title: Optional chart title
        use_plotly: If True, use Plotly (interactive); if False, use Streamlit (simple)
        color_col: Optional column for color encoding
        orientation: 'v' for vertical, 'h' for horizontal
        
    Example:
        >>> runtime_df = pd.DataFrame({
        ...     "Fragment": ["F0", "F1", "F2"],
        ...     "Runtime (s)": [5.2, 3.1, 4.8]
        ... })
        >>> render_bar_chart(runtime_df, "Fragment", "Runtime (s)", title="Fragment Runtimes")
    """
    if df.empty:
        st.warning("No data available to render chart.")
        return
    
    if use_plotly:
        # Interactive Plotly chart
        fig = px.bar(
            df,
            x=index_col if orientation == "v" else value_col,
            y=value_col if orientation == "v" else index_col,
            color=color_col,
            title=title,
            orientation=orientation,
            labels={index_col: index_col, value_col: value_col}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        # Simple Streamlit bar chart
        if df[value_col].sum() == 0:
            st.info("All values are zero.")
            return
        st.bar_chart(df.set_index(index_col))


def render_pie_chart(
    df: pd.DataFrame,
    names_col: str,
    values_col: str,
    title: Optional[str] = None,
    hole: float = 0.0
) -> None:
    """
    Render a pie chart with consistent styling.
    
    Args:
        df: DataFrame containing the data
        names_col: Column name for labels
        values_col: Column name for values
        title: Optional chart title
        hole: Donut hole size (0.0 = pie chart, 0.45 = donut)
        
    Example:
        >>> runtime_df = pd.DataFrame({
        ...     "Phase": ["Planning", "Admission", "Execution"],
        ...     "Duration (ms)": [1000, 500, 5000]
        ... })
        >>> render_pie_chart(runtime_df, "Phase", "Duration (ms)", title="Runtime Distribution")
    """
    if df.empty or df[values_col].sum() == 0:
        st.warning("No data available to render pie chart.")
        return
    
    fig = px.pie(
        df,
        names=names_col,
        values=values_col,
        title=title,
        hole=hole
    )
    st.plotly_chart(fig, use_container_width=True)


def render_scatter_chart(
    df: pd.DataFrame,
    x_col: str,
    y_col: str,
    color_col: Optional[str] = None,
    size_col: Optional[str] = None,
    hover_data: Optional[List[str]] = None,
    title: Optional[str] = None
) -> None:
    """
    Render a scatter plot with consistent styling.
    
    Args:
        df: DataFrame containing the data
        x_col: Column name for X-axis
        y_col: Column name for Y-axis
        color_col: Optional column for color encoding
        size_col: Optional column for bubble size
        hover_data: Optional list of columns for hover information
        title: Optional chart title
        
    Example:
        >>> fragment_df = pd.DataFrame({
        ...     "Runtime (s)": [1.5, 2.3, 1.2],
        ...     "Peak Memory MB": [500, 800, 450],
        ...     "Fragment": ["F0", "F1", "F2"],
        ...     "Rows": [1000, 2500, 800]
        ... })
        >>> render_scatter_chart(
        ...     fragment_df,
        ...     x_col="Runtime (s)",
        ...     y_col="Peak Memory MB",
        ...     color_col="Fragment",
        ...     size_col="Rows",
        ...     hover_data=["Fragment", "Rows"],
        ...     title="Runtime vs Memory"
        ... )
    """
    if df.empty:
        st.warning("No data available to render scatter plot.")
        return
    
    fig = px.scatter(
        df,
        x=x_col,
        y=y_col,
        color=color_col,
        size=size_col,
        hover_data=hover_data,
        title=title
    )
    st.plotly_chart(fig, use_container_width=True)


def render_dual_chart_section(
    st,
    df: pd.DataFrame,
    title: str,
    simple_chart: Dict[str, str],
    plotly_chart: Dict[str, Any]
) -> None:
    """
    Render side-by-side simple and interactive chart versions.
    
    Args:
        st: Streamlit module
        df: DataFrame with data
        title: Section title
        simple_chart: Dict with 'index_col' and 'value_col' for simple chart
        plotly_chart: Dict with kwargs for px.pie/px.bar
        
    Example:
        >>> st.subheader("Runtime Breakdown")
        >>> left, right = st.columns([2, 1])
        >>> with left:
        ...     render_bar_chart(runtime_df, "Phase", "Duration (ms)")
        >>> with right:
        ...     render_pie_chart(runtime_df, "Phase", "Duration (ms)", hole=0.45)
    """
    st.subheader(title)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_bar_chart(
            df,
            index_col=simple_chart['index_col'],
            value_col=simple_chart['value_col'],
            use_plotly=False
        )
    
    with col2:
        if plotly_chart.get('type') == 'pie':
            render_pie_chart(
                df,
                names_col=plotly_chart['names_col'],
                values_col=plotly_chart['values_col'],
                title=plotly_chart.get('title'),
                hole=plotly_chart.get('hole', 0.45)
            )


def render_metrics_row(
    st,
    metrics: Dict[str, Any],
    columns: int = 4
) -> None:
    """
    Render multiple metrics in a row with consistent styling.
    
    Args:
        st: Streamlit module
        metrics: Dict of {label: value} pairs
        columns: Number of columns to span
        
    Example:
        >>> metrics = {
        ...     "Fragment Instances": 24,
        ...     "Hosts": 4,
        ...     "Average Runtime": "2.5s",
        ...     "Runtime Skew": "3.2x"
        ... }
        >>> render_metrics_row(st, metrics, columns=4)
    """
    cols = st.columns(columns)
    
    for idx, (label, value) in enumerate(metrics.items()):
        if idx < len(cols):
            cols[idx].metric(label, value)


def render_dataframe_with_download(
    st,
    df: pd.DataFrame,
    filename: str,
    title: Optional[str] = None
) -> None:
    """
    Render a dataframe with download button.
    
    Args:
        st: Streamlit module
        df: DataFrame to display
        filename: Base filename for CSV (will add .csv extension)
        title: Optional section title
        
    Example:
        >>> render_dataframe_with_download(
        ...     st,
        ...     fragment_df,
        ...     "fragment_metrics",
        ...     title="Fragment Metrics"
        ... )
    """
    if title:
        st.subheader(title)
    
    if df.empty:
        st.info("No data available.")
        return
    
    # Download button
    csv = df.to_csv(index=False).encode()
    st.download_button(
        label=f"⬇ Download {filename.replace('_', ' ').title()}",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv"
    )
    
    # Display dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )


def render_section_divider(st) -> None:
    """Add a visual divider between sections."""
    st.divider()


def get_safe_dataframe_value(
    df: pd.DataFrame,
    column: str,
    default: Any = 0
) -> Any:
    """
    Safely extract a single aggregated value from a dataframe column.
    
    Args:
        df: DataFrame to extract from
        column: Column name
        default: Default value if column doesn't exist or is empty
        
    Returns:
        Sum of column values, or default if unavailable
    """
    if df.empty or column not in df.columns:
        return default
    
    try:
        return df[column].sum()
    except (TypeError, ValueError):
        return default


def validate_dataframe_columns(
    df: pd.DataFrame,
    required_columns: List[str],
    context: str = ""
) -> bool:
    """
    Validate that dataframe contains required columns.
    
    Args:
        df: DataFrame to validate
        required_columns: List of column names that must exist
        context: Context string for error message
        
    Returns:
        True if valid, False otherwise
        
    Example:
        >>> if not validate_dataframe_columns(
        ...     cpu_df,
        ...     ["host", "cpu_seconds"],
        ...     context="CPU metrics"
        ... ):
        ...     st.stop()
    """
    if df.empty:
        st.warning(f"{context}: DataFrame is empty.")
        return False
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.warning(
            f"{context}: Missing required columns: {', '.join(missing_columns)}"
        )
        return False
    
    return True
