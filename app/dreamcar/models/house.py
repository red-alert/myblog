from app import db
from random import randint
from math import log

from app.dreamcar.models.market import MarketDB

class HouseDB(db.document):
    rent = db.IntField()
    ring = db.IntField()
    mood = db.IntField()
    market = db.LazyReferenceField(MarketDB)

class House(object):
    def __init__(self, rent=None, ring=None):
        self.ring = ring or self.new_ring()
        self.rent = rent or self.new_rent()
        self.mood = self.resolve_mood()

    @staticmethod
    def factory():
        r = randint(1,10)
        if r>9:
            return HouseGood()
        elif r>5:
            return HouseNormal()
        else:
            return HousePoor()

    def new_rent(self):
        pass

    def new_ring(self):
        pass

    def resolve_mood(self):
        return 8 - self.ring

class HouseGood(House):
    def new_rent(self):
        return 20000 - self.ring*2000 + randint(-5,5)*1000

    def new_ring(self):
        return randint(0,5)

class HouseNormal(House):
    def new_ring(self):
        return randint(4,8)

    def new_rent(self):
        return 15000 - self.ring*1000 + randint(-5,5)*500

class HousePoor(House):
    def new_ring(self):
        return randint(6,13)

    def new_rent(self):
        return 10000 - self.ring*500 + randint(-5,5)*300
