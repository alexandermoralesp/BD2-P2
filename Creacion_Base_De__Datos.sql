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
FROM 'C:\Users\Public\Documents\ARTICLES\articles.csv'
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

-- -- BUSQUEDA (USAR EN PSYCOPG2)
-- select title, content, ts_rank_cd(content_ts, query_ts) as score
-- from articles, to_tsquery('english', 'facebook | facebook') query_ts
-- where query_ts @@ content_ts
-- order by score desc
-- limit 20;