import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import plotly.express as px

# se cargan los datos
telecom = pd.read_csv('files/datasets/output/dataset_and_clients_us.csv')

# Relación entre la tasa de llamadas internas y la duración de las llamadas <a id='corr'></a> 

# se contabilizan las llamadas internas y externas
total_internal_external = telecom.groupby('internal')[['internal']].count()
# se renombra la columna 'direction'
total_internal_external = total_internal_external.rename(columns= {'internal': 'total_calls'})

# se reinicia el índice
total_internal_external.reset_index(inplace= True)
total_internal_external

# se realiza el gráfico con seaborn (sns) a partir del DataFrame 'chain_true'
fig10 = sns.barplot(data= total_internal_external,
                    x='internal',
                    y='total_calls',
                    hue= "total_calls",
                    palette='pastel',
                    legend= False
                    )

#bucle para etiquetar cada barra 
for i in fig10.containers:
    fig10.bar_label(i, fontsize=10)


# se le asigan un título y nombres de los ejes al gráfico
fig10.set_title('Total de llamadas internas (True) y y externas (False)', fontsize= 14)
fig10.set_xlabel('Llamada fue interna', fontsize= 12)
fig10.set_ylabel('Número de llamadas', fontsize= 12)
# se guarda la figura fig10 con el método savefig()
plt.savefig('analysis/charts/a05_fig10.png')
plt.show()

# se filtran las  llamadas internas y se cuentan por operador
internal_calls_per_operator = telecom[telecom['internal'] == True].groupby('operator_id')[['calls_count']].sum()

# se renombra la columna 
internal_calls_per_operator = internal_calls_per_operator.rename(columns= {'calls_count': 'total_calls_internal'})

# se reinicia el índice
internal_calls_per_operator.reset_index(inplace= True)

internal_calls_per_operator.head()

# se calculan el total de llamadas por operador 
total_calls_op = telecom.groupby('operator_id')[['calls_count']].sum()

# se reinicia el índice
total_calls_op.reset_index(inplace= True)

# se renobra la columna
total_calls_op = total_calls_op.rename(columns= {'calls_count': 'calls_total'})
total_calls_op.head()

# el DataFrame 'total_calls_op' tiene las llamadas por operador
# se unen los DataFrame 'total_calls_op' y 'internal_calls_per_operator'
inter_calls_per_operator = total_calls_op.merge(internal_calls_per_operator, on= 'operator_id', how= 'outer')
inter_calls_per_operator.head()

# los valores nulos se sustituyen con 0
inter_calls_per_operator.fillna(0, inplace= True)

# %%
# se calculan la tasa de llamadas internas por operador (expresada en porcentaje)
inter_calls_per_operator['pct_calls_internal'] = inter_calls_per_operator['total_calls_internal'] / inter_calls_per_operator['calls_total'] * 100

inter_calls_per_operator.head()

# se calcula la duración promedio de la llamada por operador
avg_call_duration_per_operator = telecom.groupby('operator_id')[['call_duration']].mean()

# se renombra la columna 
avg_call_duration_per_operator = avg_call_duration_per_operator.rename(columns= {'call_duration': 'avg_call_duration'})

# se reinicia el índice
avg_call_duration_per_operator.reset_index(inplace= True)

avg_call_duration_per_operator.head()


# se crea un gráfico de dispersión para visualizar la relación
fig11 = px.scatter(x= inter_calls_per_operator['pct_calls_internal'], 
                 y= avg_call_duration_per_operator['avg_call_duration'],
                 labels={
                     'x': "Tasa de llamadas internas por operador",
                     'y': "Duración promedio de la llamada por operador"
                 },
                 title="Relación entre la tasa de llamadas internas y la duración promedio de la llamada"
                 )
fig11.show()

# se guarda la figura fig8 con el método write_image() de Plotly
fig11.write_image("analysis/charts/a05_fig11.png")

# calculo del coeficiente de correlación
corr_internal_duration = inter_calls_per_operator['pct_calls_internal'].corr(avg_call_duration_per_operator['avg_call_duration'])
print(corr_internal_duration)

# ==================================================================================================
# Duración de las llamadas de acuerdo al plan tarifario 

# se calcula el promedio de la duración total de las llamadas
plan_mean_dur_calls = telecom.groupby('tariff_plan')[['total_call_duration']].mean()

# se renombran las columnas
plan_mean_dur_calls = plan_mean_dur_calls.rename(columns= {'total_call_duration': 'avg_total_call_duration'})

# se reinicia el índice
plan_mean_dur_calls.reset_index(inplace= True)
plan_mean_dur_calls.head()

# se realiza el gráfico con seaborn (sns) a partir del DataFrame 'plan_mean_dur_calls'
fig12 = sns.barplot(data= plan_mean_dur_calls,
                    x='tariff_plan',
                    y='avg_total_call_duration',
                    hue= "avg_total_call_duration",
                    palette='pastel',
                    legend= False
                    )

#bucle para etiquetar cada barra 
for i in fig12.containers:
    fig12.bar_label(i, fontsize=10)


# se le asigan un título y nombres de los ejes al gráfico
fig12.set_title('Duración total promedio de las llamadas', fontsize= 14)
fig12.set_xlabel('Plan Tarifario', fontsize= 12)
fig12.set_ylabel('Duración total promedio', fontsize= 12)

# se guarda la figura fig12 con el método savefig()
plt.savefig('analysis/charts/a05_fig12.png')
plt.show()

