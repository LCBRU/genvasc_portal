import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    DEBUG = os.environ['DEBUG']
    DB_NAME = os.environ['MYSQL_DATABASE']
    DB_USER = os.environ['MYSQL_USER']
    DB_PASS = os.environ['MYSQL_PASSWORD']
    SQLALCHEMY_DATABASE_URI = 'mysql://gpuser:gppass@mysql/gp'.format(
        DB_USER, DB_PASS, DB_NAME
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO=False
