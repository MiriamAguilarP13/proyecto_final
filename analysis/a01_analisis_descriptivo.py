import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px

# se cargan los datos
telecom = pd.read_csv('files\datasets\output\dataset_and_clients_us.csv')

# se muestra la información de los datos
telecom.info()

# las columnas que tienen fechas se pasan a sus tipo de dato de fecha
telecom['date'] = pd.to_datetime(telecom['date'])
telecom['date_start'] = pd.to_datetime(telecom['date_start'])

# se emplea el método describe() para calcular los estadísticos descriptivos del DataFrame
telecom.describe()

# 
