# Prueba A/B

# # Objetivo
# 
# El objetivo  de la prueba A/B `recommender_system_test` es determinar el impacto de un nuevo embudo de pago introducido en la tienda en línea internacional. Dicho embudo está diseñado para mejorar el sistema de recomendaciones, por lo tanto, se espera que influya de forma positiva en el comportamiento de los usuarios.

# # Procesamiento de Datos

 # se importan las librerias
import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt
import plotly.express as px
from plotly import graph_objects as go





 # se cargan los datasets
project_marketing_events_us = pd.read_csv('files/datasets/test_AB/ab_project_marketing_events_us.csv', parse_dates= ['start_dt', 'finish_dt'])
new_users_upd_us = pd.read_csv('files/datasets/test_AB/final_ab_new_users_upd_us.csv', parse_dates= ['first_date'])
events_upd_us = pd.read_csv('files/datasets/test_AB/final_ab_events_upd_us.csv', parse_dates= ['event_dt'])
participants_upd_us = pd.read_csv('files/datasets/test_AB/final_ab_participants_upd_us.csv')

project_marketing_events_us.head()

new_users_upd_us.head()

events_upd_us.head()

participants_upd_us.head()

project_marketing_events_us.info()

new_users_upd_us.info()

events_upd_us.info()

participants_upd_us.info()

  
# Los tipos de datos estan bien solo en el DataFrame `events_upd_us` se cambia el tipo de dato 
# de la columna `details` a float y el dombre de la columna a usd, ya que es el pedido total en USD
#para los eventos purchase.


 # se cambia el tipo de dato
events_upd_us['details'] = pd.to_numeric(events_upd_us['details'], errors= 'coerce')


 # se cambia el nombre de la columna details -> a usd
events_upd_us = events_upd_us.rename(columns= {'details': 'usd'})
# se muestra el tipo de dato para el DataFrame
events_upd_us.dtypes

events_upd_us.isna().sum()

    
# Sólo se tienen valores nulos en el DataFrame `events_upd_us` en la columna `usd`, que es el
# pedido total en USD para los eventos purchase, por tanto, los valores nulos se dejarán en el DataFrame.

 # se unen los DataFrame 'new_users_upd_us' y 'events_upd_us'
merged_data= new_users_upd_us.merge(events_upd_us, on='user_id')


 # Combinar el resultado anterior con 'participants_upd_us' con base en user_id
merged_data= merged_data.merge(participants_upd_us, on='user_id')

merged_data.info()

 # # Análisis Exploratorio de Datos

 # se buscan los eventos que hay en los registros
# con value_counts() que hace recuentos de valores únicos
merged_data['event_name'].value_counts()

 # se contabilizan los usuarios únicos que hay en los regitros con nunique()
total_users= merged_data['user_id'].nunique()

# se calculan los usuarios 
total_users
   
# **Observaciones:**  
# Se tienen 4 diferentes tipos de eventos y cada uno tiene diferentes recuentos de valores únicos y 
# se tienen un total de 13638 en los registros. 


# se calculan el promedio de eventos por usuario/a a partir del DataFrame 'merged_data'
# se contabilizan los eventos con count() y con mean() se calcula el promedio
# el resultado se guarda en 'average_events_per_user'
average_events_per_user = merged_data.groupby('user_id')['event_name'].count().mean() 

# se calcula la mediana de los eventos por usuario/a a partir del DataFrame 'logs_exp_us'
median_events_per_user = merged_data.groupby('user_id')['event_name'].count().median()

print(f'Promedio de eventos por usuario: {round(average_events_per_user)}')
print(f'La mediana de eventos por usuario: {round(median_events_per_user)}')

 # se encuentra la fecha mínima y máxima del evento en los datos
date_min = merged_data['event_dt'].min()
date_max = merged_data['event_dt'].max()

print(f'La fecha mínima es el {date_min}\nLa fecha máxima es el {date_max}')

# se buscan los eventos que hay en los registros y su frecuencia de suceso, se realiza con value_counts()
# se reincia el índice
event_frequencies = merged_data['event_name'].value_counts().reset_index()
# se cambia el nombre de las columnas 
event_frequencies.columns = ['event_name', 'frequency']

# se imprime el DataFrame 'event_frequencies'
event_frequencies

# se encuentra la cantidad de usuarios y usuarias que realizaron cada una de las acciones (los eventos)
# se emplea nunique() para contbilizar los usuarios/as únicos/as, reset_index() para reiniciar el índice y 
# sort_values() para ordenar los valores de mayor a menor
users_event = merged_data.groupby('event_name')['user_id'].nunique().reset_index()

# se cambia el nombre de las columnas 
users_event.columns = ['event_name', 'num_users']

