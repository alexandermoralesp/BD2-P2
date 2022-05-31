# Import dependencies
import nltk
"""nltk.download("punkt")"""
from nltk.stem.snowball import SnowballStemmer
import math
import json


class InvertedIndex:
    """
    Inverted Index class
    --------------------

    """
    def __init__(self, archivo_indice):
        self.archivo_indice = archivo_indice
        self.stemmer = SnowballStemmer("spanish")
        self.index = {}
        self.idf = {}
        self.tf = {}
        self.tf_idf = {}
        self.length = {}

    def procesamiento(self, texto):
        texto_tokens = nltk.word_tokenize(texto)

        with(open("data/stoplist.txt")) as file:
            stoplist = [line.lower().strip() for line in file]
        stoplist += [',', '.', '?', '¿', ":", "``", "''", "(", ")", ":", ";"]

        texto_tokens_c = texto_tokens[:]
        for token in texto_tokens:
            if token.lower() in stoplist:
                texto_tokens_c.remove(token)

        texto_tokens_s = []
        for w in texto_tokens_c:
            texto_tokens_s.append(self.stemmer.stem(w))
        return texto_tokens_s

    def building(self, df):
        for i in range(df.shape[0]):
            texto_filtrado = self.procesamiento(df.title_content[i])
            for w in texto_filtrado:
                if w in self.index:
                    self.index[w] = self.index[w] + [i]
                    self.tf[w][i] += 1
                else:
                    self.index[w] = [i]
                    self.tf[w] = {}
                    for reg_i in range(df.shape[0]):
                        self.tf[w][reg_i] = 0
                    self.tf[w][reg_i] = 1

        for key in self.index:
            self.index[key] = sorted(list(set(self.index[key])))
        # compute the idf
            self.idf[key] = math.log10(df.shape[0]/len(self.index[key]))
        for key in self.tf:
            self.tf_idf[key] = {}
            for key2 in self.tf[key]:
                self.tf_idf[key][key2] = math.log10(
                    1+self.tf[key][key2])*self.idf[key]

        # compute the length (norm)
        for tx in range(df.shape[0]):
            self.length[tx] = 0
            for key in self.tf:
                if self.tf[key][tx] != 0:
                    self.length[tx] += (math.log10(self.tf[key][tx]))**2
            self.length[tx] = (self.length[tx])**0.5

        # store in disk
        out_file = open(self.archivo_indice+"_index.json", "w")
        json.dump(self.index, out_file, indent=6)
        out_file.close()
        out_file = open(self.archivo_indice+"_idf.json", "w")
        json.dump(self.idf, out_file, indent=6)
        out_file.close()
        out_file = open(self.archivo_indice+"_tf.json", "w")
        json.dump(self.tf, out_file, indent=6)
        out_file.close()
        out_file = open(self.archivo_indice+"_tf_idf.json", "w")
        json.dump(self.tf_idf, out_file, indent=6)
        out_file.close()
        out_file = open(self.archivo_indice+"_length.json", "w")
        json.dump(self.length, out_file, indent=6)
        out_file.close()

    def get_tfidf(self, query_terms):
        temp_d = {}
        for tk in query_terms:
            temp_d[tk] = self.tf_idf[tk]
        return temp_d

    def retrieval(self, query, k):
        self.load_index(self.index_file)
        # diccionario para el score
        score = {}
        # extraer los terminos unicos del query
        query_terms = self.procesamiento(query)
        # calcular el tf-idf del query
        tfidf_query = self.get_tfidf(query_terms)
        for term in query_terms:
            list_pub = self.tf[term]
            idf = self.idf[term]
            for docid in list_pub:
                if docid not in score:
                    score[docid] = 0
                tfidf_doc = list_pub[docid] * idf
                score[docid] += tfidf_query[term][docid] * tfidf_doc
        # aplicar la norma
        for docid in self.length:
            score[docid] = score[docid] / self.length[docid]

        # convertir el diccionaro score a una lista [(doc1, score1), (doc2, score2), ...]
        # ordenar respecto al score de forma descendente
        result = sorted(score.items(), key=lambda tup: tup[1], reverse=True)
        # retornamos los k documentos mas relevantes (de mayor similitud al query)
        return result[:k]

    def load_index(self):
        f = open(self.archivo_indice+"_index.json")
        self.index = json.load(f)
        f.close()
