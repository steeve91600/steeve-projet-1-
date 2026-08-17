import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import altair as alt

def render():

    df = pd.read_excel('BoxofficeJuin2026.xlsx')

    st.set_page_config(
        page_title="Analyse du boxoffice américain",
        layout="wide"
    )

    st.title(" :red[Analyse boxoffice américain US du 6 au 12 juillet 2026 ] :clapper:")

    st.write("Bienvenue dans cette analyse du box-office américain de la dernière semaine de  juin 2026. Comme tu peux le constater en observant les données, le **box-office** ne correspond pas au nombre d'entrées au cinéma, mais aux **recettes générées en dollars** (c'est-à-dire à l'argent rapporté par les films).Autrement dit, les spectateurs sont parfois prêts à **payer cher pour voir un bon film**.        ")
    st.write("De plus , je dois te dire, que j'aimerais te guider vers le meilleurs film , mais mon vrai boulot de data analyst est de t'expliquer ce que raconte CE tableau .")
    st.write("Commençons maintenant par le **sommaire**.")
    st.header("I. Description des colonnes de la liste ")

    desc_df = pd.DataFrame({
        "Colonne": [
            "current_rank",
            "previous_rank",
            "title",
            "occasion",
            "weekend_gross",
            "weekend_chg",
            "theaters",
            "theater_chg",
            "theater_avg",
            "cumulative_gross",
            "weeks",
            "distributor",
            "img_url",
            "rev_norm"
        ],
        "Description": [
            "Classement actuel du film au box-office pour le week-end considéré.",
            "Classement du film lors du week-end précédent.",
            "Titre du film.",
            "Événement ou période particulière associée aux données (par exemple un week-end spécifique ou une fête).",
            "Recettes générées pendant le week-end (en dollars).",
            "Évolution des recettes du week-end par rapport au week-end précédent (en %).",
            "Nombre de salles dans lesquelles le film est diffusé.",
            "Variation du nombre de salles par rapport au week-end précédent.",
            "Recette moyenne par salle pendant le week-end.",
            "Recettes cumulées du film depuis sa sortie (en dollars).",
            "Nombre de semaines écoulées depuis la sortie du film.",
            "Société chargée de la distribution du film.",
            "URL de l'affiche ou de l'image du film.",
            "Recettes normalisées (variable transformée pour faciliter les analyses statistiques)."
        ]
    })

    st.dataframe(desc_df, use_container_width=True)

    df = df.drop(columns=["Unnamed: 0", "index","img_url","occasion"])

    st.header("II.  Liste complete des films")
    st.dataframe(df, use_container_width=True)

    st.header("III. Quels films ont fait le plus de recettes cette semaine ?")

    df1 = (
        df.sort_values("weekend_gross", ascending=False)
          .head(10)
          .sort_values("weekend_gross")
    )

    fig = px.bar(
        df1,
        x="weekend_gross",
        y="title",
        orientation="h",
        text="weekend_gross",
        labels={
            "weekend_gross": "Recettes du week-end ($)",
            "title": "Film"
        }
    )

    fig.update_layout(
        height=600,
        yaxis=dict(title=""),
        xaxis=dict(title="Recettes ($)")
    )

    st.plotly_chart(fig, use_container_width=True)

    st.write(":red[***Explication:*** Ces recettes correspondent au rentrées d’argents en dollards sur une  semaine. Ainsi on ne prend en compte que cette semaine . De plus  si le film a  couté 100 millons de dollards en publicité , il est normal que ça marche la première semaine . Ainsi quelquepart , on n’en sait peu, car il y a beaucoup de facteur qui peuvent influencer les recettes sur une semaine.]")

    st.header("IV. Comment sont répartie les  recettes de film de cette semaine ?")

    df1 = df.sort_values("weekend_gross", ascending=False)

    fig = px.bar(
        df1,
        y="weekend_gross",
        x="title",
        orientation="v",
        text="weekend_gross",
        labels={
            "weekend_gross": "Recettes du week-end ($)",
            "title": "Film"
        }
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.write("***Explication:*** Il n'y a qu'une dixaine de films qui dépasse de Millions de recette par semaine . C'est pas très équitable niveau recette . Ainsi on irait tous voir lr même film .")

    st.header("V. Comment sont répartie les  recettes de film depuis leur sortie au cinéma ?")

    df1 = df.sort_values("cumulative_gross", ascending=False)

    fig = px.bar(
        df1,
        y="cumulative_gross",
        x="title",
        orientation="v",
        text="cumulative_gross",
        labels={
            "cumulative_gross": "Recettes du week-end ($)",
            "title": "Film"
        }
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.write("***Explication:*** On remarque que c'est plus homogène que la répartition des recettes par semaine (tableau précédent),donc tout ne se joue pas la première semaine .")

    st.header("IX. Répartition des recettes de cette semaine par producteur ?")

    df5 = (
        df.groupby("distributor", as_index=False)["weekend_gross"]
          .sum()
          .sort_values("weekend_gross", ascending=False)
    )

    fig = px.bar(
        df5,
        y="weekend_gross",
        x="distributor",
        orientation="v",
        text="weekend_gross",
        labels={
            "distributor": "Distributeur",
            "weekend_gross": "Recettes totales ($)"
        }
    )

    fig.update_layout(height=600)

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.write("***Explication:*** La répartition des recettes par producteur decalque la répartition des recettes par film, c'est donc on miserais tout sur un film")

    st.header("IX. Répartition des recettes total par producteur ?")

    df5 = (
        df.groupby("distributor", as_index=False)["cumulative_gross"]
          .sum()
          .sort_values("cumulative_gross", ascending=False)
    )

    fig = px.bar(
        df5,
        y="cumulative_gross",
        x="distributor",
        orientation="v",
        text="cumulative_gross",
        labels={
            "distributor": "Distributeur",
            "cumulative_gross": "Recettes totales ($)"
        }
    )

    fig.update_layout(height=600)

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.header("VIII. Quels producteurs sont les plus présents au box-office")

    df3 = df["distributor"].value_counts().reset_index()
    df3.columns = ["distributor", "count"]

    df4 = df3.sort_values("count", ascending=False).sort_values("count")

    fig = px.bar(
        df4,
        y="count",
        x="distributor",
        orientation="v",
        text="count",
        labels={
            "distributor": "Distributeur",
            "count": "Nombre d'apparitions"
        }
    )

    fig.update_layout(height=600)

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.write("***Explication:*** Ce graphique explique qu'il n'y a pas de folie . Personne ne produit 10 film en une semaine. Il n'y a pas de tactique comme ça !")

    st.write(df["weekend_chg"].dtype)
    st.write(df["weekend_chg"].apply(type).value_counts())

    st.header("IV.  Évolution des recettes du week-end par rapport au week-end précédent (en %).")

    df["weekend_chg"] = pd.to_numeric(df["weekend_chg"], errors="coerce")

    df1 = df.sort_values("weekend_chg", ascending=False)

    fig = px.bar(
        df1,
        y="weekend_chg",
        x="title",
        orientation="v",
        text="weekend_chg",
        labels={
            "weekend_chg": "Evoluation des recette (en %)",
            "title": "Film"
        }
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.write("***Explication:*** Certaines évolutions des recettes sont en positive , c'est donc que les gens ont adoré ( comme Omaha avec plus 300 % !!). Sinon la tendance est au négatif, c'est donc que le cinéma, c'est décevant en général .")

    st.header("III. Il y a -t-il des valeurs folle dans les recettes de cette semaine ? ( PLUS TARD ) ")

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(df["weekend_gross"])
    ax.set_title("Boîte à moustaches de Weekend Gross")
    ax.set_ylabel("Weekend Gross")
    st.pyplot(fig)

    st.header("III.Enlevons les valeurs abérrantes ( PLUS TARD ) ")

    Q1 = df["weekend_gross"].quantile(0.25)
    Q3 = df["weekend_gross"].quantile(0.75)
    IQR = Q3 - Q1

    borne_inf = Q1 - 1.5 * IQR
    borne_sup = Q3 + 1.5 * IQR

    df_sans_outliers = df[
        (df["weekend_gross"] >= borne_inf) &
        (df["weekend_gross"] <= borne_sup)
    ]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.boxplot(df_sans_outliers["weekend_gross"])
    ax.set_title("Boîte à moustaches de Weekend Gross")
    ax.set_ylabel("Weekend Gross")
    st.pyplot(fig)

    st.header("VI B. Parlons du nombre de semaine au cinéma")

    df1 = (
        df.sort_values("weeks", ascending=False)
          .head(10)
          .sort_values("weeks")
    )

    fig = px.bar(
        df1,
        x="weeks",
        y="title",
        orientation="h",
        text="weeks",
        labels={
            "weeks": "Nombre de semaine au Box office",
            "title": "Film"
        }
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.write(" ***Explication:*** Que veux dire le nombre de semaine au cinéma d’un film ? Natchez viens de passer 34 semaine au cinema , mais qu’est ce que ça veut dire ? Est le plus beau film du monde ? Et bien d’après Google, un film reste en moyenne 10 semaines en salle , et ensuite ça n'a pas vraiment de sens .Donc  pour avoir une bonne echelle nous allons éliminer les films de plus de 10 semaines  ( car audessus cela serait  une extravageance). ")

    st.header("VII. Recette de la dernière semaine et ancienneté")

    dfa=df[['title','weeks','weekend_gross']].sort_values("weeks", ascending=False)

    st.dataframe(dfa)

    st.header("VIII. Vérification graphique")

    df_alt = df.reset_index()

    chart = alt.Chart(df_alt).mark_circle(size=80).encode(
        x=alt.X('weekend_gross:Q', title='weekend_gross'),
        y=alt.Y("weeks:Q", title="weeks", scale=alt.Scale(zero=False)),
        color=alt.Color('title:N', legend=alt.Legend(title="title")),
        tooltip=['title:N', 'weekend_gross:Q', 'weeks:Q']
    ).properties(
        title="Nuage de points : Ancienneté vs Weekend Gross"
    )

    st.altair_chart(chart, use_container_width=True)

    st.header("IV. Quels films ont fait le plus de recette au total depuis leur sortie ?")

    df1 = (
        df.sort_values("cumulative_gross", ascending=False)
          .head(10)
          .sort_values("cumulative_gross")
    )

    fig = px.bar(
        df1,
        x="cumulative_gross",
        y="title",
        orientation="h",
        text="cumulative_gross",
        labels={
            "weekend_gross": "Recettes total ($)",
            "title": "Film"
        }
    )

    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)

    st.header("VIII. Quels producteurs sont les plus présents au box-office")

    df3 = df["distributor"].value_counts().reset_index()
    df3.columns = ["distributor", "count"]

    df4 = (
        df3.sort_values("count", ascending=False)
           .head(10)
           .sort_values("count")
    )

    fig = px.bar(
        df4,
        x="count",
        y="distributor",
        orientation="h",
        text="count",
        labels={
            "count": "Nombre d'apparitions",
            "distributor": "Distributeur"
        }
    )

    fig.update_layout(height=600)

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.header("IX. Quels distributeurs ont généré le plus de recettes ?")

    df5 = (
        df.groupby("distributor", as_index=False)["weekend_gross"]
          .sum()
          .sort_values("weekend_gross", ascending=False)
          .head(10)
          .sort_values("weekend_gross")
    )

    fig = px.bar(
        df5,
        x="weekend_gross",
        y="distributor",
        orientation="h",
        text="weekend_gross",
        labels={
            "weekend_gross": "Recettes totales ($)",
            "distributor": "Distributeur"
        }
    )

    fig.update_layout(height=600)

    fig.update_traces(textposition="outside")

    st.plotly_chart(fig, use_container_width=True)

    st.header("X.Quels films ont le plus monté dans la classement cette semaine")

    df["previous_rank_num"] = pd.to_numeric(df["previous_rank"], errors="coerce")
    df["augmentation_rank_num"] = df["current_rank"] - df["previous_rank_num"]

    df["augmentation_rank"] = df["augmentation_rank_num"]
    df.loc[df["previous_rank"] == "-", "augmentation_rank"] = "-"

    df7 = (
        df[["title", "current_rank", "previous_rank", "augmentation_rank", "augmentation_rank_num"]]
        .sort_values("augmentation_rank_num")
    )

    df7 = df7.drop(columns="augmentation_rank_num")

    st.dataframe(df7)

    st.write(" **Explication** : La nouvelle  colonne 'augmentation_rank' et la soustraction entre previous_rank et current_rank . Ainsi on voit que 'O Horizon' est le film qui a le plus monté dans le classement cette semaine... J'irais donc voir 'O Horizon' au cinema si j'étais vous ! Il est évident que 'O Horizon' est la plus bonne surprise ")

    st.header("XI. Vérification graphique")

    df_alt = df.reset_index()

    chart = alt.Chart(df_alt).mark_circle(size=80).encode(
        x=alt.X('current_rank:Q', title='current_rank'),
        y=alt.Y('previous_rank:Q', title='previous_rank'),
        color=alt.Color('title:N', legend=alt.Legend(title="title")),
        tooltip=['title:N', 'current_rank:Q', 'previous_rank:Q']
    ).properties(
        title="Nuage de points : Addition but vs Match nul"
    )

    st.altair_chart(chart, use_container_width=True)

    st.header("XII. Headmap de corrélation")

    st.write(" il y a quelquechose qu’on ne peut pas calculer car les différence de recette peuvent être trop enorme. Regardons ça en transversale avec le headmap de corrélation ")

    df_corr = df[["weeks", "weekend_gross", "current_rank","previous_rank","cumulative_gross"]]

    corr = df_corr.select_dtypes(include="number").corr()

    fig, ax = plt.subplots(figsize=(8, 6))

    im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i,
                    f"{corr.iloc[i, j]:.2f}",
                    ha="center", va="center",
                    color="black")

    fig.colorbar(im, ax=ax)

    st.pyplot(fig)

    st.write("***Explication*** : ON peut voir que plus il y a de week au cinema et plus c'est un succès global.  ")

    st.header("VII. Prouvons un tendance bivarié")
