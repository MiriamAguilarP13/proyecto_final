import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt
import seaborn as sns
from matplotlib import pyplot as plt

# se guardan los datasets
dataset_us = pd.read_csv('files/datasets/input/telecom_dataset_us.csv')
clients_us = pd.read_csv('files/datasets/input/telecom_clients_us.csv')

# se muestran las primeras filas de ambos datasets 
dataset_us.head()
clients_us.head()

# se muestra la información del DataFrame 'dataset_us'
dataset_us.info()

# se cambian los tipos de datos, para las columnas: date -> formato de fecha e internal -> booleano
dataset_us['date'] = pd.to_datetime(dataset_us['date'])
dataset_us['internal'] = dataset_us['internal'].astype(bool)

# se calculan los valores ausentes
dataset_us.isna().sum()

# la columna operador_id es la única columna con valores ausentes
# Ya que son los id de los operadores los valores ausentes se sustituirán con 'unknown'
dataset_us['operator_id'].fillna('unknown', inplace= True)

# ahora se muestra la información del DataFrame 'clients_us'
clients_us.info()

# son tres columnas en total y se observa que no hay valores ausentes

# se cambia el tipo de dato de la columna date_start a fecha
clients_us['date_start'] = pd.to_datetime(clients_us['date_start'])

# se revisan duplicados en ambos DataFrames
dataset_us.duplicated().sum()
clients_us.duplicated().sum()

# se encuentran valores duplicados en el DataFrame 'dataset_us'
# se eliminan los duplicados explícitos
# con el método drop_duplicates eliminar los duplicados y especificar inplace=True para que se guarden los cambios en df
dataset_us = dataset_us.drop_duplicates().reset_index(drop=True)

# se guardan los datos 
dataset_us.to_csv("files/datasets/intermediate/dataset_us_cleaned.csv", index=False)

clients_us.to_csv("files/datasets/intermediate/clients_us_cleaned.csv", index=False)



