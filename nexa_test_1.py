import streamlit as st 

st.set_page_config(page_title="Steeve Orville Application Quatro",
     layout="wide")


st.title(":blue[Prédiction] d'approbation de prèt :cold:",help=" Merci d'être là mon ami !", text_alignment="center")

st.write("Bienvenue dans  notre application ! ")


st.space("medium")


import streamlit as st

left, middle, right = st.columns(3)
if left.button("Exploration des données", width="stretch"):
    left.markdown("You clicked the plain button.")
if middle.button("Prédiction", width="stretch"):
    middle.markdown("You clicked the emoji button.")
if right.button("Performance du modele", width="stretch"):
    right.markdown("You clicked the Material button.")






import streamlit as st
import pandas as pd


st.sidebar.title("Steeve Orville Application")
st.sidebar.image("logo.jpg")
add_selectbox = st.sidebar.selectbox(
    "Choisis ton modèle ",
    ("Logistique Regression", "Random Forest")
)
st.space("medium")



st.space("medium")
st.subheader("Metriques", divider=True)
col1, col2, col3,col4 = st.columns(4)
col1.metric("Nombre total de demandes", "70 °F", "1.2 °F")
col2.metric("Taux d'approbation global", "9 mph", "-8%")
col3.metric("Montant moyen des prêts", "86%", "4%")
col4.metric("Revenue moyen", "86%", "4%")

import plotly.express as px 




df = pd.read_excel("Tableau_clean6.xlsx")
df0=df[['TotalIncome','LoanAmountToIncome','EMI','Log_LoanAmount']]

faux = pd.read_csv("loan_data.csv")
st.space("medium")
st.subheader("Distributions", divider=True)

col1, col2= st.columns(2)







col1.write("Histogramme des revenus")
col1.bar_chart(faux['ApplicantIncome'])

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt



fig, ax = plt.subplots()

sns.boxplot(data=faux, x="LoanAmount", ax=ax)



col2.write("Répartition des montants  de prêt")
col2.pyplot(fig)

st.space("medium")
st.subheader("Corrélation", divider=True)


st.write("Heatmap Correlation")

# calcul matrice de corrélation
corr = df0.corr()

fig, ax = plt.subplots()

sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig)


import streamlit as st
import pandas as pd

# dataframe df déjà chargé
approval_rate = faux.groupby("Education")["Loan_Status"].apply(lambda x: (x == "Y").mean())
st.subheader("Taux d'approbation par éducation", divider=True)
st.dataframe(approval_rate)
st.bar_chart(approval_rate)
st.write(faux.columns)

#st.dataframe(df.style.highlight_max(axis=0))