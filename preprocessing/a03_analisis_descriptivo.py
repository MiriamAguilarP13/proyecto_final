import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt
import seaborn as sns
from matplotlib import pyplot as plt
import plotly.express as px

telecom = pd.read_csv('files/datasets/output/dataset_and_clients_us.csv')

# las columnas 'date' y 'date_start' se cambian al tipo de dato de fecha
telecom['date'] = pd.to_datetime(telecom['date'])
telecom['date_start'] = pd.to_datetime(telecom['date_start'])

telecom.dtypes

# se calculan los estadísticos descritptivos con describe()
descriptive_statistics_calls = telecom[['calls_count', 'call_duration', 'total_call_duration', 'waiting_time']].describe()

# se guardan los datos 
descriptive_statistics_calls.to_csv("files/datasets/output/descriptive_statistics_calls.csv", index=False)

# se grafica un histograma para el número de llamadas
fig1 = px.histogram(telecom, 
                    x="calls_count",
                    title="Distribución del número de llamadas",
                    nbins= 80
                    )
fig1.show()

# se guarda la figura fig1 con el método write_image() de Plotly
fig1.write_image("analysis/charts/a03_fig1.png")


# se grafica un histograma para la Duración de las llamadas
fig2 = px.histogram(telecom, 
                    x="call_duration",
                    title="Distribución de la Duración de las Llamadas",
                    nbins= 80
                    )
fig2.show()

# se guarda la figura fig2 con el método write_image() de Plotly
fig2.write_image("analysis/charts/a03_fig2.png")

# se grafica un histograma para la Duración total de las Llamadas
fig3 = px.histogram(telecom, 
                    x= "total_call_duration",
                    title="Distribución de la Duración total de las Llamadas",
                    nbins= 80
                    )
fig3.show()

# se guarda la figura fig2 con el método write_image() de Plotly
fig3.write_image("analysis/charts/a03_fig3.png")


# se grafica un histograma para el tiempo en espera
fig4 = px.histogram(telecom, 
                    x= "waiting_time",
                    title="Distribución del Tiempo de Espera",
                    nbins= 80
                    )
fig4.show()

# se guarda la figura fig2 con el método write_image() de Plotly
fig4.write_image("analysis/charts/a03_fig4.png")

# calculo de llamadas entrantes y salientes
total_in_out = telecom.groupby('direction')[['direction']].count()
# se renombra la columna 'direction'
total_in_out = total_in_out.rename(columns= {'direction': 'total_calls'})
total_in_out

plt.figure(figsize=(8, 6))
sns.set_style("ticks")

# se realiza el gráfico con seaborn (sns) a partir del DataFrame 'chain_true'
fig5 = sns.barplot(data= total_in_out, x='direction', y='total_calls', hue= "total_calls", palette='pastel', legend= False)

#bucle para etiquetar cada barra 
for i in fig5.containers:
    fig5.bar_label(i, fontsize=10)


# se le asigan un título y nombres de los ejes al gráfico
fig5.set_title('Total de llamadas entrantes (in) y salientes (out)', fontsize= 14)
fig5.set_xlabel('Dirección de llamadas', fontsize= 12)
fig5.set_ylabel('Número de llamadas', fontsize= 12)

# se guarda la figura fig2 con el método savefig()
plt.savefig('analysis/charts/a03_fig5.png')
plt.show()

# calculo de llamadas perdidas 
missed_calls = telecom.groupby('is_missed_call')[['is_missed_call']].count()
missed_calls = missed_calls.rename(columns= {'is_missed_call': 'num_calls'})
missed_calls

# se realiza el gráfico con seaborn (sns) a partir del DataFrame 'missed_calls'
fig6 = sns.barplot(data= missed_calls, x='is_missed_call', y='num_calls', hue= "num_calls", palette='pastel', legend= False)

#bucle para etiquetar cada barra 
for i in fig6.containers:
    fig6.bar_label(i, fontsize=10)


# se le asigan un título y nombres de los ejes al gráfico
fig6.set_title('Total de llamadas Perdidas (True) y Atendidas (False)', fontsize= 14)
fig6.set_xlabel('Llamadas perdidas', fontsize= 12)
fig6.set_ylabel('Número de llamadas', fontsize= 12)

# se guarda la figura fig2 con el método savefig()
plt.savefig('analysis/charts/a03_fig6.png')
plt.show()

# calculo de proporción de llamadas perdidas
total_calls = missed_calls['num_calls'].sum()

# calculo de proporción de llamadas perdidas
pct_missed_calls = missed_calls.loc[True,'num_calls'] / total_calls * 100

print(f'El porcentaje de llamadas perdidas es de {round(pct_missed_calls, 1)} %')


