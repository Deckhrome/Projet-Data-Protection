import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE
import time

# Set path of the data
PATHS = {
    "Attack 1": "results/cleaned/phy_att_1.csv",
    "Attack 2": "results/cleaned/phy_att_2.csv",
    "Attack 3": "results/cleaned/phy_att_3.csv",
    "Attack 4": "results/cleaned/phy_att_4.csv",
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

# Display selected dataset
df = datasets[selected_dataset]
if show_dataframe:
    st.subheader(f"Raw Data for {selected_dataset}")
    st.dataframe(df)

# Function: Correlation matrix for Tank columns
def correlation_matrix(df, title="Correlation Matrix for Tank Columns"):
    tank_columns = [col for col in df.columns if "Tank" in col]
    if not tank_columns:
        st.warning("No Tank columns found in this dataset.")
        return
    correlation = df[tank_columns].corr()
    fig = px.imshow(
        correlation,
        text_auto=".2f",
        color_continuous_scale="rdylbu",
        title=title,
        labels=dict(color="Correlation"),
    )
    st.plotly_chart(fig, use_container_width=True)

# Function: Distribution by attack type
def distribution_by_attack(df, column, title="Distribution by Attack Type"):
    if column not in df.columns:
        st.warning(f"Column '{column}' not found in the dataset.")
        return
    fig = px.histogram(
        df,
        x=column,
        color="Label",
        barmode="overlay",
        title=title,
        labels={column: column, "Label": "Attack Type"},
    )
    st.plotly_chart(fig, use_container_width=True)

# Function: Proportion of states for boolean components
def boolean_proportion(df, column_prefix="Pump", title="Proportion of True States"):
    bool_columns = [col for col in df.columns if column_prefix in col]
    if not bool_columns:
        st.warning(f"No columns with prefix '{column_prefix}' found.")
        return
    proportions = {col: df[col].mean() for col in bool_columns}
    fig = px.bar(
        x=list(proportions.keys()),
        y=list(proportions.values()),
        labels={"x": "Components", "y": "Proportion True"},
        title=title,
        text_auto=True,
    )
    st.plotly_chart(fig, use_container_width=True)

def count_open_valves(df):
    valv_columns = [col for col in df.columns if 'Valv' in col]
    if valv_columns:
        df['Valv_True'] = df[valv_columns].sum(axis=1)

        fig = px.histogram(
            df,
            x='Valv_True',
            color='Label',
            barmode='overlay',
            title="Distribution of Open Valves by Attack Type",
            labels={'Valv_True': 'Number of Open Valves', 'Label': 'Attack Type'},
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No valve columns found in this dataset.")
        
def count_active_pump(df):
    pump_columns = [col for col in df.columns if 'Pump' in col]
    if pump_columns:
        df['Pump_True'] = df[pump_columns].sum(axis=1)
        
        # Create histogram
        fig = px.histogram(
            df,
            x='Pump_True',
            color='Label',
            barmode='overlay',
            title="Distribution of Active Pumps by Attack Type",
            labels={'Pump_True': 'Number of Active Pumps', 'Label': 'Attack Type'},
        )
        fig.update_layout(bargap=0.1)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No pump columns found in this dataset.")

def knn_display():
    # Select with slider which df number to use
    st.markdown("Select the dataset to use for the KNN analysis.")
    df_number = st.slider("Select the dataset number", 1, 4, 1)
    path_acc = f"results/figures/knn_accuracy_df_{df_number}.png"
    path_cm = f"results/figures/knn_cm_df_{df_number}.png"

    st.image(path_acc, use_column_width=True)
    st.image(path_cm, use_column_width=True)
    


# Tabs for different analyses
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Correlation Matrix", "Distributions", "Boolean States", "Open Valves", "Active Pumps","KNN"])

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
    st.markdown("Train and test a KNN classifier interactively by selecting the number of neighbors (k).")
    knn_display()




