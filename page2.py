import streamlit as st
import pandas as pd
import plotly.express as px


# --- Corrected Imports ---
import plotly.graph_objects as go # Keep this if you need go, though px handles everything here

# Set Streamlit page configuration (must be the first Streamlit command)
st.set_page_config(
    page_title="Financial Behaviour among University Students",
    layout="wide" # Set layout here for consistency
)

# Page header
st.header("Financial Behaviour among University Students", divider="grey")

col1, col2, col3, col4 = st.columns(4)
    
col1.metric(label="PLO 2", value=f"3.3", help="PLO 2: Cognitive Skill", border=True)
col2.metric(label="PLO 3", value=f"3.5", help="PLO 3: Digital Skill", border=True)
col3.metric(label="PLO 4", value=f"4.0", help="PLO 4: Interpersonal Skill", border=True)
col4.metric(label="PLO 5", value=f"4.3", help="PLO 5: Communication Skill", border=True)

# Load your data
try:
    df2 = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='utf-8')
except UnicodeDecodeError:
    df2 = pd.read_csv('https://raw.githubusercontent.com/S23B0121-AqifAddin/projectassignmentsv/refs/heads/main/processed_financial_capability_data.csv', encoding='latin-1')
df2


# Create the countplot
    sns.countplot(
        data=data, 
        x='Compare_Prices_Before_Buying', 
        order=data['Compare_Prices_Before_Buying'].value_counts().index, 
        palette='viridis',
        ax=ax  # It is best practice to specify the axis in Streamlit
    )
    
    # Customizing labels
    ax.set_title('Decision Planning Frequency (Compare Prices Before Buying)', fontsize=14)
    ax.set_xlabel('Response', fontsize=12)
    ax.set_ylabel('Count', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # 4. Display the plot in Streamlit
    st.pyplot(fig)

# Call the function
if 'df' in locals() or 'df' in globals():
    plot_price_comparison(df)
else:
    st.error("Dataframe 'df' not found. Please ensure your data is loaded.")
