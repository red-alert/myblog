import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    MONGODB_USER = os.environ.get('MONGODB_USER') or None
    MONGODB_PASSWD = os.environ.get('MONGODB_PASSWD') or None
    MONGODB_HOST = os.environ.get('MONGODB_HOST') or '127.0.0.1'
    MONGODB_NAME = os.environ.get('MONGODB_NAME') or 'test'
    # # MONGODB_DATABASE_HOST = 'mongodb://%s:%s@%s/%s' % MONGODB_USER, MONGODB_PASSWD, MONGODB_HOST, MONGODB_NAME
    # MONGODB_DATABASE_HOST = 'mongodb://%s' % MONGODB_HOST

    MONGODB_SETTINGS = {
        'db': MONGODB_NAME,
        'host': MONGODB_HOST,
        'username': MONGODB_USER,
        'password': MONGODB_PASSWD
    }

    REDIS_HOST = os.environ.get('REDIS_HOST') or None
    REDIS_PORT = os.environ.get('REDIS_PORT') or None
    REDIS_SETTINGS = {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
    }

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

    PICTURES_DIR = os.path.join(APP_DIR, 'static/pictures')
    UPLOAD_FOLDER = 'app/static/pictures'
    STATIC = 'app/static'

    ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
    MAX_CONTENT_LENGTH = 16*1024*1024

    PIC_PER_PAGE = 10
