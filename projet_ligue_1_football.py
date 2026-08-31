import pandas as pd
import streamlit as st
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt


# ============================================================
# CONFIG STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Ligue 1 - Analyse",
    layout="wide"
)


# ============================================================
# SCRAPING
# ============================================================

@st.cache_data(ttl=3600)
def load_data():

    url = "https://www.maxifoot.fr/resultat-ligue-1-france.htm"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    soup = BeautifulSoup(
        response.content,
        "html.parser"
    )

    table = soup.find(
        "table",
        class_="clas1"
    )

    rows = table.find_all("tr")

    data = []

    for row in rows[1:]:

        cols = [
            c.text.strip()
            for c in row.find_all("td")
        ]

        if len(cols) == 10:
            data.append(cols)

    columns = [
        "Rang",
        "Equipe",
        "Points",
        "Joués",
        "Match_gagnee",
        "Match_nul",
        "Match_perdu",
        "But_mis",
        "But_pris",
        "Difference_but"
    ]

    df = pd.DataFrame(
        data,
        columns=columns
    )

    int_cols = [
        "Rang",
        "Points",
        "Match_gagnee",
        "Match_nul",
        "Match_perdu",
        "But_mis",
        "But_pris",
        "Difference_but"
    ]

    for col in int_cols:
        df[col] = df[col].astype(int)

    df = df.set_index("Equipe")

    return df


# ============================================================
# RENDER
# ============================================================

