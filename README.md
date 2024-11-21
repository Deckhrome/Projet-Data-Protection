# Project Data Protection

The objective of this project is to apply the data analysis chain on a cyberphysical dataset:

1) Using only network data
2) Using only physical data

Compare different algorithms (KNN, CART, Random Forest, XGBoost, MLP...)

Build a streamlit webapp providing an interactive interface to explore results.

## Installation

### With Conda

Create a new environment :

```bash
conda env create -f environment.yaml
```

Activate the environment :

```bash
conda activate data_protection
```

### With pip

```bash
pip install -r requirements.txt
```

## Run streamlit app

Il faut lancer les notebook pour générer les datas clean avant
(clean_network_attacks.ipynb / clean_network_attacks.ipynb)

```bash
streamlit run web/streamlit_app_physical.py
```

```bash
streamlit run web/streamlit_app_network.py
```

## Resources

- Download all the data from [here](https://ieee-dataport.org/open-access/hardware-loop-water-distribution-testbed-wdt-dataset-cyber-physical-security-testing)
