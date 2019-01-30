from app import db
from random import randint
from math import log

class JobDB(db.document):
    salary = db.IntField()
    ring = db.IntField()
    mood = db.IntField()

class Job(object):
    def __init__(self, salary=None, ring=None):
        self.salary = salary or self.new_salary()
        self.ring = ring or self.new_ring()
        self.mood = self.resolve_mood()

    @staticmethod
    def factory():
        r = randint(1,10)
        if r>9:
            return JobGood()
        elif r>4:
            return JobNormal()
        else:
            return JobPoor()

    def new_salary(self):
        pass

    def new_ring(self):
        pass

    def resolve_mood(self):
        return 0 - int(log(self.salary, 10000)*100)%100

class JobGood(Job):
    def new_salary(self):
        return 30000+randint(0,10)*5000

    def new_ring(self):
        return randint(0,4)

class JobNormal(Job):
    def new_salary(self):
        return 10000+randint(0,10)*2000

    def new_ring(self):
        return randint(4,8)

class JobPoor(Job):
    def new_salary(self):
        return 10000-randint(0,5)*500

    def new_ring(self):
        return randint(6,13)
