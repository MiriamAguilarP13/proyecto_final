import pandas as pd
import numpy as np
from scipy import stats as st
import math as mt

# se cargan los datos
telecom = pd.read_csv('files/datasets/output/dataset_and_clients_us.csv')

# ==============================================================================================
# Hipótesis
# ==============================================================================================
# Impacto de la cantidad de llamadas perdidas y la duración del tiempo de espera
# 
# Ho: No hay diferencia significativa en la duracion de espera de la llamada entre aquellos que tienen llamadas perdidas y aquellos que no las tienen.  
# 
# Ha: Hay una diferencia significativa en la duracion de espera de la llamada entre aquellos que tienen llamadas perdidas y aquellos que no las tienen.
# =============================================================================

telecom.head(3)

# con numpy se calculan los percentiles 90, 95 y 99 del DataFrame 'telecom' para la columna de 'waiting_time'
print(np.percentile(telecom['waiting_time'], [90, 95, 99]))

# se filtra el DataFrame
telecom_95 = telecom[telecom['waiting_time'] <= 1163]
telecom_95.head()

#* Al calcular los percentiles del número de llamadas  se observa que no más del 5 % de la duración de tiempo de espera  duraron más de 1163.
#* Con base a o anterior para las pruebas de hipótesis se filtraran los datos donde la duración total de las llamadas sea menor o igual a 1163.

# se separan los datos en dos grupos: operadores con llamadas perdidas y operadores sin llamadas perdidas
no_missed_calls_operators = telecom_95[telecom_95['is_missed_call'] == 0]
missed_calls_operators = telecom_95[telecom_95['is_missed_call'] == 1]

#* Para determinar el valor del parámetro `equal_var` se hace un test de levene para saber si las varianzas son iguales o diferentes.
#* El valor de alfa será de 5 % (0.05).  
# 
#* La hipótesis nula (H0) en el test de Levene es que todas las poblaciones tienen varianzas iguales.  
#* La hipótesis alternativa (Ha) es que al menos una de las poblaciones tiene una varianza diferente.

# función para la prueba de levene
def test_levene(sample_1, sample_2, alpha= 0.05):
    levene_test = st.levene(sample_1, sample_2)

    p_value = levene_test.pvalue


    if p_value < alpha:
        print('El valor p en el test de levene es:', p_value)
        result= 'Se rechaza la hipótesis nula'
    else:
        result = 'No se rechaza la hipótesis nula'
    
    return print(result)

# función para la prueba de hipótesis con ttest_ind()
def hypothesis_test(sample_1, sample_2, alpha= 0.05, equal_var= True):

    results_score = st.ttest_ind(sample_1, sample_2, equal_var)

    p_value = results_score.pvalue


    if p_value < alpha:
        print('El valor p en el test de levene es:', p_value)
        result= 'Se rechaza la hipótesis nula'
    else:
        result = 'No se rechaza la hipótesis nula'
    
    return print(result)

# se realiza el test de levene para realizar una prueba de igualdad de varianzas entre loa dos grupos
levene_result_hip_1 = test_levene(no_missed_calls_operators['waiting_time'], missed_calls_operators['waiting_time'], alpha= 0.05)

#* De acuerdo al resultado del test de levene se rechaza la hipótesis nula, por lo que las varianzas son diferentes. Entonces el parámetro `equal_var` se deja como `False`.

# Se realiza la prueba las hipótesis
hip_1_result = hypothesis_test(no_missed_calls_operators['waiting_time'], missed_calls_operators['waiting_time'], alpha= 0.05, equal_var= False)

#* De acuerdo al resultado, podemos rechazar la hipósis nula, por lo que si hay una diferencia significativa 
#* en la duración del tiempo de espera entre los operadores que tienen llamadas perdidas y los que no las tienen. El valor de p  es demasiado bajo para concluir que no existe una diferencia significativa entre los operadores que tienen llamdas perdidas y los que no las tienen en el tiempo de espera.

# ==================================================================================================================
# Impacto de los diferentes planes de tarifas en la duración total de las llamadas.  
# 
# Ho: La tarifa del cliente (A, B o C) no afecta significativamente en la duranción de las llamadas. 
# 
# Ha: Hay una diferencia significativa en la duranción de las llamadas entre las tarifa del cliente (A, B o C).

# ==================================================================================================================

# se filtra el DataFrame telecom_95 para cada una de las tarifas
plan_a = telecom_95[telecom_95['tariff_plan'] == 'A']
plan_b = telecom_95[telecom_95['tariff_plan'] == 'B']
plan_c = telecom_95[telecom_95['tariff_plan'] == 'C']

# se realiza el test de levene para realizar una prueba de igualdad de varianzas entre los dos grupos
# entre los dos grupos son los del plan a y b
levene_result_hip_2_ab = test_levene(plan_a['total_call_duration'], plan_b['total_call_duration'], alpha= 0.05)

# se realiza el test de levene para realizar una prueba de igualdad de varianzas entre los dos grupos
# entre los dos grupos son los del plan a y c
levene_result_hip_2_ac = test_levene(plan_a['total_call_duration'], plan_c['total_call_duration'], alpha= 0.05)

# se realiza el test de levene para realizar una prueba de igualdad de varianzas entre los dos grupos
# entre los dos grupos son los del plan a y b
levene_result_hip_2_bc = test_levene(plan_b['total_call_duration'], plan_c['total_call_duration'], alpha= 0.05)

#* De acuerdo a los resultados del test de levene se rechaza la hipótesis nula, por lo que las varianzas
#* son diferentes en los tres casos. Entonces el parámetro `equal_var` se deja como `False`.

# Se realiza la prueba las hipótesis entre los grupos a y b
hip_1_result_ab = hypothesis_test(plan_a['total_call_duration'], plan_b['total_call_duration'], alpha= 0.05, equal_var= False)

# Se realiza la prueba las hipótesis entre los grupos a y c
hip_1_result_ac = hypothesis_test(plan_a['total_call_duration'], plan_c['total_call_duration'], alpha= 0.05, equal_var= False)

# Se realiza la prueba las hipótesis entre los grupos a y b
hip_1_result_bc = hypothesis_test(plan_b['total_call_duration'], plan_c['total_call_duration'], alpha= 0.05, equal_var= False)

#* De acuerdo al resultado, podemos rechazar la hipótesis nula, por lo que si hay una diferencia 
#* significativa en la duración de las llamadas entre los tres planes tarifarios. El valor de p es demasiado bajo para concluir que no existe una diferencia significativa entre estos planes tarifarios.




