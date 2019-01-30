from flask_restful import Resource
from flask import jsonify

from app.dreamcar import api, bp



@bp.route('/dreamcar', methods=['GET', 'POST'])
def dreamcar():
    return render_template('dreamcar/dreamcar.html')

@api.resource('/dreamcar/<id>')
class DreamCar(Resource):
    def get():
        pass

    def put():
        pass

    def post():
        pass

    def delete():
        pass