# se ordena por la columna 'users' de mayor a menor
users_event = users_event.sort_values(by= 'num_users', ascending= False)

# se imprime el DataFrame 'users_per_event'
users_event

# se calcula la proporción de usuarios y usuarias que realizaron la acción al menos una vez
# se crea la columna 'proportion' en el DataFrame 'users_event'
# se divide la columna 'users' entre el total de usuarios que es la variable 'total_users'
users_event['proportion'] = users_event['num_users'] / total_users

# se reinicia el índice
users_event = users_event.reset_index(drop= True)
# se imprime el DataFrame 'users_event'
users_event

 # se realiza un gráfico de embudo con plotly.graph_objects
fig1 = go.Figure(go.Funnel(
    y = users_event['event_name'],
    x = users_event['num_users']))

fig1.show()

# **Observaciones:**  
# Para hacer el gráfico de embudo el orden de los eventos parece ser como si no fueran parte de una
# secuencia. El evento de product_cart es dónde se pierden más usuarios y usuarias, mientras que, el
# porcentaje de usuarios y usuarias que hace todo el viaje desde su primer evento hasta el pago (purchase) son el 33.5%.  


# # Comparación de grupos

# se calcula la cantidad de usuarios y usuarias que tengan los tres grupos experimentales
merged_data.groupby('group')['user_id'].nunique()
    
# **Observaciones:**  
# El grupo A tiene más usurios y usuarias que el grupo B, con 7874 y 6205, respectivamente.    


 # se filtra el DataFrame 'merged_data' para los grupos A y B
group_a = merged_data[merged_data['group'] == 'A']
group_b = merged_data[merged_data['group'] == 'B']

 # se guardan los user_id únicos del grupo a y b
user_id_gpo_a = group_a['user_id'].unique()

user_id_gpo_b = group_b['user_id'].unique()

 # se buscan los usuarios que están presentes en ambas muestras
# Encontrar la intersección utilizando isin() 
common_users_ab= np.intersect1d(user_id_gpo_a, user_id_gpo_b)

# Mostrar el resultado y las frecuencias
print('Usuarios en común:', len(common_users_ab))

fig2 = px.histogram(merged_data,
                    x='event_dt',
                    title='Histograma del número de eventos entre los días',
                    labels={'event_dt':'Fecha y Hora del Evento'},
                    opacity=0.8,
                    color_discrete_sequence=['lightseagreen']
                    )
fig2.show()

  
# **Observaciones:**  
# En el histograma se observa que no hay datos para el día 25 de diciembre y para el 30 si hay datos 
# pero son muy escasos. Por tanto se excluirán esos datos de l 30 de diciembre del DataFrame antes de 
# iniciar la prueba A/B.      


 # se filtran los datos para las fechas de la columna 'event_dt' menores al 30 de diciembre
final_df= merged_data[(merged_data['event_dt'] <= '2020-12-29')]
final_df.head()

 # # Prueba A/B

 # se filtra el DataFrame 'final_data' para el experimento 248, que es el grupo con fuentes alteradas
group_a = final_df[final_df['group'] == 'A']
group_b = final_df[final_df['group'] == 'B']

 # se contabilizan la cantidad de eventos por usuario/a en el grupo a
# se hace con groupby() y se cuentan los eventos de la columna 'event_name' con count()
# se reinician los índices
users_events_a = group_a.groupby('user_id')['event_name'].count().reset_index()

# se cambian los nombres de las columnas
users_events_a.columns = ['user_id', 'count_events']

# se imprime las 5 primeras filas
users_events_a.head()

# se contabilizan la cantidad de eventos por usuario/a en el grupo a
# se hace con groupby() y se cuentan los eventos de la columna 'event_name' con count()
# se reinician los índices
users_events_b = group_b.groupby('user_id')['event_name'].count().reset_index()

# se cambian los nombres de las columnas
users_events_b.columns = ['user_id', 'count_events']

# se imprime las 5 primeras filas
users_events_b.head()

 # se compara el grupo control a con el grupo con fuentes alteradas b
# se establece el valor de alpha en 0.05
alpha = 0.05

# Realizar la prueba de Mann-Whitney de las muestras de del grupo a y el grupo b con la  función 'st.mannwhitneyu()'
results_a_b = st.mannwhitneyu(users_events_a['count_events'], users_events_b['count_events'])

print('El valor p es:', results_a_b.pvalue)

if results_a_b.pvalue < alpha:
    print('Se rechaza la hipótesis nula, hay diferencia entre los dos grupos')
else:
    print('No se rechaza la hipótesis nula, no hay diferencia entre los dos grupos')

 
