# **Proyecto individual N° 1:**
# MLOps : Sistema de Recomendación de Películas

<div align="center">
  <img src="image.png" alt="MLOps en Sistema de Recomendación de Películas" width="600">
</div>


Este proyecto consiste en la creación de un sistema de recomendación de películas utilizando Machine Learning y técnicas de procesamiento de datos. El proyecto se centra en la manipulación y análisis de dos conjuntos de datos (`movies_dataset.csv` y `credits.csv`), así como en el desarrollo de una API utilizando FastAPI para disponibilizar consultas relacionadas con las películas.

## Estructura del Proyecto

El proyecto se divide en las siguientes etapas principales:

### 1. Procesamiento de Datos

Se realizaron los siguientes Minimum Viable Products (MVP):

1. **Desanidamiento de Campos**: 
   - Algunos campos como `belongs_to_collection`, `production_companies`, y otros (ver diccionario de datos) están anidados, es decir, contienen un diccionario o una lista como valores en cada fila. Se desanidaron estos campos para poder unirlos al dataset y facilitar futuras consultas a la API. Alternativamente, se exploraron métodos para acceder a estos datos sin desanidarlos.

2. **Relleno de Valores Nulos en Campos Numéricos**:
   - Los valores nulos de los campos `revenue` y `budget` fueron reemplazados por el número 0.

3. **Eliminación de Filas con Fechas Nulas**:
   - Los valores nulos en el campo `release_date` fueron eliminados para mantener la consistencia en el análisis temporal.

4. **Formateo de Fechas**:
   - Las fechas presentes en el dataset fueron formateadas al formato `AAAA-mm-dd`.
   - Se creó la columna `release_year`, que contiene el año extraído del campo `release_date`.

5. **Cálculo del Retorno de Inversión**:
   - Se creó una columna llamada `return` que representa el retorno de inversión calculado como `revenue / budget`. En los casos donde no se disponía de datos suficientes para el cálculo, se asignó el valor 0.

6. **Eliminación de Columnas Irrelevantes**:
   - Se eliminaron las columnas `video`, `imdb_id`, `adult`, `original_title`, `poster_path`, y `homepage` por no ser utilizadas en el análisis.

### 2. Desarrollo de la API

Se desarrolló una API utilizando el framework FastAPI para disponibilizar los datos procesados y permitir consultas específicas. Las siguientes funcionalidades fueron implementadas:

1. **cantidad_filmaciones_mes**:
   - Devuelve la cantidad de películas que fueron estrenadas en un mes específico.

2. **cantidad_filmaciones_dia**:
   - Devuelve la cantidad de películas que fueron estrenadas en un día específico.

3. **score_titulo**:
   - Proporciona el título, el año de estreno y el score de una película específica.

4. **votos_titulo**:
   - Devuelve el título, la cantidad de votos y el valor promedio de las votaciones para una película específica. Si la película no cuenta con al menos 2000 valoraciones, se muestra un mensaje indicando que no cumple esta condición.

5. **get_actor**:
   - Retorna el éxito de un actor medido a través del retorno de inversión, la cantidad de películas en las que ha participado y el promedio de retorno. No se consideran los directores en esta función.

6. **get_director**:
   - Devuelve información similar a `get_actor`, pero enfocada en los directores de películas.

7. **recomendacion**:
   - Proporciona una lista de 5 películas similares a una película dada, basada en la relación de vecindad entre películas en el dataset.

### 3. Despliegue del Proyecto en Render

El proyecto se ha desplegado utilizando [Render](https://render.com/), una plataforma de alojamiento en la nube que permite implementar aplicaciones de manera sencilla. A continuación se detallan los pasos para desplegar el proyecto desde un repositorio en GitHub:

1. **Crear una cuenta en Render**:
   - Si no tienes una cuenta en Render, puedes registrarte en [Render](https://render.com/).

2. **Conectar tu cuenta de GitHub con Render**:
   - Una vez que hayas iniciado sesión en Render, conecta tu cuenta de GitHub para que Render pueda acceder a tus repositorios.

3. **Crear un Nuevo Servicio**:
   - Selecciona la opción "New +" y elige "Web Service" para desplegar una aplicación web.
   - Selecciona el repositorio que contiene tu proyecto desde la lista de repositorios en GitHub.

4. **Configurar el Entorno**:
   - Define la rama del repositorio que deseas desplegar (por ejemplo, `main`).
   - Selecciona la versión de Python adecuada para tu proyecto, que en este caso es Python 3.9.
   - Configura los comandos de inicio para la aplicación. Por ejemplo, para ejecutar la API de FastAPI con Uvicorn, podrías usar:
     ```bash
     uvicorn main:app --host 0.0.0.0 --port 10000
     ```

5. **Configurar Variables de Entorno**:
   - Si tu proyecto requiere variables de entorno (por ejemplo, claves API o configuraciones de base de datos), agrégalas en la sección "Environment".

6. **Desplegar el Proyecto**:
   - Una vez configurado, Render comenzará a desplegar tu aplicación. El proceso puede tomar unos minutos.
   - Una vez que el despliegue esté completo, Render te proporcionará una URL donde estará disponible tu aplicación.


## Cómo Ejecutar el Proyecto

### Requisitos

- Python 3.9
- FastAPI
- Pandas
- Uvicorn (para ejecutar la API)
- Otros paquetes listados en `requirements.txt`

### Instalación

1. Enlaces Resumen

- Api: [Despliegue en Render](https://mlops-recomendacion-de-peliculas-14.onrender.com).
- Clonar repositorio:
   ```bash
   git clone https://github.com/GonzaloHC/MLOps_Recomendacion_de_Peliculas.git
