<h1 align="center">
  <br>
  <br>
  Proyecto 2 de Base de Datos 2
  <br>
</h1>
<p align="center">
  <img src="https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white">
  <img src="https://img.shields.io/badge/CLion-black?style=for-the-badge&logo=clion&logoColor=white">
  <img src="https://img.shields.io/badge/NeoVim-%2357A143.svg?&style=for-the-badge&logo=neovim&logoColor=white">
  <img src="https://img.shields.io/badge/CMake-%23008FBA.svg?style=for-the-badge&logo=cmake&logoColor=white">
  <img src="https://img.shields.io/badge/Notion-%23000000.svg?style=for-the-badge&logo=notion&logoColor=white">
</p>
<!-- 
TODO: colocar el gif
<h1 align="center">
  <a href="#"><img src="./assets/capture.gif" alt="" width="70%"></a>
</h1> -->


## Integrantes

| Apellidos y Nombres       | Código de alumno | % Participación |
|---------------------------|------------------|-----------------|
| Morales Panitz, Alexander | 202020195        | 100%            |
| Ugarte Quispe, Grover     | 202020195        | 100%            |
| Gutierrez Guanilo, Luis   | 202010074        | 100%    

| Lista de actividades realizadas                                                                                                                                                                | Responsable       | Nota |
|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------|------|
| Creación del algoritmo de Single pass in memory, creación de la clase del indice invertido, creación de instrucciones de retrieval en sql y nuestra python                                                                                                | Grover Ugarte     |      |
| Aplicabilidad del hash dentro de single pass in memory                                                                                      | Alexander Morales |      |
| GUI de inicio a fin, diseño de la GUI,  parser para las peticiones, manejo de la API para la obtención de similitudes por postgres y nuestra implementación | Luis Gutierrez    |      |



# Enlace del video: https://youtu.be/Ty75uPJ7sX4

# Enlace al dataset unido completo All the news de Kaggle: https://drive.google.com/file/d/14gxCwBHZ--SpBmdM3xkL1NpDOESPxmoo/view?usp=sharing

# Agregar los siguientes archivos en la carpeta <a href="https://github.com/alexanderutec/BD2-P2/tree/LUIS/app/static">estatica de la aplicación</a>

- <a href="https://drive.google.com/file/d/14gxCwBHZ--SpBmdM3xkL1NpDOESPxmoo/view?usp=sharing">articles.csv</a>
- <a href="https://drive.google.com/file/d/11ya84UdrdREkQ5aIK35QcQvXHH9daL4A/view?usp=sharing">df_r.json </a>
- <a href="https://drive.google.com/file/d/122UNaZyg82MwUJl_zEDIoVks8eqwMPOG/view?usp=sharing">idf_r.json</a>
- <a href="https://drive.google.com/file/d/14_3VE2Bfa5pgpenTozIHLXo29CXfQEjR/view?usp=sharing">length_.json</a>
- <a href="">stoplist.txt</a>
- <a href="https://drive.google.com/file/d/14bXOC8hBo_YjUeg0bMlhm7IY93SPw2UK/view?usp=sharing">tf_idf_r.json</a>
- <a href="https://drive.google.com/file/d/14TaoqmxBdKe92MGbVVi3e2b98cQA-xeC/view?usp=sharing">tf_rrrrrr1.json</a>

Estos archivos no pueden estar en el repositorio debido a que son demasiado grandes.

## Introducción

El presente proyecto tiene como objetivo el aprendizaje de la recuperación de texto. El método más conocido para aquello es mediante el Índice Invertido. El cual tiene la finalidad de describir la frecuencia de una palabra en un documento y a partir de aquello verificar similitudes entre aquello y el documento. Por ese motivo, el objetivo es implementar aquella  estructura para datos masivos utilizando python y hacer comparaciones con la similitud de consultas de texto en SQL.

