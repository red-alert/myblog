from flask import Flask
from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config)

bootstap = Bootstrap(app)

from app import routes
