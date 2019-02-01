from app import db
from random import randint
from math import pow

class CarDB(db.Document):
    price = db.IntField(default=0)
    age = db.IntField(default=0)
    mood = db.IntField(default=0)
    have = db.BooleanField(default=False)

class Car(object):
    def __init__(self):
        self.price = self.new_price()
        self.age = 0
        self.mood = self.resolve_mood()

    @staticmethod
    def factory():
        r = randint(1,10)
        if r>7:
            return CarGood()
        elif r>3:
            return CarNormal()
        else:
            return CarPoor()

    def new_price(self):
        pass

    def now_price(self):
        return self.price / (0.2 * self.age)

    def resolve_mood(self):
        if self.price > 500000:
            t = 10
        else:
            t = int(self.price*pow(0.8,self.age))
        return 5-self.age + t

    @staticmethod
    def get(hero): # 买车
        pass

    @staticmethod
    def sell(hero): # 卖车
        pass

    @staticmethod
    def destroy(hero): # 车消失
        pass

class CarGood(Car):
    def new_price(self):
        return 3000000 + randint(-10,10) * 200000

class CarNormal(Car):
    def new_price(self):
        return 600000 + randint(-20,20) * 30000

class CarPoor(Car):
    def new_price(self):
        return 100000 + randint(-10,10) * 5000
