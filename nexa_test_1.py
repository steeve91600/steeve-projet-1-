import streamlit as st 

st.set_page_config(page_title="Steeve  Application",
     layout="wide")


st.title(":orange[Baby] :blue[time] :blue[application] :clock230:",help=" Merci d'être là mon ami !", text_alignment="center")



import datetime
import streamlit as st

import datetime
import streamlit as st
import pandas as pd
import os

import pytz
file_path = "avrivril.xlsx"

# --- Inputs ---

paris = pytz.timezone("Europe/Paris")
event_time = st.datetime_input(
    "Heure et date automatique",
    datetime.datetime.now(paris)
)

genre = st.radio(
    "Fais ton choix ",
    ["SG", "SD"],
    index=None,
)

# --- Bouton Enregistrer ---
if st.button("Enregistrer"):
    
    if genre is not None:

        new_data = pd.DataFrame([{
            "Date": event_time,
            "Genre": genre
        }])
        
        if os.path.exists(file_path):
            existing_data = pd.read_excel(file_path)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data
        
        updated_data.to_excel(file_path, index=False)
        
        st.success("Données enregistrées ✅")
        st.rerun()

    else:
        st.warning("Choisis un genre avant d'enregistrer ⚠️")

# --- Affichage du tableau ---



st.subheader("📊 Données enregistrées")

if os.path.exists(file_path):
    df = pd.read_excel(file_path)

    # conversion obligatoire en datetime
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # 🔥 différence entre lignes
    df["difference"] = df["Date"].diff()
    df=df.sort_index(ascending=False)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Aucune donnée pour le moment")

mean_diff = df["difference"].mean()

# conversion en minutes
mean_minutes = mean_diff.total_seconds() / 60

st.subheader(f":red[Il y a une TT en moyenne  toutes les {round(mean_minutes, 2)} minutes]")