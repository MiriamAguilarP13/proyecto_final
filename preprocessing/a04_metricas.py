import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px


# se cargan los datos
telecom = pd.read_csv('files/datasets/output/dataset_and_clients_us.csv')

# Tasa de llamadas perdidas por operador   
# `Tasa de abandono de llamadas = Total de llamadas perdidas / Total de llamadas * 100`

# ahora se filtra el DataFrame 'telecom' para las llamadas que son perdidas del DataFrame
missed_calls = telecom[telecom['is_missed_call'] == True]
missed_calls.head()

# se calculan el total de llamadas por operador 
total_calls_op = telecom.groupby('operator_id')[['calls_count']].sum()

# se reinicia el índice
total_calls_op.reset_index(inplace= True)

# se renobra la columna
total_calls_op = total_calls_op.rename(columns= {'calls_count': 'calls_total'})
total_calls_op.head()

# se agrupan los datos por operador y se calcula las llamdas perdidas 
missed_calls_op = missed_calls.groupby('operator_id').agg({'is_missed_call': 'count'})
# se renombran las columnas
missed_calls_op = missed_calls_op.rename(columns= {'is_missed_call': 'total_missed_calls'})
missed_calls_op.reset_index(inplace= True)

missed_calls_op.head()

# se unen los DataFrames 'total_calls_op' y 'missed_calls_op' con merge() 
op_churn_rate = total_calls_op.merge(missed_calls_op, on= 'operator_id', how= 'outer')
op_churn_rate.head()

# ! 
# TODO: terminar de correr el script restante
# se calculan valores ausente
op_churn_rate.isna().sum()

# %%
# los valores ausentes se siustituyen con 0, ya que esos operadores no tuvieron llamadas perdidas
op_churn_rate.fillna(0, inplace= True)

# %%
# se calcula la tasa de llamadas perdidas por operador
op_churn_rate['pct_missed_calls'] = op_churn_rate['total_missed_calls'] / op_churn_rate['calls_total'] * 100

# se muestran los valores ordenados de mayor a menor porcentaje de abandono de llamadas
op_churn_rate.sort_values(by= 'pct_missed_calls', ascending= False).head()


# %%
# se grafica un histograma para la distribución del porcentaje de llamadas perdidas
fig7 =  px.histogram(op_churn_rate,
                     x="pct_missed_calls",
                     title= 'Distribución del porcentaje de llamadas perdidas para los operadores',
                     nbins= 80
                     )
fig7.show()

# se guarda la figura fig7 con el método write_image() de Plotly
fig7.write_image("analysis/charts/a04_fig7.png")

# Tiempo Medio Operativo (TMO) <a id='tmo'></a>
# Brinda información sobre la duración media de las llamadas o transacciones en un período determinado.
 
# `TMO = Tiempo total de espera hasta ser atendido + Tiempo total de conversación + Tiempo total de tareas después de la llamada / número total de llamadas atendidas`. En el DataFrame `telecom` se tiene la columna `total_call_duration` que tiene la duración de las llamadas incluyendo el tiempo de espera por tanto se empleara para el cálculo del TMO como numerador.

# del DataFrame 'Telecom' se calculan el tiempo total de la duración de las llamadas por operador
tot_call_dur_op = telecom.groupby('operator_id')[['total_call_duration']].sum()

# se reinicia el índice
tot_call_dur_op.reset_index(inplace= True)
tot_call_dur_op.head()

# los DataFrames 'tot_call_dur_op' y 'op_churn_rate' con merge
op_metrics = op_churn_rate.merge(tot_call_dur_op, on= 'operator_id')
op_metrics.head()

# se calcula el tiempo medio operativo, se divide el tiempo total de las llamadas entre el total de las llamadas
op_metrics['tmo'] = op_metrics['total_call_duration'] / op_metrics['calls_total']
op_metrics.head()


