from flask import request, flash, jsonify, render_template
from flask import redirect, url_for
from flask_restful import Resource
from app.place import api, bp
from app.place.models import RedisCanvas
from app.place.models import Pixel as p
from app.place.forms import TestForm

from flask import Response

import struct

@bp.route('/place', methods=['GET','POST'])
def place_page():
    p.create(14,1,1)
    p.create(15,2,1)
    p.create(10,3,1)
    p.create(13,1,0)
    p.create(9,0,0)
    p.create(10,2,0)
    p.create(11,3,0)
    p.create(12,4,0)
    p.create(13,5,0)
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
        board = RedisCanvas.get_board()
        return Response(board)

    def post(self):
        try:
            req_pixel = request.json
            p.create(req_pixel['color'],req_pixel['x'],req_pixel['y'])
            return 201
        except:
            raise
