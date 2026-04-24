import streamlit as st
import pandas as pd

st.set_page_config(page_title="LoL Partner Finder", layout="centered")

st.title("🔍 LoL Partner Finder")

# 1. Chargement de la base de données
@st.cache_data
def load_data():
    return pd.read_parquet('base_lol_complete.parquet')

df = load_data()

# 2. NOUVEAU : Création de la liste pour l'autocomplétion
@st.cache_data
def get_player_list(dataframe):
    # On prend tous les noms uniques, on enlève les cases vides, et on trie par ordre alphabétique
    joueurs = dataframe['playername'].dropna().unique().tolist()
    return sorted(joueurs, key=str.casefold)

liste_joueurs = get_player_list(df)

# 3. NOUVEAU : Menu déroulant avec barre de recherche intégrée
# On ajoute une case vide "" au début pour ne pas lancer une recherche dès l'ouverture du site
nom = st.selectbox(
    "Pseudo du joueur (tapez pour chercher) :", 
    options=[""] + liste_joueurs, 
    index=0
)

# 4. Logique d'affichage
if nom != "":
    # On a plus besoin de vérifier l'orthographe ou les majuscules puisque l'utilisateur a cliqué sur le bon nom !
    matchs = df[df['playername'] == nom][['gameid', 'side']]
    
    if not matchs.empty:
        partenaires = pd.merge(matchs, df, on=['gameid', 'side'])
        partenaires = partenaires[partenaires['playername'] != nom]
        
        stats = partenaires.groupby(['playername', 'teamname']).size().reset_index(name='Games')
        stats = stats.sort_values(by='Games', ascending=False)
        
        st.write(f"### Coéquipiers historiques de **{nom}**")
        st.dataframe(stats, use_container_width=True, hide_index=True)
    else:
        st.error("Une erreur est survenue lors de la récupération des données.")
