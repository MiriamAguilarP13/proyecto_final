### Descripción de los datasets  

- `ab_project_marketing_events_us.csv`: el calendario de eventos de marketing para 2020  
- `final_ab_new_users_upd_us.csv`: todos los usuarios que se registraron en la tienda en línea desde el 7 hasta el 21 de diciembre de 2020  
- `final_ab_events_upd_us.csv`: todos los eventos de los nuevos usuarios en el período comprendido entre el 7 de diciembre de 2020 y el 1 de enero de 2021  
- `final_ab_participants_upd_us.csv`: tabla con los datos de los participantes de la prueba  

Estructura `ab_project_marketing_events_us.csv`:  

- `name`: el nombre del evento de marketing  
- `regions`: regiones donde se llevará a cabo la campaña publicitaria  
- `start_dt`: fecha de inicio de la campaña  
- `finish_dt`: fecha de finalización de la campaña  

Estructura `final_ab_new_users_upd_us.csv`:  

- `user_id`  
- `first_date`: fecha de inscripción  
- `region`  
- `device`: dispositivo utilizado para la inscripción  

Estructura `final_ab_events_upd_us.csv`:  

- `user_id`  
- `event_dt`: fecha y hora del evento  
- `event_name`: nombre del tipo de evento  
- `details`: datos adicionales sobre el evento (por ejemplo, el pedido total en USD para los eventos `purchase`)  

Estructura `final_ab_participants_upd_us.csv`:  

- `user_id`  
- `ab_test`: nombre de la prueba  
- `group`: el grupo de prueba al que pertenecía el usuario  