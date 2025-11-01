# PCOS Machine Learning Project

## Objetivo
Desarrollar modelos de ML para:
1. Predicción de SOP (Sí/No)
2. Clustering de fenotipos
3. Sistema de severidad

## Dataset
- Archivo: PCOS_data_1.xlsx
- Filas: 541 pacientes
- Columnas: 42 variables
- Target: PCOS (Y/N)

## Setup
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

## Notebooks
1. `01_exploratory_analysis.ipynb` - EDA inicial
2. `02_data_cleaning.ipynb` - Limpieza de datos
3. `03_feature_engineering.ipynb` - Creación de features
4. `04_modeling.ipynb` - Entrenamiento de modelos

## Estado
- [ ] Setup del proyecto
- [ ] EDA completo
- [ ] Limpieza de datos
- [ ] Feature engineering
- [ ] Modelado