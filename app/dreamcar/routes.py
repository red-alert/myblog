# from flask_restful import Resource, request
from flask import jsonify, redirct, request

from app.dreamcar.models.hero import Hero
from app.dreamcar.models.scene import Scene

from app.dreamcar import bp

@bp.route('/dreamcar/<id>', methods=['GET','POST'])
def dreamcar(id):
    hero = Hero(id=id)
    scene = Scene(hero=hero)
    if request.args.get('choice'):
        c = request.args.get('choice')
        scene.update(c)
    return render_template('dreamcar/dreamcar.html', scene=scene)

# @bp.route('/dreamcar/<id>', methods=['GET', 'POST'])
# def dreamcar(id):
#     hero = Hero(id=id)
#     scene = Scene(hero=hero)
#     return render_template('dreamcar/dreamcar.html',scene=scene)
#
# @api.resource('/dreamcar/<id>/')
# class DreamCar(Resource):
#     def get():
#         pass
#
#     def put():
#         pass
#
#     def post(id):
#         choice = request.json()["choice"]
#         hero = Hero(id=id)
#         scene = Scene(hero=hero)
#         scene.update(choice)
#         return render_template('dreamcar/dreamcar.html',scene=scene)
#
#     def delete():
#         pass
