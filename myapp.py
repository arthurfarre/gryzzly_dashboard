import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuration du mot de passe
PASSWORD = "Sight2025!"  # Remplacez par votre mot de passe sécurisé

# Fonction d'authentification
def check_password():
    """Affiche un formulaire de connexion et vérifie le mot de passe."""
    if "auth" not in st.session_state:
        st.session_state.auth = False

    if not st.session_state.auth:
        password = st.text_input("Entrez le mot de passe :", type="password")
        if password == PASSWORD:
            st.session_state.auth = True
            st.rerun()
        else:
            st.warning("Mot de passe incorrect.")
            st.stop()

# Vérification de l'authentification
check_password()





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

# Streamlit UI
st.title("Gryzzly Dashboard 📊")
st.sidebar.header("Filtres")

# Visualization: Hours per Project
st.subheader("Heures déclarées par projet")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=project_hours.head(10), x="Duration", y="Project name", ax=ax)
ax.set_xlabel("Total Hours")
st.pyplot(fig)

# Visualization: Hours per User
st.subheader("Heures déclarées par utilisateur")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=user_hours.head(10), x="Duration", y="Username", ax=ax)
ax.set_xlabel("Total Hours")
st.pyplot(fig)

# Visualization: Costs per Project
st.subheader("Coût déclaré par projet")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(data=project_costs.head(10), x="Entry cost", y="Project name", ax=ax)
ax.set_xlabel("Total Cost (€)")
st.pyplot(fig)

st.write("📌 **Filtrage et fonctionnalités avancées à venir !**")
