import streamlit as st
import pandas as pd
import plotly.express as px
from st_functions_physical import * # Import all functions from st_functions_physical.py

# Set path of the data
PATHS = {
    "Attack 1": "results/cleaned/Physical dataset/phy_att_1_cleaned.csv",
    "Attack 2": "results/cleaned/Physical dataset/phy_att_2_cleaned.csv",
    "Attack 3": "results/cleaned/Physical dataset/phy_att_3_cleaned.csv",
    "Attack 4": "results/cleaned/Physical dataset/phy_att_4_cleaned.csv",
}

DATASET_INDEX_MAPPING = {
    "Attack 1": 1,
    "Attack 2": 2,
    "Attack 3": 3,
    "Attack 4": 4,
}

# Streamlit page configuration
st.set_page_config(
    page_title="Analysis of Physical Attacks",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Analysis of Physical Attacks 📊")
st.markdown(
    "Dashboard to explore and analyze physical attack datasets interactively."
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
if show_dataframe:
    st.subheader(f"Raw Data for {selected_dataset}")
    st.dataframe(df)

# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([ "Correlation Matrix",
                                                                        "Distributions",
                                                                        "Boolean States",
                                                                        "Open Valves",
                                                                        "Active Pumps",
                                                                        "KNN",
                                                                        "CART", 
                                                                        "RF",
                                                                        "XGB",
                                                                        "MLP"])

with tab1:
    st.subheader("Correlation Matrix for Tank Columns")
    correlation_matrix(df)

with tab2:
    st.subheader("Distribution of attack types")
    fig = px.histogram(
        df,
        x="Label",
        title="Distribution of Attack Types",
        labels={"Label": "Attack Type"},
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Distribution of Tank values by Attack Type")
    distribution_by_attack(df, "Tank_1", title="Distribution of Tank_1 by Attack Type")

    distribution_by_attack(df, "Tank_2", title="Distribution of Tank_2 by Attack Type")
    distribution_by_attack(df, "Tank_3", title="Distribution of Tank_3 by Attack Type")
    distribution_by_attack(df, "Tank_4", title="Distribution of Tank_4 by Attack Type")
    distribution_by_attack(df, "Tank_5", title="Distribution of Tank_5 by Attack Type")
    distribution_by_attack(df, "Tank_6", title="Distribution of Tank_6 by Attack Type")

    st.subheader("Distribution of Flow_sensor_1 by Attack Type")
    distribution_by_attack(df, "Flow_sensor_1", title="Distribution of Flow_sensor_1 by Attack Type")

with tab3:
    st.subheader("Proportion of True States for Pumps")
    boolean_proportion(df, column_prefix="Pump", title="Proportion of True States for Pumps")

    st.subheader("Proportion of True States for Valves")
    boolean_proportion(df, column_prefix="Valv", title="Proportion of True States for Valves")

with tab4:
    st.subheader("Distribution of Open Valves by Attack Type")
    st.markdown("This analysis computes the number of valves open for each sample and shows the distribution by attack type.")
    count_open_valves(df)

with tab5:
    st.subheader("Distribution of Pump States by Attack Type")
    st.markdown("This analysis computes the number of active pumps for each sample and shows the distribution by attack type.")
    count_active_pump(df)

with tab6:
    st.subheader("KNN Results")
    st.markdown("Train and test a KNN classifier.")
    knn_display(index_dataframe)

with tab7:
    st.subheader("CART Results")
    st.markdown("Train and test a CART classifier.")
    cart_display(index_dataframe)

with tab8:
    st.subheader("Random Forest Results")
    st.markdown("Train and test a RF classifier.")
    rfc_display(index_dataframe)

with tab9:
    st.subheader("XGBoost Results")
    st.markdown("Train and test a XGBoost classifier.")
    xgb_display(index_dataframe)

with tab10:
    st.subheader("MLP Results")
    st.markdown("Train and test a MLP classifier.")
    mlp_display(index_dataframe)


