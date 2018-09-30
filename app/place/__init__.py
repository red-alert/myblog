from flask import Blueprint
from flask_restful import Api

bp = Blueprint('place', __name__)
api = Api(bp)

from app.place import routes
