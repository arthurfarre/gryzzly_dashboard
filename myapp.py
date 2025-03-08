import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
file_path = "export_gryzzly_20250221_projects_from-20240101_to-20241231 (1).xlsx"
xls = pd.ExcelFile(file_path)
df_projects = pd.read_excel(xls, sheet_name='projects')
df_declarations = pd.read_excel(xls, sheet_name='declarations')

# Convert date columns to datetime format
df_declarations['Entry date'] = pd.to_datetime(df_declarations['Entry date'])
df_projects['Start date'] = pd.to_datetime(df_projects['Start date'])

# Aggregate total declared hours per project
project_hours = df_declarations.groupby("Project name")["Duration"].sum().reset_index()
project_hours = project_hours.sort_values(by="Duration", ascending=False)

# Aggregate total declared hours per user
user_hours = df_declarations.groupby("Username")["Duration"].sum().reset_index()
user_hours = user_hours.sort_values(by="Duration", ascending=False)

# Aggregate total declared cost per project
project_costs = df_declarations.groupby("Project name")["Entry cost"].sum().reset_index()
project_costs = project_costs.sort_values(by="Entry cost", ascending=False)

# Streamlit UI - Modern Theme
st.set_page_config(page_title="Gryzzly Dashboard", page_icon="📊", layout="wide")

# Custom CSS for a modern UI
st.markdown("""
    <style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f4;
    }
    .block-container {
        max-width: 1200px;
        padding: 2rem;
        background: white;
        border-radius: 10px;
        box-shadow: 0px 4px 15px rgba(0, 0, 0, 0.1);
    }
    .stTextInput>div>div>input {
        border-radius: 10px;
        padding: 10px;
        border: 1px solid #ccc;
    }
    .stButton>button {
        background-color: #007BFF;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #0056b3;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📊 Gryzzly Dashboard - Analyse des Projets")
st.markdown("---")

# Search bar with better UI
search_term = st.text_input("🔍 Rechercher un projet", "", help="Tapez le nom d'un projet pour filtrer")
filtered_projects = project_hours[project_hours["Project name"].str.contains(search_term, case=False, na=False)]

# Visualization: Hours per Project
st.subheader("⏳ Heures déclarées par projet")
fig = px.bar(filtered_projects.head(10), x="Duration", y="Project name", orientation='h', color="Duration",
             color_continuous_scale="Blues", title="🔝 Top 10 des projets avec le plus d'heures déclarées",
             template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Visualization: Hours per User
st.subheader("👤 Heures déclarées par utilisateur")
fig = px.bar(user_hours.head(10), x="Duration", y="Username", orientation='h', color="Duration",
             color_continuous_scale="Greens", title="👥 Top 10 des utilisateurs ayant déclaré le plus d'heures",
             template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

# Visualization: Costs per Project
st.subheader("💰 Coût déclaré par projet")
fig = px.bar(project_costs.head(10), x="Entry cost", y="Project name", orientation='h', color="Entry cost",
             color_continuous_scale="Reds", title="💸 Top 10 des projets les plus coûteux",
             template="plotly_white")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.markdown("📌 **Filtrage et fonctionnalités avancées à venir !**")
