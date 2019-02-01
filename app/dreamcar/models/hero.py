from app import db
from app.dreamcar.models.job import JobDB
from app.dreamcar.models.house import HouseDB
from app.dreamcar.models.car import CarDB
from app.dreamcar.models.contract import ContractDB

HEALTH = {"0":"好极了",
          "1":"很一般",
          "2":"不舒服",
          "3":"很难受",
          "4":"糟透了",
          "5":"死掉了",
          "6":""}
MOOD = {"0":"非常开心", # 100 - 80
        "1":"开心", # 80 - 30
        "2":"说不上开心", # 30 - 0
        "3":"不开心", # 0 - -20
        "4":"抑郁", # -20 - -70
        "5":"抑郁到了极点", # -70 -
        "6":""}

class HeroDB(db.Document):
    name = db.StringField()
    health = db.IntField(default=100)
    mood = db.IntField(default=0)
    year = db.IntField(default=0)
    month = db.IntField(default=0)
    saving = db.IntField(default=0)
    girl = db.BooleanField(default=False)
    house = db.LazyReferenceField(HouseDB)
    job = db.LazyReferenceField(JobDB)
    car = db.LazyReferenceField(CarDB)
    contract = db.LazyReferenceField(ContractDB)
    scene = db.IntField(default=0)
    last_scene = db.IntField(default=0)

class Hero(object):
    def __init__(self, id, db=None, name=None,health=100,mood=0,year=0,month=0,saving=0,girl=False,house=None,job=None,car=None,contract=None, scene=None, last_scene=None):
        self.id = id
        self.db = db
        self.name = name
        self.health = health
        self.mood = mood
        self.year = year
        self.month = month
        self.saving = saving
        self.girl = girl
        self.house = house
        self.job = job
        self.car = car
        self.contract = contract
        self.scene = scene
        self.last_scene = last_scene
        self.init(id=self.id)

    def init(self, id):
        self.db = HeroDB.objects.get(id=id)
        self.name = self.db.name
        self.health = self.db.health
        self.mood = self.db.mood
        self.year = self.db.year
        self.month = self.db.month
        self.saving = self.db.saving
        self.girl = self.db.girl
        self.house = self.db.house
        self.job = self.db.job
        self.car = self.db.car
        self.contract = self.db.contract
        self.scene = self.db.scene
        self.last_scene = self.db.last_scene

    def update(self):
        self.db.update(name=self.name, health=self.health, mood=self.mood, \
                       year=self.year, month=self.month, saving=self.saving, \
                       girl=self.girl, house=self.house,  job=self.job, car=self.car, \
                       contract=self.contract, scene=self.scene, last_scene=self.last_scene)

    def __str__(self):
        return "Hero[{0}]:{1} {2} {3} {4} {5} {6} {7}".format(str(self.id), self.name, self.year, self.month, self.saving, self.get_mood(), self.get_health(), self.db)

    def get_health(self):
        if self.health > 100:
            self.health = 100
            self.save()
            return self.get_health()
        if self.health > 90:
            return HEALTH["0"]
        elif self.health > 15:
            return HEALTH["1"]
        elif self.health > -5:
            return HEALTH["2"]
        elif self.health > -30:
            return HEALTH["3"]
        elif self.health > -60:
            return HEALTH["4"]
        else:
            return HEALTH["5"]

    def get_mood(self):
        if self.mood > 100:
            self.mood = 100
            self.save()
            return self.get_mood()
        if self.mood > 80:
            return MOOD["0"]
        elif self.mood > 30:
            return MOOD["1"]
        elif self.mood > 0:
            return MOOD["2"]
        elif self.mood > -20:
            return MOOD["3"]
        elif self.mood > -70:
            return MOOD["4"]
        else:
            return MOOD["5"]

    def month_expense(self):
        pass

    def grow_old(self):
        self.month += 1
        if self.month > 12:
            self.year += 1
            self.month -=12
