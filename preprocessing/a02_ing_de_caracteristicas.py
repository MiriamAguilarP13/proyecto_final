import pandas as pd

dataset_us = pd.read_csv('files\datasets\intermediate\dataset_us_cleaned.csv')
clients_us = pd.read_csv('files\datasets\intermediate\clients_us_cleaned.csv')

# información de DataFrames
dataset_us.info()
clients_us.info()

# las columnas que tienen fechas se pasan a sus tipo de dato de fecha
dataset_us['date'] = pd.to_datetime(dataset_us['date'])
clients_us['date_start'] = pd.to_datetime(clients_us['date_start'])

# se crea una columna para calcular el tiempo en espera para cada operador
dataset_us['waiting_time'] = dataset_us['total_call_duration'] - dataset_us['call_duration']

# se unen ambos DataFrames con merge()
dataset_clients_merged = dataset_us.merge(clients_us, on= 'user_id')

# se muestra la información del nuevo DataFrame
dataset_clients_merged.info()

# se guardan los datos 
dataset_clients_merged.to_csv("files/datasets/output/dataset_and_clients_us.csv", index=False)