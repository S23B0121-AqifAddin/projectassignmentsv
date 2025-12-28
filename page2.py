import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px # Import Plotly Express

# --- Streamlit Application ---

st.set_page_config(
    page_title="Motorbike Accident Analysis",
    layout="wide" # Use wide layout for better visualization
)

st.title("Bangladesh Motorbike Accident")
st.subheader(" Objective : To profile the highest-risk rider population by age, education, and occupation to inform targeted safety campaigns and interventions.")

summary_text = "This group of visualizations focuses on the demographic profile of the bikers involved in the accident dataset. The analysis highlights that students are the most frequently represented occupation, followed by those with an Above high school education, indicating a strong skew towards a highly-educated demographic in the biking population or accident victims. The Distribution of Biker Age reveals a critical risk factor, with the majority of accidents occurring in the mid-to-late 20s, suggesting that younger, less-experienced adults are disproportionately at risk. This is confirmed by the histogram and box plot, which show a peak frequency in this age range and a right-skewed distribution. The key finding is that safety interventions should specifically target this younger, educated, and student population."
st.info(summary_text)
# 1. Load the dataset
try:
    # Attempt to load the real data
    # IMPORTANT: Update this path if your CSV is in a different location
    df = pd.read_csv("motorbike_accident_severity.csv")
except FileNotFoundError:
    # If the file is not found, create a dummy DataFrame for demonstration
    st.warning("Data file 'motorbike_accident_severity.csv' not found. Using comprehensive dummy data for demonstration.")
    
    # Dummy data structure must include all columns used later in the script
    data = {
        'Biker_Occupation': np.random.choice(['Student', 'Govt Employee', 'Self Employed', 'Private Employee', 'Others', 'Unemployed'], size=200),
        'Accident_Severity': np.random.choice(['Minor', 'Moderate', 'Major'], size=200),
        'Age_Band': np.random.choice(['<25', '25-45', '46-65', '>65'], size=200),
        'Biker_Education_Level': np.random.choice(['High School', 'Diploma', 'Bachelor\'s', 'Master\'s', 'PhD', 'None'], size=200),
        'Biker_Age': np.random.randint(16, 76, size=200) # Added numerical Biker_Age for histogram
    }
    df = pd.DataFrame(data)

st.header('1. Biker Occupation Distribution')
summary_text = "The highest frequency of bikers in the accident dataset are Students, followed by Others, Business, and Service occupations, which have similar frequencies. This suggests that the student demographic may be disproportionately involved in motorbike accidents compared to other occupational groups"
st.info(summary_text)

# --- CHART 1: Biker Occupation Distribution (Plotly Bar) ---
if 'Biker_Occupation' in df.columns:
    
    occupation_counts = df['Biker_Occupation'].value_counts().reset_index()
    occupation_counts.columns = ['Biker_Occupation', 'Count'] # Rename columns for clarity

    fig_occ = px.bar(
        occupation_counts,
        x='Biker_Occupation',
        y='Count',
        title='Distribution of Biker Occupation',
        labels={'Biker_Occupation': 'Biker Occupation', 'Count': 'Number of Bikers'},
        color='Biker_Occupation', # Color bars by occupation category
        color_discrete_sequence=px.colors.qualitative.D3 # A different color palette
    )

    # 3. Customize the plot (Plotly customizations)
    fig_occ.update_layout(
        xaxis_title_text='Biker Occupation', # X-axis title
        yaxis_title_text='Count',           # Y-axis title
        xaxis_tickangle=-45,                # Rotate x-axis labels
        hovermode="x unified"               # Improve hover behavior
    )

    # 4. Display the chart in Streamlit
    st.plotly_chart(fig_occ, use_container_width=True)
else:
    st.error("The DataFrame does not contain a 'Biker_Occupation' column for analysis.")


st.header('2. Biker Education Level Distribution')
summary_text = "The clear majority of bikers involved in the accidents have an Above high school education level. The count for High school is significantly lower, and Less than high school is the lowest. This could indicate a higher propensity for accidents among the more educated group, or simply that the biking population is predominantly educated above the high school level."
st.info(summary_text)

# --- CHART 2: Biker Education Level Distribution (Plotly Bar) ---
if 'Biker_Education_Level' in df.columns:

    # 1. Calculate counts
    education_counts = df['Biker_Education_Level'].value_counts().reset_index()
    education_counts.columns = ['Biker_Education_Level', 'Count']

    # 2. Create the Plotly figure
    fig_edu = px.bar(
        education_counts,
        x='Biker_Education_Level',
        y='Count',
        title='Distribution of Biker Education Level',
        labels={'Biker_Education_Level': 'Education Level', 'Count': 'Number of Bikers'},
        color='Biker_Education_Level', # Color bars by education category
        color_discrete_sequence=px.colors.qualitative.Plotly # Use a different palette for distinction
    )

    # 3. Customize the plot
    fig_edu.update_layout(
        xaxis_title_text='Biker Education Level',
        yaxis_title_text='Count',
        xaxis_tickangle=-45,
        hovermode="x unified"
    )

    # 4. Display the chart in Streamlit
    st.plotly_chart(fig_edu, use_container_width=True)
else:
    st.error("The DataFrame does not contain a 'Biker_Education_Level' column for analysis.")
    
st.header('3. Distribution of Biker Age')
summary_text = "The age distribution is right-skewed, meaning there is a tail extending towards older ages. The peak frequency of accidents occurs in the mid-to-late 20s (around 25-30 years old). The box plot confirms this, with the median (the line inside the box) and the highest bars clustering in this younger adult range. This highlights younger adults as the highest-risk age group for motorbike accidents"
st.info(summary_text)

# --- CHART 3: Biker Age Distribution (Plotly Histogram) ---
if 'Biker_Age' in df.columns:

    fig_age = px.histogram(
        df,
        x='Biker_Age',
        nbins=20,  # Set number of bins
        title='Distribution of Biker Age',
        labels={'Biker_Age': 'Biker Age', 'count': 'Frequency'},
        marginal='box', # Add a box plot on top for summary statistics
        color_discrete_sequence=['#E63946'], # Color changed to vibrant red for context
        opacity=0.8
    )

    fig_age.update_layout(
        xaxis_title_text='Biker Age',
        yaxis_title_text='Frequency',
        hovermode="x unified"
    )
    
    st.plotly_chart(fig_age, use_container_width=True)
else:
    st.error("The DataFrame does not contain a 'Biker_Age' column for analysis.")
