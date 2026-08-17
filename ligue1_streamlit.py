import streamlit as st
from pathlib import Path
import importlib.util

st.set_page_config(
    page_title="Portfolio Data Analyst",
    page_icon="📊",
    layout="wide",
)

PROJECTS = {
    "Projet Box Office US": {
        "file": "projet_box_office_us.py",
        "description": "Analyse des performances du box-office américain à partir de données cinématographiques.",
        "icon": "🎬",
    },
    "Projet Ligue 1 Football": {
        "file": "projet_ligue_1_football.py",
        "description": "Analyse de données de la Ligue 1 : clubs, résultats, classements et indicateurs de performance.",
        "icon": "⚽",
    },
}

def load_project(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    if spec is None or spec.loader is None:
        raise ImportError(f"Impossible de charger {path.name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

st.title("📊 Mon Portfolio Data")
st.markdown(
    "Bienvenue sur mon portfolio interactif. "
    "Sélectionnez un projet dans la barre latérale pour consulter son analyse."
)

# --- Barre latérale ---
with st.sidebar:
    st.header("Mes projets")
    selected = st.radio(
        "Choisir un projet",
        ["Accueil"] + list(PROJECTS.keys()),
    )

# --- Synchronisation avec session_state ---
if "selected_project" in st.session_state:
    selected = st.session_state["selected_project"]

# --- Page Accueil ---
if selected == "Accueil":
    st.subheader("Mes projets")
    cols = st.columns(2)

    for col, (name, project) in zip(cols, PROJECTS.items()):
        with col:
            st.markdown(f"## {project['icon']} {name}")
            st.write(project["description"])
            if st.button(f"Ouvrir — {name}", key=f"open_{name}"):
                st.session_state["selected_project"] = name
                st.rerun()

    st.info("Les deux projets sont séparés dans leurs propres fichiers Python et sont chargés depuis cette application Streamlit.")

# --- Page Projet ---
else:
    project = PROJECTS[selected]
    st.header(f"{project['icon']} {selected}")
    st.caption(project["description"])

    project_path = Path(__file__).parent / project["file"]

    if project_path.exists():
        try:
            module = load_project(project_path)
            if hasattr(module, "render"):
                module.render()
            else:
                st.warning(
                    f"Le fichier `{project['file']}` doit contenir une fonction `render()` "
                    "pour afficher le projet dans le portfolio."
                )
        except Exception as e:
            st.error(f"Erreur lors du chargement du projet : {e}")
    else:
        st.error(f"Fichier introuvable : {project_path.name}")

