from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
# import mongoengine
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface
from flask_login import LoginManager
from flask_cache import Cache

app = Flask(__name__)
app.config.from_object(Config)
# db = mongoengine.connect(app.config['MONGODB_NAME'], host=app.config['MONGODB_HOST'])
# db = mongoengine.connect('test', host='127.0.0.1')
# print("mongodb connected!")
# db.close()
# print("mongodb closed!")
db = MongoEngine(app)
# app.session_interface = MongoEngineSessionInterface(db)

login = LoginManager(app)
login.login_view = 'login'

bootstap = Bootstrap(app)

cache = Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

from app import routes
