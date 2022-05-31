
import os
from datetime import datetime
from email.message import Message
from itertools import accumulate
from os import access
from unicodedata import name
import hashlib
from unittest import result
from urllib import response
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
        Query = request.get_json()['Query']
        aux =[{Query:'asdasd','hddf':'poposs'},{Query:'asasfdf','hddf':'fdgh'}]
        print(aux)
        print(jsonify(aux))
        return jsonify(aux)
    elif request.method == 'GET':
        return render_template("on-sql.html")

@home.route("/our_implementation/",methods = ['GET','POST'])
def our_implementation():
    if request.method == 'POST':
        
        Query = request.get_json()['Query']
        aux =[{Query:'asdasd','hddf':'poposs'},{Query:'asasfdf','hddf':'fdgh'}]
        print(aux)
        print(jsonify(aux))
        return jsonify(aux)
        
    elif request.method == 'GET':
        
        return render_template("our-implementation.html")    
