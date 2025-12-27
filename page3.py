import streamlit as st
import pandas as pd


# --- Data Loading and Caching ---
DATA_URL = "https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv"

@st.cache_data
def load_data(url):
    """Loads and returns the DataFrame from the specified URL."""
    try:
        data = pd.read_csv(url)
        # Drop any unnamed columns that might result from CSV indexing
        data = data.loc[:, ~data.columns.str.contains('^Unnamed')]
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data(DATA_URL)