# se grafica un histograma para la distribución del tiempo medio operativo (tmo)
fig8 =  px.histogram(op_metrics,
                     x="tmo",
                     title= 'Distribución del tiempo medio operativo (TMO) para los operadores',
                     nbins= 80
                     )
fig8.show()

# se guarda la figura fig8 con el método write_image() de Plotly
fig8.write_image("analysis/charts/a04_fig8.png")

# Tasa del tiempo de espera por operador/a <a id='waiting_time'></a>

# del DataFrame 'telecom' se calculan el tiempo de espera total por operador
tot_wait_time = telecom.groupby('operator_id')[['waiting_time']].sum()
# se reinicia el índice
tot_wait_time.reset_index(inplace= True)
tot_wait_time.head()

# los DataFrames 'op_metrics' y 'tot_wait_time' se unene con merge
op_metrics = op_metrics.merge(tot_wait_time, on= 'operator_id')
op_metrics.head()

# se calcula el porcentaje de tiempo de espera, se divide el tiempo total en espera  entre el total del tiempo de las llamadas
op_metrics['pct_waiting_time'] = op_metrics['waiting_time'] / op_metrics['total_call_duration'] * 100
op_metrics.head()

# se grafica un histograma para la distribución del porcentaje del tiempo de espera
fig9 =  px.histogram(op_metrics,
                     x="pct_waiting_time",
                     title= 'Distribución del porcentaje del tiempo de espera para los operadores',
                     nbins= 80
                     )
fig9.show()

# se guarda la figura fig8 con el método write_image() de Plotly
fig9.write_image("analysis/charts/a04_fig9.png")

# se calculan los estadísticos descritivos para el DataFrame
op_metrics_est = op_metrics.describe()
op_metrics_est

# se guardan los datos 
op_metrics_est.to_csv("files/datasets/output/a04_descriptive_statistics_metrics.csv", index=False)

# TODO:

# se filtra el DataFrame 'op_metrics'
ineffect_op_id_missed_call = op_metrics[op_metrics['pct_missed_calls'] > 5]['operator_id']

# se filtran el DataFrame 'op_metrics' para los valor donde el valor de TMO se mayor a 77
ineffect_op_id_tmo = op_metrics[op_metrics['tmo'] > 77]['operator_id']

# se filtran el DataFrame 'op_metrics' para los valor donde el valor del porcentaje del tiempo de espera sea mayor a 21
ineffect_op_id_wait_time = op_metrics[op_metrics['pct_waiting_time'] > 21]['operator_id']

# se buscan los operadores en comun entre los Series 'ineffect_op_id_missed_call' y 'ineffect_op_id_tmo'
# o los operadores en comun entre los Series 'ineffect_op_id_missed_call' y 'ineffect_op_id_wait_time'
common_values_1 = ineffect_op_id_missed_call[ineffect_op_id_missed_call.isin(ineffect_op_id_tmo) | (ineffect_op_id_missed_call.isin(ineffect_op_id_wait_time))]

# se buscan los operadores en comun entre los Series 'ineffect_op_id_tmo' y 'ineffect_op_id_wait_time'
common_values_2 = ineffect_op_id_tmo[ineffect_op_id_tmo.isin(ineffect_op_id_wait_time)]

# ahora se se buscan los operadores en comun entre los dos Series
common_values_3 = common_values_1[common_values_1.isin(common_values_2)]

print(f'La cantidad de operadores con una menor eficiencia en el porcentaje de llamadas perdidas son: {len(ineffect_op_id_missed_call)}')

print(f'La cantidad de operadores con una menor eficiencia en el tiempo medio de operación son: {len(ineffect_op_id_tmo)}')

print(f'La cantidad de operadores con una menor eficiencia en el tiempo de espera son: {len(ineffect_op_id_wait_time)}')

print(f'La cantidad de operadores con una menor eficiencia en las tres metricas son: {len(common_values_3)}')

