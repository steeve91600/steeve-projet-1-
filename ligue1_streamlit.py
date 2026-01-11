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
    page_title="Ligue 1 - Classement live",
    layout="wide"
)

st.title("⚽ Analyse du championnat de France de football Ligue 1 ")

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












st.subheader("Faut-il marquer beaucoup pour gagner le championnat ? ( Comparaison Buts mis/ Points final )")
st.write("Légende : Ce visuel compare le nombre de buts mis et le nombre de point. Et la réponse est que Lens domine ce championnat mais marque peu. Ce qui est triste car Marseille et Paris FC marque beaucoup sans penser à gagner le match !")
st.bar_chart(
    df[["But_mis", "Points"]],
    color=["#BEEF4C","#EF6DBD"],
    stack=False
)




st.subheader("Quelle équipe est la plus ennuyante A ?( Histogramme des matchs nuls)")

st.write("Légende: Ce visuel montre quelle sont les équipe qui font le plus de match nul . Et c'est Lorient qui gagne !")
st.bar_chart(df["Match_nul"])
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