#     
# **Observaciones:**  
# De acuerdo al resultado de la prueba estadística `scipy.stats.mannwhitneyu()`, se rechaza la hipótesis 
# nula, por tanto si hay una diferencia entre los dos grupos a y b. Por lo tanto, si existe una diferencia
# entre el grupo B con el nuevo embudo de pago y el grupo control.  


# # Comprobar la diferencia estadística entre las proporciones

merged_data.head()

# se contabilizan los usuarios únicos que hay en los regitros con nunique()
total_users= final_df['user_id'].nunique()

# se calculan los usuarios 
total_users

# se crea la función proportion()
def proportion(df, event):
    users_events = df[df['event_name'] == event]['user_id'].nunique()
    total_users = df['user_id'].nunique()
    proportion = round(users_events / total_users, 3)
    return proportion

# con un bucle for se calcula la proporción para cada evento en el grupo a

events = ['login', 'product_page', 'purchase', 'product_cart']

for event in events:
    result_proportion = proportion(group_a, event) # se emplea la función proportion()
    print(f'La proporción del evento {event} es: {result_proportion}')

# con un bucle for se calcula la proporción para cada evento en el grupo b
for event in events:
    result_proportion = proportion(group_b, event) # se emplea la función proportion()
    print(f'La proporción del evento {event} es: {result_proportion}')

  
# ****  
# Se comprueba si la diferencia entre las proporciones de los grupos es estadísticamente significativa.


 # se crea una función para calcular la proporción por evento
def proportion_by_event(df_group):
    '''
    Función que calcula la proporción para todos los eventos de interés y retorna una tupla con los resultados.
    '''
    # Lista de los eventos de interés
    events_of_interest = ['login', 'product_page', 'purchase', 'product_cart']
    
    # se crea un diccionario, cada clave del diccionario es un evento de interés, y el valor asociado 
    # es la proporción calculada utilizando la función 'proportion' 
    proportions_dict = {event: proportion(df_group, event) for event in events_of_interest}
    
    # La función retorna una tupla que contiene las proporciones calculadas para cada evento en el 
    # mismo orden en que aparecen en la lista 'events_of_interest'
    return tuple(proportions_dict[event] for event in events_of_interest)

 # Llamada a la función 'proportion_by_event' con el grupo a
p_login_a, p_product_page_a, p_purchase_a, p_product_cart_a= proportion_by_event(group_a)

 # Llamada a la función 'proportion_by_event' con el grupo b
p_login_b, p_product_page_b, p_purchase_b, p_product_cart_b= proportion_by_event(group_b)

 # se crea la función 'proportion_combined'
def proportion_combined(df_group_1, df_group_2):
    '''
    Función que calcula las proporciones combinadas de usuarios que realizaron eventos específicos en dos grupos dados
    '''
    
    events_of_interest = ['login', 'product_page', 'purchase', 'product_cart']

    proportions_combined = {}

    for event in events_of_interest:
        # usuarios/as combinados de ambos grupos por evento
        users_comb_event = df_group_1[df_group_1['event_name'] == event]['user_id'].nunique() + df_group_2[df_group_2['event_name'] == event]['user_id'].nunique()
        # usuarios/as totales de ambos grupos
        total_users_comb = df_group_1['user_id'].nunique() + df_group_2['user_id'].nunique()
        # el resultado se almacena en el diccionario 'proportions_combined'
        proportions_combined[event] = round(users_comb_event / total_users_comb, 3)

    return proportions_combined

 # se llama a la función 'proportion_combined' con los grupos a y b
proportions_combined = proportion_combined(group_a, group_b)

 # se imprimen los valores de las propociones comibinadas con un bucle for
for key, value in proportions_combined.items():
    print(f'{key}: {value}')

 # se guardan las proporciones combinadas de cada evento en una variable diferente
p_login_comb= proportions_combined['login']
p_product_page_comb= proportions_combined['product_page']
p_purchase_comb= proportions_combined['purchase']
p_product_cart_comb= proportions_combined['product_cart']

# se gurdan los valores de las proporciones en una lista
p_list_comb_a_b = [p_login_comb, p_product_page_comb, p_purchase_comb, p_product_cart_comb]
p_list_comb_a_b

 # se calcula la diferencia entre las proporciones de los dos grupos a y b

difference_login = p_login_a - p_login_b
difference_product_page = p_product_page_a - p_product_page_b
difference_purchase = p_purchase_a - p_purchase_b
difference_product_cart = p_product_cart_a - p_product_cart_b

# se guardan los valores de las diferencias en una lista
diff_list_a_b = [difference_login, difference_product_page, difference_purchase, difference_product_cart]
print(diff_list_a_b)

   
# *******
# Se crea una función para probar la hipótesis de que las proporciones son iguales o no. 

 # se cre una función para calcular el valor p y probar la hipótesis
