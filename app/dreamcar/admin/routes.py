from flask import render_template

from app.dreamcar.models.hero import HeroDB

from app.dreamcar import bp
from app.dreamcar.models.hero import HeroDB
from app.dreamcar.models.house import HouseDB
from app.dreamcar.models.job import JobDB
from app.dreamcar.models.contract import ContractDB
from app.dreamcar.models.car import CarDB
from app.dreamcar.models.market import MarketDB
from app.dreamcar.admin.forms import HeroForm

@bp.route('/dreamcar_addhero', methods=['GET', 'POST'])
def dreamcar_addhero():
    form = HeroForm()
    if form.validate_on_submit():
        hero = HeroDB(name=form.name.data)
        hero.save()
        car = CarDB()
        car.save()
        m1 = MarketDB()
        m1.save()
        m2 = MarketDB()
        m2.save()
        m = [m1,m2]
        house = HouseDB(markets=m)
        house.save()
        contract = ContractDB()
        contract.save()
        job = JobDB()
        job.save()
        hero.update(car=car,house=house,job=job,contract=contract)

    return render_template('dreamcar/admin/add_hero.html', form=form)
