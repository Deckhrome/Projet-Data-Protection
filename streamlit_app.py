import streamlit as st
import pandas as pd

path_attack1 = "/home/johan/Desktop/PDSSC/Projet/data/dataset/Network datatset/clean_csv/attack_1_cleaned.csv"

st.set_page_config(
    page_title="Analysis Network Attacks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Analysis Network Attacks")
st.markdown("_Diplay Attack 1 data v1_")

# Cache to not reload the data every time the script is run
@st.cache_data
def load_data(path):
    return pd.read_csv(path, low_memory=False, header=0, sep=",", nrows=1000)

df_1 = load_data(path_attack1)

# Checkbox on sidebar to show/hide the dataframe
CHK_1 = st.sidebar.checkbox("Show dataframe attack_1")

if CHK_1:
    # Limit the number of rows to display
    st.dataframe(
        df_1,
        column_config= {
            "Time": "Date and Time",
            "label" : st.column_config.TextColumn(
                "Label",
            ),
        }
    )



