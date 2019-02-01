from app import db
from random import randint

class MarketDB(db.Document):
    cost = db.IntField(default=0)
    health = db.IntField(default=0)
    distance = db.IntField(default=0)

class Market(object):
    def __init__(self, cost=None, health=None, distance=None):
        self.cost = cost or self.new_cost()
        self.health = health or self.new_health()
        self.distance = distance or self.new_distance()

    @staticmethod
    def factory():
        r = rand(1,10)
        if r>7:
            return MarketGood()
        elif r>4:
            return MarketNormal()
        else:
            return MarketPoor()

    def new_cost(self):
        pass

    def new_health(self):
        pass

    def new_distance(self):
        return randint(1,4)

class MarketGood(Market):
    def new_cost(self):
        return 5000 + randint(-6,6) * 500

    def new_health():
        return randint(0,5)

class MarketNormal(Market):
    def new_cost(self):
        return 1000 + randint(-5,5)*100

    def new_health(self):
        return randint(-1,3)

class MarketPoor(Market):
    def new_cost(self):
        return 300 + randint(-5,5)*50

    def new_health(self):
        return randint(-3,1)
