import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# CONFIG STREAMLIT
# -----------------------------
def render():

    st.title("Mon projet")

    
st.set_page_config(
    page_title="Ligue 1 - Analyse",
    layout="wide"
)


st.markdown(
    "<h1 style='color:#6ADFF7;text-align:center;'> Projet ligue 1 live ⚽</h1>",
    unsafe_allow_html=True
)

st.title("SOMMAIRE")
st.subheader("1. Intro ")
st.subheader("2. Legende des colonnes")
st.subheader("3. Classement général")
st.subheader("4 .Les buts  marqués")
st.subheader("5 .Les buts encaissés")
st.subheader("6. Les matchs nuls")
st.subheader("7. Les matchs gagnés")
st.subheader("8. Les matchs perdus")
st.subheader("9 .Vision globale des 5 valeurs")
st.subheader("10. Faut-il marquer beaucoup pour gagner le championnat ?")
st.subheader("11. Les buts font-ils le classement ?")
st.subheader("12. Faut-il faire des matchs nul pour gagner ? ")
st.subheader("13. Qui est le plus équilibré ?")
st.subheader("14. Qui est le plus équilibré B ?")
st.subheader("15 .Qui fait le spectacle ?")
st.subheader("16 .Peut-on marquer beaucoup de but et faire beaucoup de match nul ? ")
st.subheader("17. Graphique 3D représentant le nombre de but pris , le nombre de but mis et le nombre de points de chaque équipe .")

st.subheader("1. Intro", divider=True)
st.write("Bienvenue sur le projet **Ligue 1 live**, mis à jour par  Steeve Orville le Dimanche 22 novembre 2026. Ce projet a pour but de présenter l’analyse de donnée .  ")
st.write("Ici nous allons analyser le tableau de la Ligue 1 ( championnat de France de football professionnel) . Les données de ce tableau sont actualisées automatiquement chaque semaine grâce à la technologie du scraping de données . Les graphiques bouge donc automatiquement chaque semaine . ")
st.write(" Remarque : c'est une analyse de données simple donc il n'y a pas de machine learning à la fin . ")
st.subheader("2. Légende des colonnes", divider=True)
st.write("Voici la légende des colonnes du « Classement Général » : ")
st.write("**Equipe** : le nom de l’équipe en question")
st.write("**Rang** : Place dans le classement ")
st.write("**Points** : Nombre de point ( relatif à la place du classement )")
st.write("**Joués** : Numéro de la journée ")
st.write("**Match_gagnee** : Nombre de match gagné par l’équipe")
st.write("**Match_nul** : Nombre de match nul réalisé par l’équipe ")
st.write("**Match_perdu** : Nombre de match perdu par l’équipe")
st.write("**But_mis** : Nombre de but marqué par l’équipe")
st.write("**But_pris** : Nombre de but pris par l’équipe ")
st.write("**Difference_but** : Soustraction entre le nombre de but marqué et le nombre de but pris .")
st.write("**Addition_but** : Addition entre les buts marqués et les buts encaissés .")

# -----------------------------
# SCRAPING (AVEC CACHE)
# -----------------------------
@st.cache_data(ttl=3600)
def load_data():
    url = "https://www.maxifoot.fr/resultat-ligue-1-france.htm"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")

    table = soup.find("table", class_="clas1")
    rows = table.find_all("tr")

    data = []
    for row in rows[1:]:
        cols = [c.text.strip() for c in row.find_all("td")]
        if len(cols) == 10:
            data.append(cols)

    columns = [
        "Rang", "Equipe", "Points", "Joués",
        "Match_gagnee", "Match_nul", "Match_perdu",
        "But_mis", "But_pris", "Difference_but"
    ]

    df = pd.DataFrame(data, columns=columns)

    # Conversion types
    int_cols = [
        "Rang", "Points", "Match_gagnee",
        "Match_nul", "Match_perdu",
        "But_mis", "But_pris", "Difference_but"
    ]

    for col in int_cols:
        df[col] = df[col].astype(int)

    df = df.set_index("Equipe")

    return df


df = load_data()

df['Addition_but']=df["But_mis"]+df["But_pris"]

# -----------------------------
# AFFICHAGE
# -----------------------------
st.subheader("3. Classement général", divider=True)
st.dataframe(df, use_container_width=True)









df.sort_values(["But_mis"] , ascending=True)






st.subheader("4 .Les buts  marqués ", divider=True)

st.write("Légende: Ce visuel montre la répartition des buts marqués")



import altair as alt
import streamlit as st


import matplotlib.pyplot as plt
import streamlit as st




df3 = df.sort_values("But_mis", ascending=True).reset_index()

import altair as alt



chart = alt.Chart(df3).mark_bar(color="#1de52a").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("But_mis:Q")
)

st.altair_chart(chart, use_container_width=True)


st.subheader("5 .Les buts  encaissés ", divider=True)

st.write("Légende: Ce visuel montre la répartition des buts encaissé")






df3 = df.sort_values("But_pris", ascending=True).reset_index()





chart = alt.Chart(df3).mark_bar(color="#c8e413").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("But_pris:Q")
)

