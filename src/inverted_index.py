import pandas as pd
import numpy as np
import nltk
nltk.download("punkt")
from nltk.stem.snowball import SnowballStemmer
import os.path
import math
import json

class IndiceInvertido:
  def __init__(self, ruta_datos, ruta_raiz, N_reg_part=5000):
    self.N = N_reg_part
    self.ruta_datos = ruta_datos
    self.ruta_raiz = ruta_raiz
    self.stemmer = SnowballStemmer("english")
    self.datos = pd.read_csv(self.ruta_datos)

  def archivosPrevios(self, n_colecciones, tf, df = "df_r", idf="idf_r", tfidf="tf_idf_r", length="length_r"):
    self.archivo_tf = tf
    self.archivo_df = df
    self.archivo_idf = idf
    self.archivo_tf_idf = tfidf
    self.archivo_length = length
    self.n_colecciones = n_colecciones
    self.n_paginas = n_colecciones//self.N
  
  def procesamiento(self, texto):
    texto_tokens = nltk.word_tokenize(texto)

    with(open(self.ruta_raiz+"stoplist.txt")) as f:
      stoplist = [line.lower().strip() for line in f]
    stoplist += [',', '.', '?', '¿', ":", "``", "''", "(", ")", ":", ";"]

    texto_tokens_c = texto_tokens[ : ]
    for token in texto_tokens:
      if token.lower() in stoplist:
        texto_tokens_c.remove(token)

    texto_tokens_s = []
    for w in texto_tokens_c:
      texto_tokens_s.append(self.stemmer.stem(w))
    return texto_tokens_s

  def construirIndiceTF(self):
    datos_temp = self.datos.title + " " + self.datos.content

    self.n_colecciones = datos_temp.shape[0]
    self.n_paginas = self.n_paginas//self.N
    self.archivo_fraccion_tf = "tf_r"

    tf_dict = dict()
    for i in range(datos_temp.shape[0]):
      tokens = None
      if type(datos_temp.title_content[i]) == str:
        tokens = self.procesamiento(datos_temp.title_content[i]) 
      elif type(datos_temp.content[i]) == str:
        tokens = self.procesamiento(datos_temp.content[i]) 
      else:
        tokens = self.procesamiento(datos_temp.title[i])
      for j in tokens:
        if j in tf_dict.keys():
          if i in tf_dict[j].keys():
            tf_dict[j][i] += 1
          else:
            tf_dict[j][i] = 1
        else:
          tf_dict[j] = dict()
          tf_dict[j][i] = 1
      if (i+1)%self.N == 0:
        with open(self.ruta_raiz+self.archivo_fraccion_tf+str((i+1)//self.N)+".json", "w") as f:
          json.dump(tf_dict, f, indent = 2)
          f.close()
        tf_dict = {}

  def construirIndiceDF(self):
    self.archivo_df = "df_r"
    df_dict = {}
    for i in range(1,self.n_paginas+1):
      tf_page = None
      with  open(self.ruta_raiz+str(i)+".json", "r") as f:
        tf_page = json.load(f)
        f.close()
      for j in tf_page.keys():
        if j in df_dict.keys():
          df_dict[j] += len(tf_page[j].keys())
        else:
          df_dict[j] = len(tf_page[j].keys())
    with open(self.ruta_raiz+self.archivo_df+".json", "w") as f:
      json.dump(df_dict, f)
      f.close()

  def construirIndiceIDF(self):
    self.archivo_idf = "idf_r"
    with open(self.ruta_raiz+self.archivo_df+".json", "r") as f:
      idf_dict = {}
      df_dict = json.load(f)
      for i in df_dict.keys():
        idf_dict[i] = math.log10(self.n_colecciones/df_dict[i])
      with open(self.ruta_raiz+self.archivo_idf+".json", "w") as f1:
        json.dump(idf_dict, f1)
        f1.close()
      f.close()

  def mezclarIIParciales(self,N_pages=-1, i1=0, i2=0, prefix=None):
    if N_pages < 0:
      N_pages = self.n_paginas
      i1 = 1
      i2 = N_pages
      prefix = self.archivo_fraccion_tf

    if i1 < i2 or N_pages > 1:
      for i in range(i1+1, i2+1, 2):
        dict1 = {}
        dict2 = {}
        f = open(self.ruta_raiz+prefix+str(i)+".json", "r")
        dict1 = json.load(f)
        f.close()
        f = open(self.ruta_raiz+prefix+str(i-1)+".json", "r")
        dict2 = json.load(f)
        f.close()
        for key2 in dict2:
          if key2 in dict1.keys():
            for colkey2 in dict2[key2]:
              dict1[key2][colkey2] = dict2[key2][colkey2] 
          else:
            dict1[key2] = dict2[key2]

        f = open(self.ruta_raiz+prefix+"r"+str(i//2)+".json", "w")
        json.dump(dict1, f)
        f.close()
      if N_pages%2 == 0:
        self.mezclarIIParciales(N_pages//2, i1, i2//2, prefix+"r")
      else:
        f = open(self.ruta_raiz+prefix+str(i2)+".json", "r")
        dict1 = json.load(f)
        f.close()
        f = open(self.ruta_raiz+prefix+"r"+str(i2//2+1)+".json", "w")
        json.dump(dict1, f)
        f.close()
        self.mezclarIIParciales(N_pages//2+1, i1, i2//2+1, prefix+"r")
    else:
      self.archivo_tf = prefix

  def sacar_largo(self):
    self.archivo_length = "length_r"
    tf_dict = None
    with open(self.ruta_raiz+self.archivo_tf_idf+".json") as f:
      tf_dict = json.load(f)
      f.close()
    length_array = [0] * self.n_colecciones
    for word in tf_dict:
      for key in tf_dict[word]:
        length_array[int(key)] += (tf_dict[word][key])**2
    for i in range(self.n_colecciones):
      length_array[i] = length_array[i]**0.5
    with open(self.ruta_raiz+self.archivo_length+".json", "w") as f:
      json.dump(length_array, f)
      f.close()

  def sacar_tf_idf(self):
    self.archivo_tf_idf = "tf_idf_r"
    # tf_dict pasa a ser tfidf_dict
    tf_dict = None
    with open(self.ruta_raiz+self.archivo_tf+".json", "r") as f:
      tf_dict = json.load(f)
      f.close()
    idf_dict = None
    with open(self.ruta_raiz+self.archivo_idf+".json", "r") as f:
      idf_dict = json.load(f)
      f.close()
    for word in tf_dict:
      for index in tf_dict[word]:
        tf_dict[word][index] = math.log10(1+tf_dict[word][index])*idf_dict[word]
    with open(self.ruta_raiz+self.archivo_tf_idf+".json", "w") as f:
      json.dump(tf_dict, f)
      f.close()


  def retrieval(self, query, k=1):
    tf_idf_dict = None
    with open(self.ruta_raiz+self.archivo_tf_idf+".json", "r") as f:
      tf_idf_dict = json.load( f)
      f.close()
    idf_dict = None
    with open(self.ruta_raiz+self.archivo_idf+".json", "r") as f:
      idf_dict = json.load( f)
      f.close()
    length_dict = None
    with open(self.ruta_raiz+self.archivo_length+".json", "r") as f:
      length_dict = json.load( f)
      f.close()
    
    scores = {}
    query_terms = self.procesamiento(query)

    # TF_IDF DEL QUERY
    tf_idf_query_dict = {}
    #obtener tf
    for i in query_terms:
      if i in tf_idf_query_dict.keys():
        tf_idf_query_dict[i] += 1
      else:
        tf_idf_query_dict[i] = 1


    #obtener tf_idf
    for i in tf_idf_query_dict:
      if i in idf_dict.keys():
        tf_idf_query_dict[i] = math.log10(tf_idf_query_dict[i]+1)*idf_dict[i]
      else:
        del tf_idf_query_dict[i]
    
    #obtener query_length
    q_length = 0
    for i in tf_idf_query_dict:
      q_length += (tf_idf_query_dict[i])**2
    q_length = q_length**0.5

    # COSINE SCORE
    for qtx in tf_idf_query_dict:
      for df_id in tf_idf_dict[qtx]:
        scores[df_id] = tf_idf_dict[qtx][df_id]*tf_idf_query_dict[qtx]

    for i in scores:
      if length_dict[int(i)] == 0:
        scores[i] = 0
      else:
        scores[i] /= (length_dict[int(i)]*q_length)

    result = sorted(scores.items(), key= lambda tup: tup[1], reverse=True)
    indices = [int(result[i][0])  for i in range(0, k)]
    similitud = [result[i][1] for i in range(0,k)]

    res_data = self.datos.loc[indices,:]
    res_data["similitud"] = similitud
    return res_data