Con respecto al empleo de datos masivos, nos hemos basado en la recopilación de noticias de Kaggle denominada: All the news (https://www.kaggle.com/datasets/snapcrack/all-the-news?resource=download). 

![](img/lazy-news.gif)

La cual cuenta con los siguientes campos:

- Num: Identificador (int)
- Title: Título de la noticia (texto)
- Publication: Editorial (varchar)
- Author: Autor (varchar)
- Date: Fecha (date)
- Year: Año (numeric)
- Month: Mes (numeric)
- URL: Enlace a noticia (text)
- Content: Contenido de la noticia (text)


## Fundamentación para la elaboración del Índice Invertido

Para las operaciones del índice invertido se decidió crear una clase llamada <a href="https://github.com/alexanderutec/BD2-P2/blob/main/src/inverted_index.py">**InvertedIndex**</a>

Por ese motivo, es necesario realizar una explicación de sus métodos.

### Constructor

```py 
def __init__(self, ruta_datos, ruta_raiz, N_reg_part=5000)
```
- ruta_datos: Ruta donde se encuentra el archivo con los datos de noticias (*articles.csv*)
- ruta_raiz: Ruta donde se desea que los archivos de salvado de la instancia del índice se guarden
- N_reg_part: Cuando se crean índices invertidos locales, se tomará con respecto a una cantidad por defecto 5000 registros por índice

Lo que hará el constructor será incializar aquellos valores como atributos y creará un Stemmer para tokenizar el lengaje natural.

### Definir donde se inicializaron archivos previos

```py
def archivosPrevios(self, n_colecciones, tf, df = "df_r", idf="idf_r", tfidf="tf_idf_r", length="length_r")
```

- n_colecciones: Cantidad de registros contiene el archivo de datos original
- tf: El nombre del archivo donde se encuentra exportado el índice invertido de frecuencia de términos global que ya fue mezclado
- df: El nombre del archivo donde se encuentra exportado los datos del índice invertido de frecuencia de archivos que contienen una palabra
- idf: El nombre del archivo donde se encuentra exportado el índice invertido con los valores df invertidos normalizados mediante la fórmula vista en clase
- tfidf: El nombre del archivo donde se encuentra exportado el índice invertdo con los valores tfidf de cada término por cada documento
- length: El nombre del archivo donde se encuentra exportado el índice invertido con los datos de la distancia de cada vector tfidf de cada término

Esta función se utiliza para cuando el índice invertido ya haya sido creado en su totalidad y solo sea necesaria su carga. Por lo que se introducen los nombres donde fueron guardados.

### Procesamiento de lenguaje

```py
def procesamiento(self, texto)
```
- texto: Se recibe el texto natural

Esta función es la vista en clase que utiliza el *SnowballStemmer* para tokenizar el texto introducido.

### Construcción de Indices Invertidos de TF locales

```py
def construirIndiceTF(self)
```

Esta función va por cada registro dentro del DataFrame y va tokenizando el contenido y el título de la noticia para ir creando un indice invertido de TF temporal. Al llegar a la cantidad N de registros a tomar (5000 por defecto), exporta el índice invertido en un json numerizado y repite el proceso hasta que se terminan las entradas.

### Construcción del Indice DF

```py
def construirIndiceDF(self)
```

Esta función se encarga de crear los indices de los términos que se presentan en *n* documentos. A pesar de que el índice invertido no haya sido construido, este utiliza todos los indices locales para construir este. Finalmente lo exporta en un json.

### Construcción del Indice IDF

```py
def construirIndiceIDF(self)
```

Esta función se encarga de crear los valores IDF utilizando el índice de DF exportado.

### Single Pass In Memory

```py
def mezclarIIParciales(self,N_pages=-1, i1=0, i2=0, prefix=None)
```

- N_pages: La cantidad de paginas que tienen indices invertidos locales de un nivel específico
- i1: Iterador numérico que trabaja con respecto al indice tf local numerizado mínimo de un nivel
- i2: Iterador numérico que trabaja con respecto al índice tf local numerizado máximo de un nivel
- prefix: El prefijo con el que el último índice invertido local de un nivel *x* fue exportado

Esta función se encarga de realizar el algoritmo de Single Pass in Memory mediante los siguientes pasos:

1. Cuando se hace la primera llamada (sin algún argumento)
   1. Se asigna el índice *i1* a la primera página del II local (1) e *i2* a la última (N_pages)
   2. Se define el prefijo con el que se exportará el índice invertido local del siguiente nivel
2. Si *i1* es mayor a *i2* y el número de paginas sea mayor a 1:
   1. Iteramos entre cada dos páginas de todos los índice invertidos locales
      1. Estos dos índices son cargados como diccionarios y por cada entrada (palabra):
         1. Si está presente en el diccionario de número menor, se itera por cada una de los archivos que contienen esa palabra en el otro diccionario y se le agregan al primer diccionario
         2. En caso contrario, se define una nueva entrada al diccionario de la palabra con aquellos valores del segundo diccionario
   2. Este nuevo diccionario mezclado de nivel superior es guardado en un nuevo archivo con el índice númerico incrementado agregandole un caracter *r* al prefijo como nuevo identificador.
   3. Si el nivel tiene una cantidad de páginas par, este llama a la función de la siguiente forma ```self.mezclarIIParciales(N_pages//2, i1, i2//2, prefix+"r")```
   4. En caso contrario 
      1. La página que no fue considerada en la mezcla de pares es clonada y cambiada de prefijo para llevarla al siguiente nivel
      2. Se llama la función de la siguiente manera ```self.mezclarIIParciales(N_pages//2+1, i1, i2//2+1, prefix+"r")```
3. En caso solamente haya una sola página, significa que el índice ya fue mezclado totalmente, por lo que el prefijo del último nivel creado se le asigna al atributo dl nombre del archivo exportado de indice invertido que contiene los valores TF de cada término

### Obtención de la distancia de cada vector TF_IDF

```py
def sacar_largo(self)
```

Esta función se encarga de importar el indice invertido global con los datos TF_IDF y por cada palabra, este considera sus valores como un vector y obtiene su distancia mediante la fórmula euclidiana.

### Obtención del índice invertido con datos TF_IDF

```py
def sacar_tf_idf(self)
```

Esta función emplea el diccionario obtenido tras importar el archivo con el índice invertido con valores TF global y el índice con valores IDF. Se emplea la fórmula vista en clase y se procede a exportar este índice como un archivo json.

### Prepara un objeto indice invertido cuando se quiere utilizar en una aplicación

```py
def prepararRetrieval(self)
```

Esta función requiere que los archivos exportados de TF global, DF, IDF, distancia y TF_IDF ya hayan sido creados. Lo que realizará es cargarlos en la memoria RAM para facilitar su acceso.

### Procesamiento de frases y retorno de similitudes por medio de similitud de coseno

```py
def retrieval(self, query, k=1)
```

- query: Texto a buscar similitud en los datos
- k: Cantidad registros a retornar con mayor similitud

Esta función hace el uso del TF_IDF, distancias, IDF para realizar similitudes de la siguiente forma:
 
1.  Se emplea la función ```procesamiento``` con el *query* para formar un vector de frecuncias con cada token
2.  Para obtener el tf-idf del *query*, empleamos el archivo IDF para por cada token del vector tf de *query*.
    1.  Si un token del query no se encuentra en el indice IDF, esta entrada es eliminada del vector
3. Obtenemos la distancia del vector *query*
4. Creamos una lista que contendo los resultados de similitud
5. Empleamos la similitud de coseno con un registro *n*:
   1. Por cada palabra en el vector query:
      1. Accedemos a la palabra en el índice TF-IDF y accedemos a la entrada *n*
      2. Multiplicamos cada valor (Se realiza el producto escalar de vectores)
   2. Finalmente, accedemos al índice de distancias y obtenemos el valor de la distancia *n* y la multiplicamos con la distancia del query para luego dividir el resultado del producto escalar
   3. Agregamos el resultado a la lista y volvemos a repetir desde el paso 1 hasta cubrir todos los registros
6. Ordenamos la lista poblada de forma descendente
7. Retornamos los primero *k* elementos

## Parte SQL

A continuación se presentan los comandos SQL para poblar una tabla con los datos presentados.
```sql
-- CREAR TABLA
create table articles(
    id INT primary key,
    title text,
    publication VARCHAR(100),
    author text,
    fecha DATE,
    anho NUMERIC,
    mes NUMERIC,
    enlace text,
    content text
);

-- COPIAR DATOS DEL CSV
COPY articles(id, title, publication, author, fecha, anho, mes, enlace, content)
FROM 'DIRECCION PUBLICA DEL CSV ARTICLES'
DELIMITER ','
CSV HEADER;

-- CREAR NUEVA COLUMNA
alter table articles add column content_ts tsvector;
-- POBLAR NUEVA COLUMNA
update articles
set content_ts = x.content_ts
from (
    select id, setweight(to_tsvector('english', title), 'A') ||
    setweight(to_tsvector('english', content), 'A')
    as content_ts from articles
) as x
where x.id = articles.id;
-- CREAR INDICE GIN
create index idx_content_ts on articles using gin(content_ts);

```

Para que una query sea aplicada en sql, lo que se realizó fue aplicar la función ```procesamiento```  para tokenizar la frase y agregarla a la consulta SQL separados mediante el separador | utilizando la librería *psycopg2*. La consulta se da de la siguiente forma:

```sql
-- BUSQUEDA (USAR CON PSYCOPG2)
select title, content, ts_rank_cd(content_ts, query_ts) as score
from articles, to_tsquery('english', 'PALABRAS SEPARADAS EN PYTHON') query_ts
where query_ts @@ content_ts
order by score desc
limit 20;
```

## Experimentación 

Para la experimentación, se accedió a probar con frases de 10, 100 y 600 palabras. Para medir el tiempo en nuestra aplicación, se utilizó la librería *time*.

### Resultados

Se obtuvieron los siguientes resultados en milisegundos:

|     | Implementación | SQL        |
| --- | -------------- | ---------- |
| 10  | 116,555        | 2289,24    |
| 10  | 115,156        | 4212,89    |
| 10  | 101,221        | 4001,23    |
| 100 | 150,292        | 88603,147  |
| 100 | 200,121        | 93235,345  |
| 100 | 170,788        | 91221,321  |
| 600 | 458,585        | 528843,825 |
| 600 | 512,6          | 522644,103 |
| 600 | 488,734        | 523885,112 |


![](img/Implementación%20y%20SQL.png)

### Interpretación y análisis

Observamos de que las consultas en SQL tardan mucho más que en la implementación python. Esto puede darse a diversos motivos:
- Latencia de la librería *psycopg2*
- La aplicación importa la clase IndiceInvertido antes de ejecutar
- Los archivos de índice invertido son cargados a medida que comienza la aplicación y ya se encuentran en RAM


