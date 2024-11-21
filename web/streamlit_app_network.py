import streamlit as st
import pandas as pd
import plotly.express as px
from st_functions_network import *
# Set path of the data
PATHS = {
    "Attack 1": "results/cleaned/Network_dataset/attack_1_cleaned.csv",
    "Attack 2": "results/cleaned/Network_dataset/attack_2_cleaned.csv",
    "Attack 3": "results/cleaned/Network_dataset/attack_3_cleaned.csv",
    "Attack 4": "results/cleaned/Network_dataset/attack_4_cleaned.csv",
}

DATASET_INDEX_MAPPING = {
    "Attack 1": 1,
    "Attack 2": 2,
    "Attack 3": 3,
    "Attack 4": 4,
}

# Streamlit page configuration
st.set_page_config(
    page_title="Analysis of Network Attacks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Analysis of Network Attacks 📊")
st.markdown(
    "Dashboard to explore and analyze Network Attacks datasets interactively."
)

# Cache to not reload the data every time
@st.cache_data
def load_data(path, nrows=None):
    return pd.read_csv(path, low_memory=False, header=0, encoding='utf-8', nrows=nrows)

# Load all datasets
datasets = {key: load_data(path) for key, path in PATHS.items()}

# Sidebar options
st.sidebar.title("Dataset Options")
selected_dataset = st.sidebar.radio("Select a dataset to analyze:", list(datasets.keys()))
show_dataframe = st.sidebar.checkbox("Show the raw data for the selected dataset")
index_dataframe = DATASET_INDEX_MAPPING[selected_dataset]

# Display selected dataset
df = datasets[selected_dataset]
# Compter le nombre d'occurrences de chaque label en fonction de proto
df_counts = df.groupby(['proto', 'label']).size().reset_index(name='count')
if show_dataframe:
    st.subheader(f"Raw Data for {selected_dataset}")
    st.dataframe(df.head(1000)) #revoir

# Tabs for different analyses
tab1,tab2,tab3,tab4,tab5,tab6,tab7,tab8 = st.tabs([ "Percentage of attacks","Histograms","co-occurrence matrix","mean","XGBOOST","CART","Random forest","KNN"])

with tab1:
    st.subheader("Percentage of attacks by each protocols")
    camembert(df_counts)

with tab2:
    st.subheader("Histograms")
    histogramme(df_counts,'proto',"label")
    histogramme(df_counts,'label',"Attaques différentes")

with tab3:
    st.subheader(" co-occurrence matrix")
    matrice_coocurrence(df)

with tab4:
    st.subheader("mean")
    mean_display(df)

with tab5:
    st.subheader("XGBOOST Results")
    st.markdown("Train and test a XGBOOST classifier.")
    XGBoost_display(index_dataframe)

with tab6:
    st.subheader("CART Results")
    st.markdown("Train and test a CART classifier.")
    CART_display(index_dataframe)
    
with tab7:
    st.subheader("Random forest Results")
    st.markdown("Train and test a Random forest classifier.")
    RF_display(index_dataframe)

with tab8:
    st.subheader("KNN")
    st.markdown("Train and test a KNN classifier.")
    KNN_display(index_dataframe)
