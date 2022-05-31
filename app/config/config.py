
class Config():
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1234@localhost:5432/dbp20'       # dialecto + dbapi
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = './static/img/'
    MAIL_SERVER= 'smtp.gmail.com'
    MAIL_DEBUG = True
    MAIL_USERNAME= 'dbpcorreoprueba@gmail.com'
    MAIL_PASSWORD= 'Utecdbp12345'
    MAIL_DEFAULT_SENDER= 'dbpcorreoprueba@gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL=True
    MAIL_USE_TLS=False
