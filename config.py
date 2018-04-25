import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    # MONGODB_USER = ''
    # MONGODB_PASSWD= ''
    # MONGODB_HOST= '127.0.0.1'
    # MONGODB_NAME = 'test'
    # # MONGODB_DATABASE_HOST = 'mongodb://%s:%s@%s/%s' % MONGODB_USER, MONGODB_PASSWD, MONGODB_HOST, MONGODB_NAME
    # MONGODB_DATABASE_HOST = 'mongodb://%s' % MONGODB_HOST

    MONGODB_SETTINGS = {
        'db': 'test',
        'host': '127.0.0.1',
    }
