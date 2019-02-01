from app import db
from random import choice, randint
from math import pow

PERCENT = [0.3,0.4,0.5,0.6,1.0]
TOTAL_AGE = [12,24,36,60]


class ContractDB(db.Document):
    pre = db.IntField(default=0)
    sum = db.IntField(default=0)
    total_age = db.IntField(default=1)
    age = db.IntField(default=0)
    paid = db.BooleanField(default=True)

class Contract(object):
    def __init__(self, db=None, pre=None, sum=None, total_age=None, age=None, paid=False):
        self.db = db
        self.pre = pre
        self.sum = sum
        self.total_age = total_age
        self.age = age
        self.paid = paid
        self.rest = None
        self.monthly = None

    def from_db(self, db):
        self.db = db
        self.pre = self.db.pre
        self.sum = self.db.sum
        self.total_age = self.db.total_age
        self.age = self.db.age
        self.paid = self.db.paid
        self.rest = self.money_pay_early()
        self.monthly = self.month_expense()

    @classmethod
    def factory(cls, car):
        sum = car.price
        percent = choice(PERCENT)
        if percent == 1.0:
            total_age = 0
            paid = True
        else:
            total_age = choice(TOTAL_AGE)
        pre = sum * percent
        rest = sum - pre
        rate = randint(5,8)*0.01
        rest = int(rest*pow((1+rate),total_age/12))
        return cls(pre=pre,sum=sum,total_age=total_age,age=0,paid=paid)

    def month_expense(self):
        return self.rest / (self.total_age - self.age)

    def money_pay_early(self):
        rest = self.sum - self.pre
        rest = int(rest*self.age/12)
        return rest