st.altair_chart(chart, use_container_width=True)


st.subheader("6 .Les matchs nuls ", divider=True)

st.write("Légende: Ce visuel montre la répartition des matchs nuls")






df3 = df.sort_values("Match_nul", ascending=True).reset_index()





chart = alt.Chart(df3).mark_bar(color="#1d3622").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("Match_nul:Q")
)

st.altair_chart(chart, use_container_width=True)


st.subheader("7 .Les matchs gagnées ", divider=True)

st.write("Légende: Ce visuel montre la répartition des matchs gagnées par équipe")






df3 = df.sort_values("Match_gagnee", ascending=True).reset_index()





chart = alt.Chart(df3).mark_bar(color="#F415D6").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("Match_gagnee:Q")
)

st.altair_chart(chart, use_container_width=True)




st.subheader("8 .Les matchs perdus ", divider=True)

st.write("Légende: Ce visuel montre la répartition des matchs perdu par équipe")






df3 = df.sort_values("Match_perdu", ascending=True).reset_index()





chart = alt.Chart(df3).mark_bar(color="#6B49CE").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("Match_perdu:Q")
)




st.altair_chart(chart, use_container_width=True)


st.subheader("9 .Vision global des 5 valeurs (avec Normalisation)", divider=True)



df["But_pris_nor"] = (
    (df["But_pris"] - df["But_pris"].min())
    / (df["But_pris"].max() - df["But_pris"].min())
)
df["But_mis_nor"] = (
    (df["But_mis"] - df["But_mis"].min())
    / (df["But_mis"].max() - df["But_mis"].min())
)

df["Match_gagnee_nor"] = (
    (df["Match_gagnee"] - df["Match_gagnee"].min())
    / (df["Match_gagnee"].max() - df["Match_gagnee"].min())
)
df["Match_nul_nor"] = (
    (df["Match_nul"] - df["Match_nul"].min())
    / (df["Match_nul"].max() - df["Match_nul"].min())
)

df["Match_perdu_nor"] = (
    (df["Match_perdu"] - df["Match_perdu"].min())
    / (df["Match_perdu"].max() - df["Match_perdu"].min())
)


import streamlit as st

df_plot = df[
    ["But_mis_nor", "But_pris_nor", "Match_gagnee_nor",
     "Match_nul_nor", "Match_perdu_nor"]
].rename(columns={
    "But_mis_nor": "Buts marqués",
    "But_pris_nor": "Buts encaissés",
    "Match_gagnee_nor": "Matchs gagnés",
    "Match_nul_nor": "Matchs nuls",
    "Match_perdu_nor": "Matchs perdus"
})

st.area_chart(
    df_plot,
    color=["#FF0000", "#0000FF", "#00AA00", "#FFA500", "#800080"],
    stack=True
)

st.write("***Legende :*** Rouge pour les buts mis , bleu pour les but pris , vert pour les match gagné , orange pour les matchs nul et violet pour les match perdu ")
st.subheader("10. Faut-il marquer beaucoup pour gagner le championnat ? ( Comparaison Buts mis/ Points final )", divider=True)


st.write("Légende : Ce premier tableau montre une simple division entre le nombre de point et le nombre de but .Voici donc comme resulta un Rapport point/but .Pour bien expliquer , l'équipe en haut du tableau est une equipe qui marque beaucou^p de but mais a beaucuop de points au classement")


df['Rapport_but_point']=df['But_mis']/df['Points']
kiki=df[['Rapport_but_point','But_mis','Points']]
kiki2=kiki.sort_values('Rapport_but_point',ascending=True)
styled_df = kiki2.style.background_gradient(subset=['Rapport_but_point'], cmap="Blues")

st.dataframe(styled_df, use_container_width=True)

st.write("Légende : Ce visuel compare le nombre de buts mis ( vert ) et le nombre de point ( rose).")






df4 = df.sort_values("Points", ascending=True).reset_index()

df4["Equipe"] = pd.Categorical(
    df4["Equipe"],
    categories=df4["Equipe"].tolist(),
    ordered=True
)

st.bar_chart(
    df4,
    x="Equipe",
    y=["Points", "But_mis"],
    color=["#BEEF4C","#EF6DBD"],
    stack=False
)











import altair as alt

df_reset = df.reset_index()

st.write("Légende : Voici un nuage de point et un droite de regression linéaire. ")
st.write("Explication : Plus un point est aloigné de la droite, moins son comportement est normal.")
df_scatter = df.reset_index()

chart = alt.Chart(df_scatter).mark_circle(
    size=100
).encode(
    x=alt.X(
        "Points:Q",
        title="Points"
    ),
    y=alt.Y(
        "But_mis:Q",
        title="Buts marqués"
    ),
    color=alt.Color(
        "Equipe:N",
        title="Équipe"
    ),
    tooltip=[
        "Equipe:N",
        "Points:Q",
        "But_mis:Q"
    ]
)

st.altair_chart(
    chart,
    use_container_width=True
)











