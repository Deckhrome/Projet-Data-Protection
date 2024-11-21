import pandas as pd
import plotly.graph_objects as go
import plotly.subplots as sp
import streamlit as st
import plotly.express as px
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import numpy as np
import pandas as pd


def camembert(df):
    proto1="TCP"
    proto2="Modbus"
    total_counts = df.groupby('proto')['count'].transform('sum')
    df['percentage'] = (df['count'] / total_counts) * 100 
    # Filtrer les données pour les protocoles actuels
    df_proto1 = df[df['proto'] == proto1]
    df_proto2 = df[df['proto'] == proto2]
    count1=df_proto1.sum()
    count2=df_proto2.sum()
    # Calculer le nombre total d'attaques pour chaque protocole
    total_attacks_proto1 = df_proto1['percentage'].sum()
    total_attacks_proto2 = df_proto2['percentage'].sum()
    
    # Créer une figure avec deux sous-graphiques
    fig = sp.make_subplots(rows=1, cols=2, 
                           subplot_titles=(f'Pourcentage d\'attaques pour le protocole {proto1} (Total: {count1["count"]})',
                                           f'Pourcentage d\'attaques pour le protocole {proto2} (Total: {count2["count"]})'),
                           specs=[[{'type':'pie'}, {'type':'pie'}]])  # Spécifier que les deux sous-graphiques sont des camemberts

    # Créer le premier camembert
    fig.add_trace(
        go.Pie(labels=df_proto1['label'], values=df_proto1['percentage'], hole=0.3),  # Si vous voulez un donut, utilisez 'hole'
        row=1, col=1
    )
    
    # Créer le deuxième camembert
    fig.add_trace(
        go.Pie(labels=df_proto2['label'], values=df_proto2['percentage'], hole=0.3),
        row=1, col=2
    )

    # Mettre à jour la mise en page
    fig.update_layout(title_text='Comparaison des attaques par protocole', title_x=0.5)

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)

def histogramme(df,x,title):

    # Créez le plot
    fig = px.histogram(df, x=x,y="count",
                title=title,
                labels={'proto': 'Protocole', 'label': 'Nombre d\'attaques'},
                color="label")

    # Affichez le graphique
    st.plotly_chart(fig, use_container_width=True)

def XGBoost_display(index_df):
    st.markdown("Select the dataset to use for the XGBOOST analysis.")
    path_cm = f"results/figures/network/df_{index_df}/Confusion_XGBOOST.png"
    path_acc = f"results/figures/network/df_{index_df}/res_XGBOOST.png"
    path_bm = f"results/figures/network/df_{index_df}/balanced_matthew_XGBOOST.png"
    st.image(path_cm, use_container_width=True)
    st.image(path_acc, width=600)
    st.image(path_bm, width=600)

def CART_display(index_df):
    st.markdown("Select the dataset to use for the CART analysis.")
    path_cm = f"results/figures/network/df_{index_df}/Confusion_CART.png"
    path_acc = f"results/figures/network/df_{index_df}/res_cart.png"
    path_bm = f"results/figures/network/df_{index_df}/balanced_matthew_CART.png"
    st.image(path_cm, use_container_width=True)
    st.image(path_acc, width=600)
    st.image(path_bm, width=600)


def RF_display(index_df):
    st.markdown("Select the dataset to use for the CART analysis.")
    path_cm = f"results/figures/network/df_{index_df}/Confusion_random_forest.png"
    path_acc = f"results/figures/network/df_{index_df}/res_random_forest.png"
    path_bm = f"results/figures/network/df_{index_df}/balanced_matthew_random_forest.png"
    # Affiche l'image de confusion avec la largeur par défaut
    st.image(path_cm, use_container_width=True)
    
    # Affiche l'image d'exactitude avec une largeur plus petite (par exemple 50% de la largeur du conteneur)
    st.image(path_acc, width=600)  # Ajustez la largeur selon vos besoins
    st.image(path_bm, width=600)

def KNN_display(index):
    if index <=2:
        st.markdown("Select the dataset to use for the CART analysis.")
        #path_cm = f"results/figures/network/df_1/Confusion_random_forest.png"
        path_acc = f"results/figures/network/df_{index}/res_KNN.png"
        
        # Affiche l'image de confusion avec la largeur par défaut
        #st.image(path_cm, use_container_width=True)
        
        # Affiche l'image d'exactitude avec une largeur plus petite (par exemple 50% de la largeur du conteneur)
        st.image(path_acc, width=600)  # Ajustez la largeur selon vos besoins

def matrice_coocurrence(df):
    # Créer une table croisée (contingency table) des adresses MAC et IP
    crosstab = pd.crosstab(df['mac_d'], df['ip_d'])
    
    # Création de la carte thermique (heatmap) de la table croisée
    fig = px.imshow(crosstab,
                    text_auto=True,  # Affiche les valeurs dans chaque cellule
                    color_continuous_scale='RdBu',  # Palette de couleurs
                    title="Co-occurrence matrix"
                )
    
    # Adjust the figure size to make it larger
    fig.update_layout(
        width=1200,  # You can change this value to make the heatmap wider
        height=800   # You can change this value to make the heatmap taller
    )
    
    # Affichage de la figure avec un container Streamlit qui ajuste la largeur
    st.plotly_chart(fig, use_container_width=True)



def mean_display(df_attack):
    normal_dpkt=df_attack[df_attack["label"]=="normal"]
    mean_normal_dpkt=normal_dpkt["n_pkt_src"].mean()

    MITM_dpkt=df_attack[df_attack["label"]=="MITM"]
    mean_MITM_dpkt=MITM_dpkt["n_pkt_src"].mean()

    DoS_dpkt=df_attack[df_attack["label"]=="DoS"]
    mean_DoS_dpkt=DoS_dpkt["n_pkt_src"].mean()

    physical_fault_dpkt=df_attack[df_attack["label"]=="physical fault"]
    mean_physical_fault_dpkt=physical_fault_dpkt["n_pkt_src"].mean()

    # Données des moyennes calculées
    categories = ['Normal', 'MITM', 'DoS', 'Physical Fault']
    means = [mean_normal_dpkt, mean_MITM_dpkt, mean_DoS_dpkt, mean_physical_fault_dpkt]

    # Créer un DataFrame pour Plotly
    data = pd.DataFrame({
        'Category': categories,
        'Mean Packet Count': means
    })

    # Créer le barplot avec Plotly
    fig = px.bar(data, x='Category', y='Mean Packet Count', 
             title='Moyenne du nombre de paquets par catégorie',
             labels={'Category': 'Type d\'attaque', 'Mean Packet Count': 'Moyenne des paquets (n_pkt_src)'},
             color='Category', color_discrete_sequence=px.colors.qualitative.Set2)

    # Afficher le graphique
    st.plotly_chart(fig, use_container_width=True)