import os

basedir = os.path.abspath(os.path.dirname(__file__))

#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'test.db')
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.abspath(os.getcwd())+'\migrations\\test_db\\test.db'


SECRET_KEY = os.environ.get('SECRET_KEY', "dfsgsd98g7ds98g7sgjh")
SQLALCHEMY_TRACK_MODIFICATIONS = False