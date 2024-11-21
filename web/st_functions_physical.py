import streamlit as st
import plotly.express as px
from st_functions_network import *
# Function: Display dataset information

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

# Function: Display the results of the Classification models

def knn_display(index_df):
    st.markdown("Select the dataset to use for the KNN analysis.")
    path_acc = f"results/figures/Physical dataset/df_{index_df}/knn_accuracy.png"
    path_cm = f"results/figures/Physical dataset/df_{index_df}/knn_conf_matrix_k_5.png"

    st.image(path_acc, use_container_width=True)
    st.image(path_cm, use_container_width=True)


def cart_display(index_df):
    st.markdown("Select the dataset to use for the CART analysis.")
    path_acc = f"results/figures/Physical dataset/df_{index_df}/cart_metrics_balanced.png"
    path_cm = f"results/figures/Physical dataset/df_{index_df}/cart_conf_matrix_balanced.png"

    st.image(path_acc, use_container_width=True)
    st.image(path_cm, use_container_width=True)

def rfc_display(index_df):
    st.markdown("Select the dataset to use for the RFC analysis.")
    path_acc = f"results/figures/Physical dataset/df_{index_df}/rf_metrics_balanced.png"
    path_cm = f"results/figures/Physical dataset/df_{index_df}/rf_conf_matrix_balanced.png"

    st.image(path_acc, use_container_width=True)
    st.image(path_cm, use_container_width=True)

def xgb_display(index_df):
    st.markdown("Select the dataset to use for the XGB analysis.")
    path_acc = f"results/figures/Physical dataset/df_{index_df}/xgb_metrics.png"
    path_cm = f"results/figures/Physical dataset/df_{index_df}/xgb_conf_matrix.png"

    st.image(path_acc, use_container_width=True)
    st.image(path_cm, use_container_width=True)
    
def mlp_display(index_df):
    st.markdown("Select the dataset to use for the MLP analysis.")
    path_acc = f"results/figures/Physical dataset/df_{index_df}/mlp_metrics.png"
    path_cm = f"results/figures/Physical dataset/df_{index_df}/mlp_conf_matrix.png"

    st.image(path_acc, use_container_width=True)
    st.image(path_cm, use_container_width=True)