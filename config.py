#encoding: utf-8
import os
# import pymysql

DEBUG = True

SECRET_KEY = os.urandom(24)

HOSTNAME = '127.0.0.1'
PORT     = '3306'
DATABASE = 'tornado_01'
USERNAME = 'root'
PASSWORD = 'qwe123'


DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(
    USERNAME,
    PASSWORD,
    HOSTNAME,
    PORT,
    DATABASE
)

SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False