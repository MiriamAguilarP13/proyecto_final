# Librerias ---------------------------------------- 

import pandas as pd

# Loading data ---------------------------------------- 

users_behavior = pd.read_csv("files/datasets/intermediate/a01_users_behavior_cleaned.csv")

# Creación del escalador ---------------------------------------- 

# Guardar escalador ---------------------------------------- 

users_behavior.to_csv("files/datasets/intermediate/a02_users_behavior_cleaned.csv")
