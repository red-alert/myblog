from flask import Blueprint

bp = Blueprint('dreamcar', __name__)

from app.dreamcar import routes, admin
                                                                                                                    
