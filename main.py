import os
import pandas as pd
from fastapi import FastAPI

# cargamos los datos
data_mvp_funciones = pd.read_csv(
    os.path.join("Output", "data_mvp_final_funciones.csv"),
    index_col=0,
).convert_dtypes()
data_mvp_funciones_final = pd.read_csv(
    os.path.join("Output", "data_mvp_final_ml.csv"),
    index_col=0,
).convert_dtypes()
data_mvp_actor = pd.read_csv(
    os.path.join("Pipeline", "credits_normalizada.csv"),
    index_col=0,
).convert_dtypes()
data_mvp_director = pd.read_csv(
    os.path.join("Output", "data_mvp_final_funciones_exitodir.csv"),
    index_col=0,
).convert_dtypes()
data_mvp_recomendacion = pd.read_csv(
    os.path.join("Output", "data_mvp_ml_recomend_indexed.csv"),
    index_col=[0, 1],
).convert_dtypes()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "API del proyecto: Henry PI_MLOPS, por GonzaloH"}

@app.get("/cantidad_filmaciones_mes/{mes}")
# definimos
def cantidad_filmaciones_mes(mes: str):
    # Crear un diccionario para convertir los meses en español a números
    meses = {
        'enero': 1, 'febrero': 2, 'marzo': 3, 'abril': 4,
        'mayo': 5, 'junio': 6, 'julio': 7, 'agosto': 8,
        'septiembre': 9, 'octubre': 10, 'noviembre': 11, 'diciembre': 12
    }
    
    # Convertir el mes a minúsculas para asegurar la coincidencia
    mes = mes.lower()
    
    if mes not in meses:
        raise ValueError("Mes inválido. Por favor ingrese un mes válido en español.")
    
    # Obtener el número correspondiente al mes
    mes_numero = meses[mes]
    
    # Convertir la columna de fechas a datetime si no lo está ya
    data_mvp_funciones ['release_date'] = pd.to_datetime(data_mvp_funciones['release_date'], errors='coerce')
    
    # Filtrar el DataFrame por el mes
    peliculas_mes = data_mvp_funciones[data_mvp_funciones['release_date'].dt.month == mes_numero]
    
    # Devolver la cantidad de filmaciones en ese mes
    return f"{len(peliculas_mes)} cantidad de peliculas fueron estrenadas en el mes de {mes}"


@app.get("/cantidad_filmaciones_dia/{dia}")
# definimos
def cantidad_filmaciones_dia(dia: str):
    # Crear un diccionario para convertir los días de la semana en español a números
    dias_semana = {
        'lunes': 0, 'martes': 1, 'miércoles': 2, 'jueves': 3,
        'viernes': 4, 'sábado': 5, 'domingo': 6
    }
    
    # Convertir el día a minúsculas para asegurar la coincidencia
    dia = dia.lower()
    
    if dia not in dias_semana:
        raise ValueError("Día inválido. Por favor ingrese un día válido en español.")
    
    # Obtener el número correspondiente al día
    dia_numero = dias_semana[dia]
    
    # Convertir la columna de fechas a datetime si no lo está ya
    data_mvp_funciones['release_date'] = pd.to_datetime(data_mvp_funciones['release_date'], errors='coerce')
    
    # Filtrar el DataFrame por el día de la semana
    peliculas_dia = data_mvp_funciones[data_mvp_funciones['release_date'].dt.dayofweek == dia_numero]
    
    # Devolver la cantidad de filmaciones en ese día
    return f'{len(peliculas_dia)} cantidad de peliculas fueron estrenadas en los dias {dia}'


@app.get("/score_titulo/{titulo_de_la_filmación}")
# definimos
def score_titulo(titulo_de_la_filmacion: str):
    # Filtrar el DataFrame por el título de la filmación
    filmacion = data_mvp_funciones_final[data_mvp_funciones_final['title'].str.lower() == titulo_de_la_filmacion.lower()]

    if filmacion.empty:
        return "Título no encontrado."

    # Obtener el título, año de estreno y score
    titulo = filmacion['title'].values[0]
    anio_estreno = filmacion['release_year'].values[0]
    score = filmacion['popularity'].values[0]

    return f'La pelicula {titulo} fue estrenado en el año {anio_estreno} con un score/popularidad de {score}'


