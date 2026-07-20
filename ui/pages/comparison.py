# ui/pages/comparison.py

import streamlit as st

def render_comparison(
    comparison,
    regressions
):

    st.subheader(
        "Comparison"
    )

    st.write(comparison)

    if regressions:

        st.error(
            "\n".join(regressions)
        )

