def render_bar_chart_section(
    st,
    title: str,
    dataframe: pd.DataFrame,
    index_col: str,
    value_col: str
):
    """Helper to standardize bar chart rendering."""
    st.subheader(title)
    st.bar_chart(dataframe.set_index(index_col))

# Usage in app.py:
# render_bar_chart_section(st, "Fragment Runtime", runtime_df, "Fragment", "Runtime (s)")