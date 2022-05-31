from app import create_app

if __name__ == "__main__":
    create_app().run(debug=True, port=5002)

# https://stackoverflow.com/questions/70400863/common-file-structure-with-flask-and-flask-sqlalchemy