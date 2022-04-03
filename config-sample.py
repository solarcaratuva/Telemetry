import os

basedir = os.path.abspath(os.path.dirname(__file__))


POSTGRES = {
    'user': 'postgres',
    'pw': '',
    'db': '',
    'host': 'localhost',
    'port': '5432',
}

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', '')

    # SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    BASIC_AUTH_USERNAME = ''
    BASIC_AUTH_PASSWORD = ''
