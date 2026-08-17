import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt

def render():

    # -----------------------------
    # CONFIG STREAMLIT
    # -----------------------------
    st.set_page_config(
        page_title="Ligue 1 - Analyse",
        layout="wide"
    )

    st.markdown(
        "<h1 style='color:#6ADFF7;text-align:center;'> Ce dashboard est en pause tant que le championnat de foot de ligue 1 est en pause ( merci de votre compréhension)  ⚽</h1>",
        unsafe_allow_html=True
    )

    st.title("SOMMAIRE")
    st.subheader("1. Intro ")
    st.subheader("2. Legende des colonnes")
    st.subheader("3. Classement général")
    st.subheader("4. Faut-il marquer beaucoup pour gagner le championnat ?")
    st.subheader("5. Quelle équipe est la plus ennuyante A ?")
    st.subheader("6. Les buts font-ils le classement ?")
    st.subheader("7. Faut-il faire des matchs nuls pour gagner ?")
    st.subheader("8. Qui est le plus équilibré ?")
    st.subheader("9. Qui est le plus équilibré B ?")
    st.subheader("10. Qui fait le spectacle ?")
    st.subheader("11. Peut-on marquer beaucoup de but et faire beaucoup de match nul ?")
    st.subheader("11. BILAN DE L'ANALYSE")

    st.subheader("1. Intro", divider=True)
    st.write("Bienvenue sur le projet **Ligue 1 savoir**, réalisé et publié par  Steeve  le Dimanche 11 Janvier 2026. Ce projet a pour but de présenter l’analyse de donnée .  ")
    st.write("Nommée « Ligue 1 savoir » , car l’objectif c’est le savoir et pas l’avoir . Nous allons donc essayer de comprendre en profondeur, c’est quoi la ligue 1 . Pour ceux qui ne savent rien , vraiment rien … la « Ligue 1 » , c’est le plus haut niveau du championnat de France de football . ")
    st.write(" Le premier chapitre de cette analyse portera sur le tableau  « Classement Général » . Ce tableau , résume ce qui se passe d’une manière général dans la Ligue 1 . Ce tableau est en streaming live, donc actualisé en temps réel . Les graphiques sont aussi en temps réel , seul les légendes de graphique et les titres sont manuels ( actualisé une fois par mois ). ")

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
        headers = {"User-Agent": "Mozilla/5.0"}
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
    df['Addition_but'] = df["But_mis"] + df["But_pris"]

    # -----------------------------
    # AFFICHAGE
    # -----------------------------
    st.subheader("3. Classement général", divider=True)
    st.dataframe(df, use_container_width=True)

    df.sort_values(["But_mis"], ascending=True)

    st.subheader("4. Faut-il marquer beaucoup pour gagner le championnat ? ( Comparaison Buts mis/ Points final )", divider=True)
    st.write("Légende : Ce premier tableau montre une simple division entre le nombre de point et le nombre de but .Voici donc comme resulta un Rapport point/but .Pour bien expliquer , l'équipe en haut du tableau est une equipe qui marque beaucou^p de but mais a beaucuop de points au classement")

    df['Rapport_but_point'] = df['But_mis'] / df['Points']
    kiki = df[['Rapport_but_point', 'But_mis', 'Points']]
    kiki2 = kiki.sort_values('Rapport_but_point', ascending=True)
    styled_df = kiki2.style.background_gradient(subset=['Rapport_but_point'], cmap="Blues")

    st.dataframe(styled_df, use_container_width=True)

    st.write("Légende : Ce visuel compare le nombre de buts mis et le nombre de point. Et la réponse est que Lens domine ce championnat mais marque peu. Ce qui est triste car Marseille et Paris FC marque beaucoup sans penser à gagner le match !")

    st.bar_chart(
        df[["But_mis", "Points"]],
        color=["#BEEF4C", "#EF6DBD"],
        stack=False
    )

    df_reset = df.reset_index()

    st.write("Légende : Voici un nuage de point et un droite de regression linéaire. ")
    st.write("Explication : Plus un point est aloigné de la droite, moins son comportement est normal. Ainsi , Lens, ,Le Havre , Lyon et Metz contredise la théorie qu'il faut marquer pour gagner")

    points = alt.Chart(df_reset).mark_circle(size=80).encode(
        x=alt.X("But_mis:Q", title="Buts marqués"),
        y=alt.Y("Points:Q", title="Points"),
        color=alt.Color("Equipe:N", legend=None),
        tooltip=["Equipe", "But_mis", "Points"]
    )

    regression = points.transform_regression(
        "But_mis",
        "Points"
    ).mark_line(color="red", size=3)

    chart = (points + regression).properties(width=800, height=800)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(chart, use_container_width=False)

    st.subheader("5. Quelle équipe est la plus ennuyante A ?( Histogramme des matchs nuls)", divider=True)
    st.write("Légende: Ce visuel montre quelle sont les équipe qui font le plus de match nul . Et c'est Lorient, le Havre et Rennes qui gagnent avec 7 matchs nuls chacun")

    df_sorted = df.sort_values("Match_nul", ascending=True).reset_index()

    chart = alt.Chart(df_sorted).mark_bar(color="#b852dd").encode(
        x=alt.X("Equipe:N", sort=None),
        y=alt.Y("Match_nul:Q")
    )

    st.altair_chart(chart, use_container_width=True)

    st.write('Réponse :')

    st.subheader("6. Les buts font-ils le classement? (Comparaison Points / Différence de buts", divider=True)
    st.write("Légende : Ce visuel compare la différence de but et le nombre de point.")

    st.bar_chart(df[["Points", "Difference_but"]], use_container_width=True)

    st.subheader("7. Faut-il faire des matchs nul pour gagner ?  ", divider=True)
    st.write('Légende : Ce visuel compare le nombre de match nul et le nombre de point . Et la réponse est clair, Lens n a pas besion de faire de match nul pour gagner ! ')

    st.bar_chart(
        df[["Points", "Match_nul"]],
        color=["#EA61CA", "#80AFF1"],
        stack=False
    )

    st.subheader("8. Qui est le plus équilibré ? ( Comparaison Buts mis/ But pris )", divider=True)
    st.write('Légende : Ce rapport compare les Buts mis et les Buts pris . Ainsi Monaco semble aimer mettre des buts et prendre des but !')

    st.bar_chart(
        df[["But_mis", "But_pris"]],
        color=["#BFF640", "#E9B771"],
        use_container_width=True
    )

    st.subheader("9. Qui est le plus équilibré B ? ( Comparaison Buts mis/ But pris )", divider=True)
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

    chart = (points + regression).properties(width=800, height=800)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.altair_chart(chart, use_container_width=False)

    st.subheader("10 .Qui fait le spectacle ?( But marqué + But encaissé )", divider=True)
    st.write("Légende: Ce visuel montre quelle sont les équipe qui font le plus de match nul . Et c'est Lorient, le Havre et Rennes qui gagnent avec 7 matchs nuls chacun")

    df_sorted = df.sort_values("Addition_but", ascending=True).reset_index()

    chart = alt.Chart(df_sorted).mark_bar(color="#b852dd").encode(
        x=alt.X("Equipe:N", sort=None),
        y=alt.Y("Match_nul:Q")
    )

    st.altair_chart(chart, use_container_width=True)

    st.subheader("11. Peut-on marquer beaucoup de but et faire beaucoup de match nul ? ", divider=True)
    st.write("Légende: De ce graphique ce détache Le Havre qui fait beaucoup de match nul et ne montre pas beaucoup de but ")

    df_alt = df.reset_index()

    chart = alt.Chart(df_alt).mark_circle(size=80).encode(
        x=alt.X('Addition_but:Q', title='Addition but'),
        y=alt.Y('Match_nul:Q', title='Match nul'),
        color=alt.Color('Equipe:N', legend=alt.Legend(title="Équipe")),
        tooltip=['Equipe:N', 'Addition_but:Q', 'Match_nul:Q']
    ).properties(
        title="Nuage de points : Addition but vs Match nul"
    )

    st.altair_chart(chart, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.title(" Buts mis")
        fig, ax = plt.subplots(figsize=(20, 8.5))
        sns.boxplot(
            y=df["But_mis"],
            width=0.4,
            linewidth=0.5,
            whis=1.2,
            flierprops={"markersize": 5},
            ax=ax
        )
        ax.tick_params(axis='both', labelsize=20)
        ax.set_ylabel("Points", fontsize=20)
        ax.set_title("Les buts mis ", fontsize=20)
        st.pyplot(fig)

    with col2:
        st.title(" Buts pris")
        fig, ax = plt.subplots(figsize=(20, 8.5))
        sns.boxplot(
            y=df["But_pris"],
            width=0.4,
            linewidth=0.5,
            whis=1.2,
            flierprops={"markersize": 5},
            ax=ax
        )
        ax.tick_params(axis='both', labelsize=20)
        ax.set_ylabel("Points", fontsize=20)
        ax.set_title("Les buts mis ", fontsize=20)
        st.pyplot(fig)

    with col3:
        st.title("Matchs nul ")
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.pie(
            df["Match_nul"],
            labels=df.index,
            autopct="%1.1f%%",
            startangle=90
        )
        ax.axis("equal")
        st.pyplot(fig, use_container_width=False)

    st.subheader("Statistiques descriptives")
    st.dataframe(df.describe())

    df_alt = df.reset_index()

    chart = alt.Chart(df_alt).mark_circle(size=80).encode(
        x=alt.X('But_pris:Q', title='Buts pris'),
        y=alt.Y('But_mis:Q', title='Buts mis'),
        color=alt.Color(
            'Points:Q',
            scale=alt.Scale(scheme='viridis'),
            title='Points'
        ),
        tooltip=['Equipe:N', 'But_pris:Q', 'But_mis:Q', 'Points:Q']
    ).properties(
        title="Nuage de points : couleur = Points"
    )

    st.altair_chart(chart, use_container_width=True)
