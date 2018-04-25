from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
import mongoengine
from flask_mongoengine import MongoEngine, MongoEngineSessionInterface


app = Flask(__name__)
app.config.from_object(Config)
# db = mongoengine.connect(app.config['MONGODB_NAME'], host=app.config['MONGODB_HOST'])
# db = mongoengine.connect('test', host='127.0.0.1')
# print("mongodb connected!")
# db.close()
# print("mongodb closed!")
db = MongoEngine(app)
app.session_interface = MongoEngineSessionInterface(db)

bootstap = Bootstrap(app)

from app import routes