@app.get("/votos_titulo/{titulo_de_la_filmación}")
# definimos
def votos_titulo(titulo_de_la_filmacion:str):
    # Filtrar el DataFrame por el título de la filmación
    filmacion = data_mvp_funciones_final[data_mvp_funciones_final['title'].str.lower() == titulo_de_la_filmacion.lower()]

    if filmacion.empty:
        return "Título no encontrado."

    # Obtener la cantidad de votos y el valor promedio de las votaciones
    cantidad_votos = filmacion['vote_count'].values[0]
    promedio_votaciones = filmacion['vote_average'].values[0]
    anio_estreno = filmacion['release_year'].values[0]
    titulo_peicula = filmacion['title'].values[0]

    # Verificar si la cantidad de votos es al menos 2000
    if cantidad_votos < 2000:
        return "La filmación no tiene suficientes valoraciones (menos de 2000)."

    return f'La pelicula {titulo_peicula} fue estrenada en el año {anio_estreno}. La misma cuenta con {cantidad_votos} valoraciones, con un promedio {promedio_votaciones}.'


@app.get("/get_actor/{nombre_actor}")
# definimos
def get_actor(nombre_actor:str):
    # Filtrar el DataFrame de cast para obtener las filas donde aparece el actor
    peliculas_con_actor = data_nvp_actor[data_nvp_actor['prtgnst_name'].str.contains(nombre_actor, case=False, na=False)]
    
    if peliculas_con_actor.empty:
        return f"No se encontraron películas para el actor: {nombre_actor}"
    
    # Eliminar duplicados: quedarse con una sola fila por combinación de movie_id y actor
    peliculas_con_actor = peliculas_con_actor.drop_duplicates(subset=['movie_id', 'prtgnst_name'])
    
    # Unir el DataFrame de películas con el DataFrame de cast usando movie_id
    df_actor_movies = peliculas_con_actor.merge(data_mvp_funciones, on='movie_id', how='inner')
    
    # Calcular la cantidad de películas en las que ha participado el actor
    cantidad_peliculas = df_actor_movies.shape[0]
    
    # Calcular el retorno total y el promedio de retorno para las películas en las que ha participado
    retorno_total = df_actor_movies['return'].sum()
    promedio_retorno = df_actor_movies['return'].mean()
    
    return f'El actor {nombre_actor} ha participado en {cantidad_peliculas} cantidad de filmaciones, el mismo a conseguido un retorno de {retorno_total} con un promedio {promedio_retorno} por filmación.'


@app.get("/get_director/{nombre_director}")
# definimos
def get_director(nombre_director: str):
    director_subset = data_mvp_director.loc[
        data_mvp_director['director'].str.contains(nombre_director)]
    director_return = director_subset['director_return'].drop_duplicates()
    director_return_res = round(float(director_return.iloc[0]),2)
    columns_peliculas=['movie_id','title','release_date','budget','revenue','return']
    director_peliculas = director_subset[columns_peliculas].drop_duplicates().fillna(0) ### OJO se colocó fillna(0) para corregir el error de NAType
    peliculas = []
    for _, pelicula in director_peliculas.iterrows():
        pelicula_info = {
            'nombre': pelicula['title'],
            'fecha_lanzamiento': pelicula['release_date'],
            'costo (USD)': ('{:,}'.format(round(pelicula['budget']))),
            'ganancia (USD)': ('{:,}'.format(round(pelicula['revenue']))),
            'retorno (ratio)': round(pelicula['return'],2)
        }
        peliculas.append(pelicula_info)
    return {
        'director': nombre_director,
        'retorno total': director_return_res,
        'peliculas': peliculas }


@app.get("/recomendacion_pelicula/{titulo_pelicula}")
# definimos
def recomendacion_pelicula(titulo_pelicula: str):
    recomendacion_subset = data_mvp_recomendacion.loc[
        data_mvp_recomendacion["title"].isin([titulo_pelicula])
    ]
    pelicula_vecinos = (
        recomendacion_subset[["vecino_title"]].reset_index().drop_duplicates()
    )
    pelicula_recomend = list(pelicula_vecinos["vecino_title"])
    return {"pelicula": titulo_pelicula, "recomendaciones": pelicula_recomend}