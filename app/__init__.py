from flask import Flask, render_template
from flask_login import LoginManager

from .config.config import Config
from .home import home as homeViews

app = None
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = 'clave secretita'
    
 
    # register blueprint apps
    app.register_blueprint(homeViews)
    # Flask DB Migration

    print(app.config['UPLOAD_FOLDER'])

    #handlers de errores
    register_error_handlers(app)
    return app

def register_error_handlers(app):

    @app.errorhandler(500)
    def base_error_handler(e):
        return render_template('500.html'), 500

    @app.errorhandler(404)
    def error_404_handler(e):
        return render_template('404.html'), 404

    @app.errorhandler(401)
    def error_404_handler(e):
        return render_template('401.html'), 401