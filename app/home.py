
import os
from datetime import datetime
from email.message import Message
from itertools import accumulate
from os import access
from unicodedata import name
import hashlib
from unittest import result
from urllib import response
from app.Consultas_Postgres import POSTGRES_QUERY
from src import inverted_index
import datetime
from flask import (
    Blueprint,
    Flask,
    flash,
    jsonify,
    render_template, 
    redirect, 
    session, 
    url_for, 
    request
)
from flask_login import (
    LoginManager, 
    UserMixin, 
    login_user, 
    login_required, 
    logout_user, 
    current_user
)


from itsdangerous import SignatureExpired, URLSafeTimedSerializer
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename




II =inverted_index.IndiceInvertido("app/static/articles.csv", "app/static/")
II.archivosPrevios(140000,"tf_rrrrrr1")
II.prepararRetrieval()
# blueprints
home = Blueprint('index', __name__, 
                template_folder='templates', static_folder='static')                                                                        

# functions

# endpoints
@home.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@home.route("/on_sql/",methods = ['GET','POST'])
def on_sql():
    if request.method == 'POST':  
        start = datetime.datetime.utcnow()  
        Query = request.get_json()['Query']
        K = int(request.get_json()['K'])
        if not K:
            K = 1
        restult = POSTGRES_QUERY(Query, K)
        print(restult)
        aux = []
        for i in restult.values:
            tmp = {}
            tmp["Consulta"]=i[0]
            tmp["Contenido"]=i[1][:1250]
            tmp["Similitud"]=i[2]
            aux.append(tmp)
        end = datetime.datetime.utcnow()
        result = end - start
        resp = [{"descripcion": "El codigo tarda:","e" : str(int(result.seconds)) + " segundos", "f" : str(int(result.microseconds)/1000) + " milisegundos"}]
        print(result.seconds)
        print(result.microseconds)
        retorno = [aux,resp]
        return jsonify(retorno)
    elif request.method == 'GET':
        return render_template("on-sql.html")

@home.route("/our_implementation/",methods = ['GET','POST'])
def our_implementation():
    if request.method == 'POST':
        start = datetime.datetime.utcnow()
        Query = request.get_json()['Query']
        K = int(request.get_json()['K'])
        if not K:
            K = 1
        restult = II.retrieval(Query, K)
        aux = []
        for i in restult.values:
            tmp = {}
            tmp["Consulta"]=i[1]
            tmp["Contenido"]=i[8]
            tmp["Similitud"]=i[9]
            aux.append(tmp)
        end = datetime.datetime.utcnow()
        result = end - start
        resp = [{"descripcion": "El codigo tarda:","e" : str(int(result.seconds)) + " segundos", "f" : str(int(result.microseconds)/1000) + " milisegundos"}]
        print(result.seconds)
        print(result.microseconds)
        retorno = [aux,resp]
        return jsonify(retorno)
        
    elif request.method == 'GET':
        
        return render_template("our-implementation.html")    
