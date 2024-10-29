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
def load_data(path, nrows=None):
    return pd.read_csv(path, low_memory=False, header=0, sep=",", nrows=nrows)

df_show = load_data(path_attack1,1000)

# Checkbox on sidebar to show/hide the dataframe
CHK_1 = st.sidebar.checkbox("Show dataframe attack_1")

if CHK_1:
    # Limit the number of rows to display
    st.dataframe(
        df_show,
        column_config= {
            "Time": "Date and Time",
            "label" : st.column_config.TextColumn(
                "Label",
            ),
        }
    )

col1, col2 = st.columns(2)

df_attack1 = load_data(path_attack1)


# Subset with label_n == 1 to plot attacks and the rest is normal
df_attack1_attack = df_attack1[df_attack1["label_n"] == 1]
df_attack1_normal = df_attack1[df_attack1["label_n"] == 0]

# Plot the number of attacks by type
col1.markdown("## Number of attacks by type for attack_1")
col1.bar_chart(df_attack1["label"].value_counts())

# Plot the number of attacks by protocol
col1.markdown("## Number of real attacks by protocol for attack_1")
col1.bar_chart(df_attack1_attack["proto"].value_counts())
