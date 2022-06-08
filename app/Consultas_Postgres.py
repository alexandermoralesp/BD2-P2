import psycopg2
import nltk
import pandas as pd
# nltk.download("punkt")
from nltk.stem.snowball import SnowballStemmer

stemmer = SnowballStemmer("english")

def procesamiento( texto):
    texto_tokens = nltk.word_tokenize(texto)

    with(open("stoplist.txt")) as f:
      stoplist = [line.lower().strip() for line in f]
    stoplist += [',', '.', '?', '¿', ":", "``", "''", "(", ")", ":", ";"]

    texto_tokens_c = texto_tokens[ : ]
    for token in texto_tokens:
      if token.lower() in stoplist:
        texto_tokens_c.remove(token)

    texto_tokens_s = []
    for w in texto_tokens_c:
      texto_tokens_s.append(stemmer.stem(w))
    return texto_tokens_s

def query(words, k):
    words = procesamiento(words)
    prim = "select title, content, ts_rank_cd(content_ts, query_ts) as score from articles, to_tsquery('english', '"
    ts_word = " | ".join(words)
    sec = "') query_ts where query_ts @@ content_ts order by score desc limit "+str(k)+";"
    return prim+ts_word+sec

def POSTGRES_QUERY(texto, k):
    conn = psycopg2.connect("host=localhost dbname=p2 user=Grove password=root")
    cur = conn.cursor()

    cur.execute(query(texto, k))
    regs = cur.fetchall()
    # INDICE 0: TITULO, INDICE 1: CONTENIDO, INDICE 2: PUNTAJE

    cur.close()
    conn.close()

    return pd.DataFrame(regs, columns=['Title', "Content", "Score"])

print(POSTGRES_QUERY("FACEBOOK", 5)["Content"])
