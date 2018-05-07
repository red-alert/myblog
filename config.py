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
        'db': 'myblog',
        'host': '127.0.0.1',
    }

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

    PICTURES_DIR = os.path.join(APP_DIR, 'pictures')

    UPLOAD_FOLDER = 'app/pictures'
    STATIC = 'app/static'

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16*1024*1024
