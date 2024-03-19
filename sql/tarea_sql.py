# Tarea SQL
# 
# El coronavirus tomó al mundo entero por sorpresa, cambiando la rutina diaria de todos y todas. 
# Los habitantes de las ciudades ya no pasaban su tiempo libre fuera, yendo a cafés y centros comerciales;
# sino que más gente se quedaba en casa, leyendo libros. Eso atrajo la atención de las startups (empresas emergentes)
#que se apresuraron a desarrollar nuevas aplicaciones para los amantes de los libros.  

# Te han dado una base de datos de uno de los servicios que compiten en este mercado.
#Contiene datos sobre libros, editoriales, autores y calificaciones de clientes y reseñas de libros.
# Esta información se utilizará para generar una propuesta de valor para un nuevo producto.

# # Objetivo
# 
# Analizar la base de datos para comprender el mercado de los amantes de los libros y crear un producto o 
# servicio que sea destacable al plantear las necesidades y preferencias identificadas a partir de los 
# datos recopilados.

# importar librerías
import pandas as pd
from sqlalchemy import create_engine, inspect
import os
import psycopg2
from dotenv import load_dotenv
load_dotenv()

# importar librerías

db_config = {'user': os.getenv('tripleten_sql_user'),         # nombre de usuario
             'pwd': os.getenv('tripleten_sql_pwd'), # contraseña
             'host': os.getenv('tripleten_sql_host'),
             'port': 6432,              # puerto de conexión
             'db': os.getenv('tripleten_sql_db')}           # nombre de la base de datos

connection_string = f"postgresql://{db_config['user']}:{db_config['pwd']}@{db_config['host']}:{db_config['port']}/{db_config['db']}"

engine = create_engine(connection_string, connect_args={'sslmode':'require'})

# función para ejecutar una consulta SQL utilizando pandas
def query_pandas(query):
    df= pd.io.sql.read_sql(query, con = engine)

    return df

# tabla books
query = '''SELECT * 
           FROM 
           public.books
           LIMIT 5
           '''

# primeras 5 filas de tabla books
query_pandas(query)

# tabla authors
query = '''SELECT * 
           FROM 
           public.authors
           LIMIT 5
           '''

# primeras 5 filas de tabla 
query_pandas(query)

# tabla publishers
query = '''SELECT * 
           FROM 
           public.publishers
           LIMIT 5
           '''

# primeras 5 filas de tabla 
query_pandas(query)

# tabla ratings
query = '''SELECT * 
           FROM 
           public.ratings
           LIMIT 5
           '''

# primeras 5 filas de tabla 
query_pandas(query)

# tabla reviews
query = '''SELECT * 
           FROM 
           public.reviews
           LIMIT 5
           '''

# primeras 5 filas de tabla 
query_pandas(query)

# Número de libros publicados después del 1 de enero de 2000.

# query
query = '''SELECT 
               COUNT(title) AS total_libros
           FROM 
                public.books
           WHERE publication_date > '2000-01-01'
           '''

# primeras 5 filas de tabla 
libros_totales= query_pandas(query)
libros_totales

# Número de reseñas de usuarios y la calificación promedio para cada libro

# tabla reviews
query = '''SELECT 
               bk.book_id,
               bk.title,
               COUNT(r.review_id) AS num_reviews,
               AVG(rt.rating) AS avg_rating
           FROM 
                public.books AS bk
            INNER JOIN
                public.reviews AS r ON bk.book_id = r.book_id
            INNER JOIN 
                public.ratings AS rt ON bk.book_id = rt.book_id
           GROUP BY 
                bk.book_id,
                bk.title
            ORDER BY
                num_reviews DESC
           '''

# primeras 5 filas de tabla 
reviews_ratings_books = query_pandas(query)
reviews_ratings_books.head()

# Identifica la editorial que ha publicado el mayor número de libros con más de 50 páginas (esto te ayudará a excluir folletos y publicaciones similares de tu análisis)

query = '''SELECT 
               p.publisher_id,
               p.publisher,
               COUNT(bk.book_id) AS total_books
           FROM 
                public.books AS bk
            INNER JOIN
                public.publishers AS p ON bk.publisher_id = p.publisher_id
           WHERE
               bk.num_pages > 50
           GROUP BY 
               p.publisher_id,
               p.publisher
            ORDER BY
                total_books DESC
           '''

# primeras 5 filas de tabla 
publishers_books_50_pages = query_pandas(query)
publishers_books_50_pages.head()

# Identificación del autor que tiene la más alta calificación promedio del libro: mira solo los libros con al menos 50 calificaciones

query = '''SELECT
               a.author_id,
               a.author,
               AVG(rt.rating) AS avg_rating
           FROM 
                public.books AS bk
            INNER JOIN
                public.authors AS a ON bk.author_id = a.author_id
            INNER JOIN
                public.ratings AS rt ON bk.book_id = rt.book_id
           GROUP BY
               a.author_id, 
               a.author
            HAVING
               COUNT(rt.rating_id) >= 50
            ORDER BY
                avg_rating DESC
           '''

# primeras 5 filas de tabla 
authors_ratings = query_pandas(query)
authors_ratings.head()

# Encuentra el número promedio de reseñas de texto entre los usuarios que calificaron más de 50 libros

query = ''' 
SELECT 
    AVG(num_reviews) AS avg_text_reviews_per_user
FROM (
    SELECT 
        username, 
        COUNT(text) AS num_reviews
    FROM 
        public.reviews
    WHERE 
        username IN (
            SELECT 
                username
            FROM 
                public.ratings
            GROUP BY 
                username
            HAVING 
                COUNT(rating_id) > 50
                )
GROUP BY username
    ) AS avg_reviews_per_user
        ''' 

# primeras 5 filas de tabla 
users_reviews_mean = query_pandas(query)
users_reviews_mean.head()


#  Conclusiones
    
# Después del 01 de enero del 2000 se publicaron un total de 819 libros.  
# 
# El top 5 de losl libros con más reseñas son: Twilight #1, The Hobbit or There and Back Again, The Catcher in the Rye, Harry Potter and the Prisoner of Azkaban y Harry Potter and the Chamber of Secrets. Twilight #1(1120), tuvo muchas reseñas, pero el rpomedio de las calificaciones fue de 3.7, mientras que, Harry Potter and the Prisoner of Azkaban tuvo menos reseñas (492), pero su calificación fue la más alta, 4.4.  
# 
# El top 5 de las editoriales que publicaron libros con más de 50 páginas fueron: Penguin Books, Vintage, Grand Central Publishing, Penguin Classics y Ballantine Books.     
# 
# Los 5 autores con las mayores calificaciones de sus libros fueron: Diana Gabaldon, J.K. Rowling/Mary GrandPré, Agatha Christie, Markus Zusak/Cao Xuân Việt Khương y J.R.R. Tolkien.  
# 
# Los usuarios y usuarias que calificaron más de 50 libros, en promedio hicieron 166.7 reseñas de texto.  



