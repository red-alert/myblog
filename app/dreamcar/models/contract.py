from app import db
from random import choice, randint
from math import pow

PERCENT = [0.3,0.4,0.5,0.6,1.0]
TOTAL_AGE = [12,24,36,60]


class ContractDB(db.document):
    pre = db.IntField()
    sum = db.IntField()
    total_age = db.IntField()
    age = db.IntField()
    paid = db.BooleanField(default=False)

class Contract(object):
    def __init__(self, pre=None, sum=None, rest=None, total_age=None, age=None, paid=False):
        self.pre = pre
        self.sum = sum
        self.rest = rest
        self.total_age = total_age
        self.age = age
        self.paid = paid
        self.month_expense = self.resolve_expense

    @classmethod
    def factory(cls, car=car):
        sum = car.price
        percent = choice(PERCENT)
        if percent = 1.0
            total_age = 0
        else:
            total_age = choice(TOTAL_AGE)
        pre = sum * percent
        rest = sum - pre
        rate = randint(5,8)*0.01
        rest = int(rest*pow((1+rate),total_age/12))
        return cls()

    def month_expense(self):
        return self.rest / (self.total_age - self.age)

    def money_pay_early(self):
        rest = self.sum - self.pre
        rest = int(rest*pow((1+rate),age/12))
        return rest
