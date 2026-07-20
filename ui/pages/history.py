# ui/pages/history.py

import streamlit as st
import pandas as pd

def render_history(repo):

    rows = repo.list_profiles()

    st.dataframe(
        pd.DataFrame(rows)
    )

