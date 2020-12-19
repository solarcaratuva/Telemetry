import os

basedir = os.path.abspath(os.path.dirname(__file__))


POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'telemetry',
    'host': 'localhost',
    'port': '5432',
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', 'vnkdjnfjknfl1232#')



    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

    BASIC_AUTH_USERNAME = 'byoon'
    BASIC_AUTH_PASSWORD = '123'