st.subheader("11. Les buts font-ils le classement ? (Comparaison Nombre de points / Différence de buts", divider=True)
st.write("Légende : Ce visuel compare la différence de but ( bleu foncé ) et le nombre de point ( bleu clair).")


df4 = df.sort_values("Points", ascending=True).reset_index()

df4["Equipe"] = pd.Categorical(
    df4["Equipe"],
    categories=df4["Equipe"].tolist(),
    ordered=True
)

st.bar_chart(
    df4,
    x="Equipe",
    y=["Points", "Difference_but"],
    use_container_width=True
)
st.subheader("12. Faut-il faire des matchs nul pour gagner ?  ", divider=True)
st.write('Légende : Ce visuel compare le nombre de match nul et le nombre de point . ')

st.bar_chart(
    df[["Points", "Match_nul"]],
    color=["#EA61CA","#80AFF1"],
    stack=False
)




st.subheader("13. Qui est le plus équilibré ? ( Comparaison Buts mis/ But pris )", divider=True)
st.write('Légende : Ce rapport compare les Buts mis et les Buts pris .')
st.bar_chart(
    df[["But_mis", "But_pris"]],
    color=["#BFF640","#E9B771"],
    use_container_width=True
)



st.subheader("14. Qui est le plus équilibré B ? ( Comparaison Buts mis/ But pris )", divider=True)
df_reset = df.reset_index()

st.write("Légende : Voici un nuage de point et un droite de regression linéaire. ")
st.write("Explication : Plus un point est aloigné de la droite, moins il est equilibré")
points = alt.Chart(df_reset).mark_circle(size=80).encode(
    x=alt.X("But_mis:Q", title="Buts marqués"),
    y=alt.Y("But_pris:Q", title="Buts encaissé"),
    color=alt.Color("Equipe:N", legend=None),
    tooltip=["Equipe", "But_mis", "But_pris"]
)

regression = points.transform_regression(
    "But_mis",
    "Points"
).mark_line(color="red", size=3)

chart = (points + regression).properties(
    width=800,
    height=800
)




col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.altair_chart(chart, use_container_width=False)



st.subheader("15 .Qui fait le spectacle ? ( But marqué + But encaissé )", divider=True)

st.write("Légende: Ce visuel montre une addition entre le nombre de but marqué et le nombre de but encaissé")



import altair as alt
import streamlit as st


import matplotlib.pyplot as plt
import streamlit as st

df["addition"] = df["But_mis"] + df["But_pris"]


df3 = df.sort_values("addition", ascending=True).reset_index()

import altair as alt

df_sorted = df.sort_values("Match_nul", ascending=True).reset_index()

chart = alt.Chart(df3).mark_bar(color="#3cdaa5").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("addition:Q")
)

st.altair_chart(chart, use_container_width=True)







st.subheader("16. Peut-on marquer beaucoup de but et faire beaucoup de match nul ? ", divider=True)


import altair as alt
import streamlit as st

df_alt = df.reset_index()  # index = Equipe

chart = alt.Chart(df_alt).mark_circle(size=80).encode(
    x=alt.X('Addition_but:Q', title='Addition but'),
    y=alt.Y('Match_nul:Q', title='Match nul'),
    color=alt.Color('Equipe:N', legend=alt.Legend(title="Équipe")),
    tooltip=['Equipe:N', 'Addition_but:Q', 'Match_nul:Q']
).properties(
    title="Nuage de points : Addition but vs Match nul"
)

st.altair_chart(chart, use_container_width=True)


"----------------------------------"


st.subheader("17. Graphique 3D représentant le nombre de but pris , le nombre de but mis et le nombre de points de chaque équipe .  ", divider=True)




import pandas as pd
import streamlit as st

df_alt = df.reset_index()

spec = {
    "mark": {
        "type": "circle",
        "size": 160,
        "tooltip": True
    },

    "params": [
        {
            "name": "interval_selection",
            "select": "interval"
        },
        {
            "name": "point_selection",
            "select": "point"
        }
    ],

    "encoding": {
        "x": {
            "field": "But_pris",
            "type": "quantitative",
            "title": "Buts pris"
        },

        "y": {
            "field": "But_mis",
            "type": "quantitative",
            "title": "Buts mis"
        },

        "size": {
            "field": "Points",
            "type": "quantitative",
            "title": "Points"
        },

        "color": {
            "field": "Points",
            "type": "quantitative",
            "title": "Points",
            "scale": {
                "scheme": "viridis"
            }
        },

        "fillOpacity": {
            "condition": {
                "param": "point_selection",
                "value": 1
            },
            "value": 0.3
        },

        "tooltip": [
            {
                "field": "Equipe",
                "type": "nominal",
                "title": "Équipe"
            },
            {
                "field": "But_pris",
                "type": "quantitative",
                "title": "Buts pris"
            },
            {
                "field": "But_mis",
                "type": "quantitative",
                "title": "Buts mis"
            },
            {
                "field": "Points",
                "type": "quantitative",
                "title": "Points"
            }
        ]
    },

    "width": 750,
    "height": 750
}

event = st.vega_lite_chart(
    df_alt,
    spec,
    key="vega_chart",
    on_select="rerun"
)

st.write(event)
