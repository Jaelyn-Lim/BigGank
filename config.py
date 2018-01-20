import os

DEBUG = True
SECRET_KEY = os.urandom(24)

# mysql://username:password@hostname/database
# mssql+pymssql://user:@pwd@host/db
USERNAME = 'root'
PASSWORD = ''
HOSTNAME = 'localhost:3306'
DATABASE = 'gank'
CHARSET = 'utf8'
DATABASE_TYPE = 'mysql+pymysql'

SQLALCHEMY_DATABASE_URI = '{}://{}:{}@{}/{}?charset={}'.format(DATABASE_TYPE, USERNAME, PASSWORD, HOSTNAME, DATABASE, CHARSET)

SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

CSRF_ENABLED = True