def test_proportions_difference(difference, p_event_combined, df_group1, df_group2, event, alpha= 0.05): # alpha se establece en 0.05 dentro de la función
    '''
     Función para probar la hipótesis de que las proporciones son iguales o no.
     difference: la diferencia entre las proporciones de los datasets
     p_event_combined: proporción de éxito en los dataset unidos
     df_group1: dataset de interés 1
     df_group2: dataset de interés 2
     event: evento/acción de interés
     alpha: valor de alfa para la prueba
    '''
    
    # se calcula la estadística en desviaciones estándar de la distribución normal estándar
    z_value = difference / mt.sqrt(p_event_combined * (1 - p_event_combined) * (1/df_group1[df_group1['event_name'] == event]['user_id'].nunique() + 1/df_group2[df_group2['event_name'] == event]['user_id'].nunique()))
    
    # se establece la distribución normal estándar (media 0, desviación estándar 1)
    distr = st.norm(0, 1)
    
    p_value = (1 - distr.cdf(abs(z_value))) * 2
    
    #result = {'p_value': p_value, 'reject_null': p_value < alpha}
    
    return p_value

 # se crea un diccionario combinando las listas 'diff_list_a_b' y 'p_list_comb_a_b' utilizando zip()
# se emplea list() para conevertir el resultado de zip en una lista. 
# Cada elemento de la lista es una tupla que contiene un elemento de diff_list_a_b y un elemento correspondiente de p_list_comb_a_b

results_diff_comb = list(zip(diff_list_a_b, p_list_comb_a_b))
print(results_diff_comb)


# *******
# La variable `results_diff_comb` es una lista que contiene pares de valores (como tuplas), cada uno de los pares de valores corresponde a uno de los eventos en el siguiente orden: 'login', 'product_page', 'purchase', 'product_cart'. Para guardar y asignar cada uno de estos pares de valores a su correspondiente evento/acción se hará creando un diccionario, donde las claves del diccionario serán los nombres de los eventos.  


 # se crea el diccionario vacio
dict_events_diff_comb = {}

# se crea un diccionario de mapeo evento a índice
events_index_map = {
    'login': 0,
    'product_page': 1,
    'purchase': 2,
    'product_cart': 3
}

# se usa el diccionario de mapeo para asignar los valores de 'results_diff_comb' a cada evento
for event in events:
    dict_events_diff_comb[event] = results_diff_comb[events_index_map[event]]

print(dict_events_diff_comb)

#     
# *******
# Ya se tienen la lista de los eventos de interés y el diccionario con los resultados de cada evento, ahora se llama a la función `test_proportions_difference` para hacer la prueba y determinar si hay o no diferencias entre las proporciones.   


 # se establece el valor de alpha
alpha= 0.05

events = ['product_page', 'purchase', 'product_cart']

# con un bucle for se recorre la lista de los eventos de interés
for event in events:
    
    # se almacena el resultado de la prueba en results
    results = test_proportions_difference(dict_events_diff_comb[event][0], dict_events_diff_comb[event][1], group_a, group_b, event, alpha)
    
    print(f'Resultados de la prueba para el evento: {event}')        
    print('p-value: ', results)

    if results < alpha:
        print("Rechazar la hipótesis nula: hay una diferencia significativa entre las proporciones")
    else:
        print("No se pudo rechazar la hipótesis nula: no hay razón para pensar que las proporciones son diferentes")
    print()

# **Observaciones:**  
# Con base en los resultados de la prueba en ninguno de los eventos no hay una diferencia en las proporciones. Por lo tanto, se puede decir que los grupos se dividieron correctamente.  


 # # Conclusión General
 
#     
# La columna details en el DataFrame events_upd_us se cambió al tipo de dato float y se renombró a usd, ya que representa el pedido total en USD para los eventos de compra (purchase). Había valores nulos en la columna `usd`, y se decidió mantener estos valores nulos en el DataFrame.
# 
# El evento product_cart es donde se pierden la mayoría de los usuarios y sólo el 33.5% de los usuarios completa todo el proceso desde el primer evento hasta la compra (purchase).  
# 
# El grupo A tiene más usuarios que el grupo B, con 7,874 y 6,205 usuarios respectivamente.  
# 
# No hay datos para el 25 de diciembre y los datos para el 30 de diciembre son escasos.  
# 
# De acuerdo con los resultados de la prueba estadística `scipy.stats.mannwhitneyu()`, se rechaza la hipótesis nula.
# Existe una diferencia estadísticamente significativa entre el grupo A y el el grupo B, este último tiene el nuevo embudo de pago.  
# 
# Con base en los resultados de la prueba, no hay diferencias significativas en las proporciones de eventos entre los dos grupos A y B. Los grupos se dividieron correctamente.  



