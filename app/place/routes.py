import urllib2

from flask import request, flash, jsonify, render_template
from flask import redirect, url_for
from flask_restful import Resource
from app.place import api, bp
from app.place.models import RedisCanvas
from app.place.models import Pixel as p
from app.place.forms import TestForm



@bp.route('/place', methods=['GET','POST'])
def place_page():
    return render_template('place/place.html')

@api.resource('/place/helloworld', endpoint='HelloWorld')
class HelloWorld(Resource):
    def get(self):
        return {'hello':'world'}

    def post(self):
        req = request.json
        print(dir(request))
        print(req)
        return req, 201

@api.resource('/place/pixel')
class Pixel(Resource):
    def get(self):
        response = RedisCanvas.get_board()
        return response

    def post(self):
        try:
            req_pixel = request.json
            p.create(req_pixel['color'],req_pixel['x'],req_pixel['y'])
            return 201
        except:
            raise
