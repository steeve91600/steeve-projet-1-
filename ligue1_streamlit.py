import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# CONFIG STREAMLIT
# -----------------------------

st.set_page_config(
    page_title="Ligue 2 - Classement live",
    layout="wide"
)


st.markdown(
    "<h1 style='color:#6ADFF7;text-align:center;'> Ligue 1 savoir ⚽</h1>",
    unsafe_allow_html=True
)

st.subheader("Intro")
st.write("Bienvenue sur le projet **Ligue 1 savoir**, réalisé et publié par  Steeve  le Dimanche 11 Janvier 2026. Ce projet a pour but de présenter l’analyse de donnée .  ")
st.write("Nommée « Ligue 1 savoir » , car l’objectif c’est le savoir et pas l’avoir . Nous allons donc essayer de comprendre en profondeur, c’est quoi la ligue 1 . Pour ceux qui ne savent rien , vraiment rien … la « Ligue 1 » , c’est le plus haut niveau du championnat de France de football . ")
st.write(" Le premier chapitre de cette analyse portera sur le tableau  « Classement Général » . Ce tableau , résume ce qui se passe d’une manière général dans la Ligue 1 . Ce tableau est en streaming live, donc actualisé en temps réel . Les graphiques sont aussi en temps réel , seul les légendes de graphique et les titres sont manuels ( actualisé une fois par mois ). ")
st.subheader("Légende des colonnes")
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

# -----------------------------
# AFFICHAGE
# -----------------------------
st.subheader("📊 Classement général")
st.dataframe(df, use_container_width=True)









df.sort_values(["But_mis"] , ascending=True)


st.subheader("Faut-il marquer beaucoup pour gagner le championnat ? ( Comparaison Buts mis/ Points final )")
st.write("Légende : Ce visuel compare le nombre de buts mis et le nombre de point. Et la réponse est que Lens domine ce championnat mais marque peu. Ce qui est triste car Marseille et Paris FC marque beaucoup sans penser à gagner le match !")
st.bar_chart(
    df[["But_mis", "Points"]],
    color=["#BEEF4C","#EF6DBD"],
    stack=False
)





import altair as alt

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

chart = (points + regression).properties(
    width=800,
    height=800
)




col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.altair_chart(chart, use_container_width=False)


st.subheader("Quelle équipe est la plus ennuyante A ?( Histogramme des matchs nuls)")

st.write("Légende: Ce visuel montre quelle sont les équipe qui font le plus de match nul . Et c'est Lorient, le Havre et Rennes qui gagnent avec 7 matchs nuls chacun")




import altair as alt

df_sorted = df.sort_values("Match_nul", ascending=True).reset_index()

chart = alt.Chart(df_sorted).mark_bar(color="#b852dd").encode(
    x=alt.X("Equipe:N", sort=None),
    y=alt.Y("Match_nul:Q")
)

st.altair_chart(chart, use_container_width=True)


st.write('Réponse :')






st.subheader("Quelle équipe est la plus ennuyante B ?(Cammembert des matchs nuls)")

st.write("Légende: Ce visuel montre quelle sont les équipe qui font le plus de match nul . Et c'est Lorient qui gagne !")

fig, ax = plt.subplots(figsize=(12, 4))

ax.pie(
    df["Match_nul"],
    labels=df.index,
    autopct="%1.1f%%",
    
    startangle=90
)

ax.axis("equal")  # cercle parfait

st.pyplot(fig, use_container_width=False)


st.subheader("Les buts font-ils le classement? (Comparaison Points / Différence de buts")
st.write("Légende : Ce visuel compare la différence de but et le nombre de point.")

st.bar_chart(
    df[["Points", "Difference_but"]],
    use_container_width=True
)


st.subheader("Faut-il faire des matchs nul pour gagner ?  ")
st.write('Légende : Ce visuel compare le nombre de match nul et le nombre de point . Et la réponse est clair, Lens n a pas besion de faire de match nul pour gagner ! ')

st.bar_chart(
    df[["Points", "Match_nul"]],
    color=["#EA61CA","#80AFF1"],
    stack=False
)
st.subheader("Qui aime l'action ? ( Comparaison Buts mis/ But pris )")
st.write('Légende : Ce rapport compare les Buts mis et les Buts pris . Ainsi Monaco semble aimer mettre des buts et prendre des but !')
st.bar_chart(
    df[["But_mis", "But_pris"]],
    color=["#BFF640","#E9B771"],
    use_container_width=True
)





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

 ax.axis("equal")  # cercle parfait

 st.pyplot(fig, use_container_width=False)


st.subheader("Statistiques descriptives")
st.dataframe(df.describe())






st.write("------------------------------------------------------------------------------------")
st.write("--------------------------------ELDORADO VERSION 1 --------------------------------")
st.write("------------------------------------------------------------------------------------")

import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# -----------------------------
# Configuration
# -----------------------------
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}
BASE_URL = "https://www.pagesjaunes.fr"

# -----------------------------
# Récupération des URLs de pharmacie
# -----------------------------
def get_pharmacy_urls(search_url):
    urls = set()
    response = requests.get(search_url, headers=HEADERS, timeout=15)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    for a in soup.select("a.bi-denomination"):
        href = a.get("href")
        if href:
            if href.startswith("/"):
                href = BASE_URL + href
            if "annuaire" not in href:
                urls.add(href)
    return list(urls)

# -----------------------------
# Scraping d'une seule pharmacie
# -----------------------------
def scrape_pharmacy(url):
    try:
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")

        # Nom
        nom_tag = soup.select_one("div.denom h1")
        nom = nom_tag.get_text(strip=True) if nom_tag else None

        # Adresse
        adresses = []
        for span in soup.select("a.address span"):
            txt = span.get_text(strip=True)
            if txt and "Localiser" not in txt:
                adresses.append(txt)
        adresse_complete = " | ".join(adresses) if adresses else None

        return {
            "URL": url,
            "Nom_Entreprise": nom,
            "Adresse": adresse_complete
        }
    except:
        return {
            "URL": url,
            "Nom_Entreprise": None,
            "Adresse": None
        }

# -----------------------------
# Scraping global
# -----------------------------
def scrape_all_pharmacies(search_url):
    urls = get_pharmacy_urls(search_url)
    data = []

    progress = st.progress(0)

    for i, url in enumerate(urls, start=1):
        data.append(scrape_pharmacy(url))
        progress.progress(i / len(urls))
        time.sleep(0.5)  # anti-blocage PagesJaunes

    return pd.DataFrame(data)

# -----------------------------
# Interface Streamlit
# -----------------------------
st.set_page_config(page_title="Scraper Pharmacies", layout="wide")
st.title("💊 Scraper Pharmacies – PagesJaunes")
st.write("Colle une URL de recherche PagesJaunes (ex : pharmacies à Paris)")

with st.form("search_form"):
    search_url = st.text_input(
        "URL PagesJaunes",
        placeholder="https://www.pagesjaunes.fr/recherche/pharmacie/paris"
    )
    submitted = st.form_submit_button("Lancer le scraping")

if submitted:
    if not search_url.startswith("http"):
        st.error("❌ URL invalide")
    else:
        with st.spinner("Scraping en cours... (≈ 30 secondes)"):
            df = scrape_all_pharmacies(search_url)

        st.success(f"✅ {len(df)} pharmacies récupérées")
        st.dataframe(df)

        # Téléchargement CSV
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️ Télécharger en CSV",
            csv,
            "pharmacies_pagesjaunes.csv",
            "text/csv"
        )
