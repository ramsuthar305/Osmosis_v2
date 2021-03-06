"""Flask config class."""
import os
from os.path import join, dirname, realpath


class Config:
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SESSION_TYPE = os.environ.get('SESSION_TYPE')
    MONGO_URI = os.environ.get('MONGO_URI')
    FLASK_ENV = os.environ.get('FLASK_ENV')
    UPLOAD_FOLDER = join(dirname(realpath(__file__)), os.environ.get('UPLOAD_FOLDER')+"/")


# class ProdConfig(Config):
#     DEBUG = False
#     TESTING = False
#     DATABASE_URI = os.environ.get('PROD_DATABASE_URI')
#
#
# class DevConfig(Config):
#     DEBUG = True
#     TESTING = True
#     DATABASE_URI = os.environ.get('DEV_DATABASE_URI')
