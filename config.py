import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Development:
    DEBUG = True
    SECRET_KEY = "Very sec"
    SQLALCHEMY_DATABASE_URI = "sqlite:///data.sqlite"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'my_uploads')

    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
