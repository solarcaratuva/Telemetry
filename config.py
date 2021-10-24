import os
from credentials import creds
basedir = os.path.abspath(os.path.dirname(__file__))




class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY', creds['key'])
    SQLALCHEMY_DATABASE_URI = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % creds
    SQLALECHMY_DATABASE_URI = 'postgresql://{}:{}@{}:{}/{}'.format(creds['user'],
                            creds['pw'], creds['host'], creds['port'], creds['db'])