def render():

    # --------------------------------------------------------
    # CHARGEMENT DES DONNÉES
    # --------------------------------------------------------

    df = load_data()

    df["Addition_but"] = (
        df["But_mis"] +
        df["But_pris"]
    )


    # ========================================================
    # TITRE
    # ========================================================

    st.markdown(
        """
        <h1 style='color:#6ADFF7;text-align:center;'>
            Projet Ligue 1 ⚽
        </h1>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # SOMMAIRE
    # ========================================================

    st.title("SOMMAIRE")

    st.subheader("1. Intro")
    st.subheader("2. Légende des colonnes")
    st.subheader("3. Classement général")
    st.subheader("4. Les buts marqués")
    st.subheader("5. Les buts encaissés")
    st.subheader("6. Les matchs nuls")
    st.subheader("7. Les matchs gagnés")
    st.subheader("8. Les matchs perdus")
    st.subheader("9. Vision globale des 5 valeurs")
    st.subheader("10. Faut-il marquer beaucoup pour gagner ?")
    st.subheader("11. Les buts font-ils le classement ?")
    st.subheader("12. Faut-il faire des matchs nuls ?")
    st.subheader("13. Qui est le plus équilibré ?")
    st.subheader("14. Qui fait le spectacle ?")
    st.subheader("15. Peut-on marquer beaucoup et faire beaucoup de nuls ?")
    st.subheader("16. Statistiques descriptives")


    # ========================================================
    # 1. INTRO
    # ========================================================

    st.subheader(
        "1. Intro",
        divider=True
    )

    st.write(
        "Bienvenue sur le projet **Ligue 1 savoir**, "
        "réalisé et publié par Steeve le Dimanche 11 Janvier 2026."
    )

    st.write(
        "Ce projet a pour but de présenter une analyse de données "
        "sur la Ligue 1."
    )

    st.write(
        "Nommée « Ligue 1 savoir », car l’objectif est le savoir "
        "et pas l’avoir."
    )


    # ========================================================
    # 2. LÉGENDE DES COLONNES
    # ========================================================

    st.subheader(
        "2. Légende des colonnes",
        divider=True
    )

    st.write("**Equipe** : nom de l’équipe")
    st.write("**Rang** : place dans le classement")
    st.write("**Points** : nombre de points")
    st.write("**Joués** : nombre de matchs joués")
    st.write("**Match_gagnee** : nombre de matchs gagnés")
    st.write("**Match_nul** : nombre de matchs nuls")
    st.write("**Match_perdu** : nombre de matchs perdus")
    st.write("**But_mis** : nombre de buts marqués")
    st.write("**But_pris** : nombre de buts encaissés")
    st.write(
        "**Difference_but** : buts marqués - buts encaissés"
    )
    st.write(
        "**Addition_but** : buts marqués + buts encaissés"
    )


    # ========================================================
    # 3. CLASSEMENT GÉNÉRAL
    # ========================================================

    st.subheader(
        "3. Classement général",
        divider=True
    )

    st.dataframe(
        df,
        use_container_width=True
    )


    # ========================================================
    # 4. BUTS MARQUÉS
    # ========================================================

    st.subheader(
        "4. Les buts marqués",
        divider=True
    )

    st.write(
        "Ce visuel montre la répartition des buts marqués."
    )

    df3 = (
        df.sort_values(
            "But_mis",
            ascending=True
        )
        .reset_index()
    )

    chart = alt.Chart(df3).mark_bar(
        color="#1de52a"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=None,
            title="Équipe"
        ),

        y=alt.Y(
            "But_mis:Q",
            title="Buts marqués"
        ),

        tooltip=[
            "Equipe:N",
            "But_mis:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 5. BUTS ENCAISSÉS
    # ========================================================

    st.subheader(
        "5. Les buts encaissés",
        divider=True
    )

    df3 = (
        df.sort_values(
            "But_pris",
            ascending=True
        )
        .reset_index()
    )

    chart = alt.Chart(df3).mark_bar(
        color="#c8e413"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=None,
            title="Équipe"
        ),

        y=alt.Y(
            "But_pris:Q",
            title="Buts encaissés"
        ),

        tooltip=[
            "Equipe:N",
            "But_pris:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 6. MATCHS NULS
    # ========================================================

    st.subheader(
        "6. Les matchs nuls",
        divider=True
    )

    df3 = (
        df.sort_values(
            "Match_nul",
            ascending=True
        )
        .reset_index()
    )

    chart = alt.Chart(df3).mark_bar(
        color="#1d3622"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=None,
            title="Équipe"
        ),

        y=alt.Y(
            "Match_nul:Q",
            title="Matchs nuls"
        ),

        tooltip=[
            "Equipe:N",
            "Match_nul:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 7. MATCHS GAGNÉS
    # ========================================================

    st.subheader(
        "7. Les matchs gagnés",
        divider=True
    )

    df3 = (
        df.sort_values(
            "Match_gagnee",
            ascending=True
        )
        .reset_index()
    )

    chart = alt.Chart(df3).mark_bar(
        color="#F415D6"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=None,
            title="Équipe"
        ),

        y=alt.Y(
            "Match_gagnee:Q",
            title="Matchs gagnés"
        ),

        tooltip=[
            "Equipe:N",
            "Match_gagnee:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 8. MATCHS PERDUS
    # ========================================================

    st.subheader(
        "8. Les matchs perdus",
        divider=True
    )

    df3 = (
        df.sort_values(
            "Match_perdu",
            ascending=True
        )
        .reset_index()
    )

    chart = alt.Chart(df3).mark_bar(
        color="#6B49CE"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=None,
            title="Équipe"
        ),

        y=alt.Y(
            "Match_perdu:Q",
            title="Matchs perdus"
        ),

        tooltip=[
            "Equipe:N",
            "Match_perdu:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 9. NORMALISATION
    # ========================================================

    st.subheader(
        "9. Vision globale des 5 valeurs",
        divider=True
    )

    colonnes = [
        "But_pris",
        "But_mis",
        "Match_gagnee",
        "Match_nul",
        "Match_perdu"
    ]

    for col in colonnes:

        df[col + "_nor"] = (
            (df[col] - df[col].min())
            /
            (df[col].max() - df[col].min())
        )

    st.area_chart(
        df,
        y=[
            "But_mis_nor",
            "But_pris_nor",
            "Match_gagnee_nor",
            "Match_nul_nor",
            "Match_perdu_nor"
        ],
        color=[
            "#FF0000",
            "#0000FF",
            "#00AA00",
            "#FFA500",
            "#800080"
        ],
        stack=True
    )

    st.write(
        "**Légende :** Rouge = buts mis, "
        "bleu = buts pris, vert = matchs gagnés, "
        "orange = matchs nuls, violet = matchs perdus."
    )


    # ========================================================
    # 10. RAPPORT BUTS / POINTS
    # ========================================================

    st.subheader(
        "10. Faut-il marquer beaucoup pour gagner ?",
        divider=True
    )

    df["Rapport_but_point"] = (
        df["But_mis"] /
        df["Points"]
    )

    kiki2 = (
        df[
            [
                "Rapport_but_point",
                "But_mis",
                "Points"
            ]
        ]
        .sort_values(
            "Rapport_but_point",
            ascending=True
        )
    )

    styled_df = kiki2.style.background_gradient(
        subset=["Rapport_but_point"],
        cmap="Blues"
    )

    st.dataframe(
        styled_df,
        use_container_width=True
    )


    # ========================================================
    # GRAPHIQUE POINTS / BUTS
    # ========================================================

    df4 = (
        df.sort_values(
            "Points",
            ascending=True
        )
        .reset_index()
    )

    ordre = df4["Equipe"].tolist()

    chart = alt.Chart(df4).transform_fold(
        [
            "Points",
            "But_mis"
        ],
        as_=[
            "Statistique",
            "Valeur"
        ]
    ).mark_bar().encode(

        x=alt.X(
            "Equipe:N",
            sort=ordre,
            title="Équipe"
        ),

        y=alt.Y(
            "Valeur:Q",
            title="Valeur"
        ),

        color=alt.Color(
            "Statistique:N",
            title="Statistique"
        ),

        tooltip=[
            "Equipe:N",
            "Statistique:N",
            "Valeur:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 11. POINTS / DIFFÉRENCE DE BUTS
    # ========================================================

    st.subheader(
        "11. Les buts font-ils le classement ?",
        divider=True
    )

    df4 = (
        df.sort_values(
            "Points",
            ascending=True
        )
        .reset_index()
    )

    ordre = df4["Equipe"].tolist()

    chart = alt.Chart(df4).transform_fold(
        [
            "Points",
            "Difference_but"
        ],
        as_=[
            "Statistique",
            "Valeur"
        ]
    ).mark_bar().encode(

        x=alt.X(
            "Equipe:N",
            sort=ordre
        ),

        y=alt.Y(
            "Valeur:Q"
        ),

        color=alt.Color(
            "Statistique:N"
        ),

        tooltip=[
            "Equipe:N",
            "Statistique:N",
            "Valeur:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 12. MATCHS NULS / POINTS
    # ========================================================

    st.subheader(
        "12. Faut-il faire des matchs nuls pour gagner ?",
        divider=True
    )

    df4 = (
        df[
            [
                "Points",
                "Match_nul"
            ]
        ]
        .sort_values(
            "Points",
            ascending=True
        )
    )

    st.bar_chart(
        df4,
        use_container_width=True,
        stack=False
    )


    # ========================================================
    # 13. ÉQUILIBRE BUTS MIS / BUTS PRIS
    # ========================================================

    st.subheader(
        "13. Qui est le plus équilibré ?",
        divider=True
    )

    df_reset = df.reset_index()

    points = alt.Chart(df_reset).mark_circle(
        size=100
    ).encode(

        x=alt.X(
            "But_mis:Q",
            title="Buts marqués"
        ),

        y=alt.Y(
            "But_pris:Q",
            title="Buts encaissés"
        ),

        color=alt.Color(
            "Equipe:N",
            legend=None
        ),

        tooltip=[
            "Equipe",
            "But_mis",
            "But_pris"
        ]
    )

    st.altair_chart(
        points.properties(
            width=750,
            height=750
        ),
        use_container_width=False
    )


    # ========================================================
    # 14. QUI FAIT LE SPECTACLE ?
    # ========================================================

    st.subheader(
        "14. Qui fait le spectacle ?",
        divider=True
    )

    df3 = (
        df.sort_values(
            "Addition_but",
            ascending=True
        )
        .reset_index()
    )

    ordre = df3["Equipe"].tolist()

    chart = alt.Chart(df3).mark_bar(
        color="#3cdaa5"
    ).encode(

        x=alt.X(
            "Equipe:N",
            sort=ordre,
            title="Équipe"
        ),

        y=alt.Y(
            "Addition_but:Q",
            title="Buts marqués + encaissés"
        ),

        tooltip=[
            "Equipe:N",
            "Addition_but:Q"
        ]
    )

    st.altair_chart(
        chart,
        use_container_width=True
    )


    # ========================================================
    # 15. ADDITION BUTS / MATCHS NULS
    # ========================================================

    st.subheader(
        "15. Peut-on marquer beaucoup de buts et faire beaucoup de matchs nuls ?",
        divider=True
    )

    df_alt = df.reset_index()

    chart = alt.Chart(df_alt).mark_circle(
        size=160
    ).encode(

        x=alt.X(
            "Addition_but:Q",
            title="Addition buts"
        ),

        y=alt.Y(
            "Match_nul:Q",
            title="Matchs nuls"
        ),

        color=alt.Color(
            "Equipe:N",
            legend=alt.Legend(
                title="Équipe"
            )
        ),

        tooltip=[
            "Equipe:N",
            "Addition_but:Q",
            "Match_nul:Q"
        ]
    ).properties(
        title="Addition buts vs matchs nuls",
        width=750,
        height=750
    )

    st.altair_chart(
        chart,
        use_container_width=False
    )


    # ========================================================
    # 16. BOXPLOTS + CAMEMBERT
    # ========================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.title("Buts mis")

        fig, ax = plt.subplots(
            figsize=(8, 6)
        )

        sns.boxplot(
            y=df["But_mis"],
            width=0.4,
            linewidth=0.5,
            whis=1.2,
            flierprops={
                "markersize": 5
            },
            ax=ax
        )

        ax.tick_params(
            axis="both",
            labelsize=15
        )

        ax.set_ylabel(
            "Buts",
            fontsize=18
        )

        ax.set_title(
            "Les buts marqués",
            fontsize=20
        )

        st.pyplot(fig)


    with col2:

        st.title("Buts pris")

        fig, ax = plt.subplots(
            figsize=(8, 6)
        )

        sns.boxplot(
            y=df["But_pris"],
            width=0.4,
            linewidth=0.5,
            whis=1.2,
            flierprops={
                "markersize": 5
            },
            ax=ax
        )

        ax.tick_params(
            axis="both",
            labelsize=15
        )

        ax.set_ylabel(
            "Buts",
            fontsize=18
        )

        ax.set_title(
            "Les buts encaissés",
            fontsize=20
        )

        st.pyplot(fig)


    with col3:

        st.title("Matchs nuls")

        fig, ax = plt.subplots(
            figsize=(8, 6)
        )

        ax.pie(
            df["Match_nul"],
            labels=df.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.axis("equal")

        st.pyplot(
            fig,
            use_container_width=False
        )


    # ========================================================
    # STATISTIQUES DESCRIPTIVES
    # ========================================================

    st.subheader(
        "Statistiques descriptives",
        divider=True
    )

    st.dataframe(
        df.describe(),
        use_container_width=True
    )


    # ========================================================
    # GRAPHIQUE VEGA LITE INTERACTIF
    # ========================================================

    st.subheader(
        "Analyse interactive",
        divider=True
    )

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


# ============================================================
# LANCEMENT DE L'APPLICATION
# ============================================================

render()