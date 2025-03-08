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

# Streamlit UI - Modern Dark Mode
st.set_page_config(page_title="Gryzzly Dashboard", page_icon="📊", layout="wide")

# Custom CSS for Dark Mode
st.markdown("""
    <style>
    body {
        font-family: 'Inter', sans-serif;
        background-color: #1e1e2f;
        color: #e0e0e0;
    }
    .block-container {
        max-width: 1400px;
        padding: 2rem;
        background: #2a2a40;
        border-radius: 15px;
        box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.5);
    }
    .stTextInput>div>div>input {
        background-color: #33334d;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        border: 1px solid #444466;
    }
    .stButton>button {
        background-color: #4F46E5;
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #4338CA;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.title("📊 Gryzzly Dashboard")
st.sidebar.markdown("---")

tabs = st.sidebar.radio("Navigation", ["🏠 Accueil", "📈 Performance", "📊 Analytique", "⚙️ Paramètres"])

if tabs == "🏠 Accueil":
    st.title("📊 Vue d'ensemble des projets")
    st.markdown("---")
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("📅 Projets en cours", len(df_projects))
    col2.metric("👤 Collaborateurs actifs", len(df_declarations['Username'].unique()))
    col3.metric("💰 Coût total", f"{project_costs['Entry cost'].sum():,.0f} €")
    col4.metric("⏳ Heures totales", f"{project_hours['Duration'].sum():,.0f} h")
    
    st.markdown("---")
    st.subheader("🔍 Rechercher un projet")
    search_term = st.text_input("", "", help="Tapez le nom d'un projet pour filtrer")
    filtered_projects = project_hours[project_hours["Project name"].str.contains(search_term, case=False, na=False)]
    
    # Visualization: Hours per Project
    st.subheader("⏳ Heures déclarées par projet")
    fig = px.bar(filtered_projects.head(10), x="Duration", y="Project name", orientation='h', color="Duration",
                 color_continuous_scale="darkmint", title="🔝 Top 10 des projets avec le plus d'heures déclarées",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualization: Hours per User
    st.subheader("👤 Heures déclarées par utilisateur")
    fig = px.bar(user_hours.head(10), x="Duration", y="Username", orientation='h', color="Duration",
                 color_continuous_scale="teal_r", title="👥 Top 10 des utilisateurs ayant déclaré le plus d'heures",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # Visualization: Costs per Project
    st.subheader("💰 Coût déclaré par projet")
    fig = px.bar(project_costs.head(10), x="Entry cost", y="Project name", orientation='h', color="Entry cost",
                 color_continuous_scale="reds", title="💸 Top 10 des projets les plus coûteux",
                 template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    st.markdown("📌 **Filtrage et fonctionnalités avancées à venir !**")
