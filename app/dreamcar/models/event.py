import pdb

from app import db

from app.dreamcar.models.option import OptionDB, Option
from app.dreamcar.models.contract import Contract, ContractDB
from app.dreamcar.models.car import Car, CarDB
from app.dreamcar.models.house import House, HouseDB

from flask import render_template

COLOR_FONT = {"up": "<b>增加 </b>",
              "down": "<b>减少 </b>"}

class EventDB(db.Document):
    name = db.StringField()
    story = db.StringField()
    options = db.ListField(db.LazyReferenceField(OptionDB))

class Event(object):
    def __init__(self, hero=None):
        self.hero = hero
        self.story = None
        self.options = None
        self.message = None

    def run(self,choice):
        print(self.options)
        if choice == "garage":
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 5
            self.hero.update()
        elif choice == "house":
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 4
            self.hero.update()
        elif choice == "contract":
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 6
            self.hero.update()
        elif choice in ['0','1','2']:
            self.option_processor(self.options[choice])
        else:
            self.hero.scene = 0
            self.hero.update()

    @staticmethod
    def factory(hero):
        if hero.scene == 1:
            return EventOne(hero=hero) # 看病  上班
        elif hero.scene == 2:
            return EventTwo(hero=hero) # 随机事件
        elif hero.scene == 3:
            return EventThree(hero=hero) # 超市消费
        elif hero.scene == 4:
            return EventHouse(hero=hero) # 链家
        elif hero.scene == 5:
            return EventGarage(hero=hero) # 车行
        elif hero.scene == 6:
            return EventContract(hero=hero) # 查看贷款
        elif hero.scene == 7:
            return EventFinal(hero=hero) # 游戏结局
        elif hero.scene == 8:
            return EventJob(hero=hero) # 找工作
        else:
            return EventInit(hero=hero) # 游戏开始

    def message_generator(self, option):
        results = option.results
        messages = []
        for key,value in results.items():
            if key == "extra":
                messages.append(value)
            if key == "health" and value!=0:
                messages.append("健康"+self.value_to_expression(value))
            if key == "mood" and value != 0:
                messages.append("心情"+self.value_to_expression(value))
            if key == "saving" and value != 0:
                messages.append("积蓄"+self.value_to_expression(value)+"￥"+str(value))
        return render_template("dreamcar/messages.html",messages)

    def value_to_expression(self,value):
        if value > 0:
            return COLOR_FONT["up"]
        else:
            return COLOR_FONT["down"]

    def option_processor(self, option):
        pass

class EventOne(Event):
    def __init__(self,hero):
        super().__init__()
        self.story = "新的一个月开始了"
        self.hero = hero
        self.options = []
        job = self.hero.job.fetch()
        house = self.hero.house.fetch()
        car = self.hero.car.fetch()
        if car.have:
            car_mood = car.mood
        else: car_mood = 0
        if hero.health < 50:
            self.options.append(Option(choice_message="医院看病，然后上班", results={"health":40,"mood":car_mood+house.mood+job.mood,"saving":0-100*(100-self.health)}))
        else: pass
        if hero.mood < 0:
            self.options.append(Option(choice_message="请假一个月去玩", results={"mood":50, "saving":0-2*job.salary}))
        else: pass
        self.options.append(Option(choice_message="开车上班", results={"mood":car_mood+house.mood+job.mood}))

    def option_processor(self,option):
        self.hero.scene = 2
        option = option
        print("before")
        helper(self.hero, option)
        self.message = "test"
        self.hero.update()

class EventTwo(Event):
    pass

class EventThree(Event):
    pass

class EventHouse(Event):
    pass

class EventGarage(Event):
    def __init__(self, hero):
        self.hero = hero
        car1 = Car.factory()
        car2 = Car.factory()
        self.message = None
        self.story = "今天车行出售2台车"
        a = Option(choice_message="1号车"+"总价:"+str(car1.price/10000)+"万", results={"car":"get"})
        b = Option(choice_message="2号车"+"总价:"+str(car2.price/10000)+"万", results={"car":"get"})
        c = Option(choice_message="摸了摸干瘪的钱包，下次再来吧", results={})
        self.options = [a,b,c]

    def option_processor(self, option):
        pass

class EventContract(Event):
    def __init__(self,hero):
        self.hero = hero
        contract = Contract()
        contract.from_db(self.hero.contract.fetch())
        # pdb.set_trace()
        self.message = None
        if contract.paid is not True:
            self.story = "你手上的买车合同：总价：" + \
                         str(contract.sum) + \
                         "，贷款本息:" + \
                         str(contract.sum-contract.pre) + \
                         "元，总期：" + str(contract.total_age) + \
                         "，当前：" + str(contract.age)
            a = Option(choice_message="提前还款",results={"saving":(0-contract.money_pay_early())})
            b = Option(choice_message="算了",results={})
            self.options = [a, b]
            # import pdb; pdb.set_trace()
        else:
            self.story = "你没有任何欠钱的买车合同"

    def option_processor(self, option):
        self.hero.scene = self.hero.last_scene
        option = option
        helper(self.hero, option)
        self.hero.update()

class EventFinal(Event):
    pass

class EventInit(Event):
    pass


def helper(hero, option):
    hero = hero
    results = option.results
    for key,value in results.items():
        print(results.items())
        if key == "health":
            hero.health += value
        if key == "mood":
            hero.mood += value
        if key == "saving":
            hero.saving += value
        if key == "girl":
            hero.girl = value
        if key == "house":
            getattr(House, value)(hero)
        if key == "job":
            getattr(Job, value)(hero)
        if key == "car":
            getattr(Car, value)(hero)
        if key == "contract":
            getattr(Contract, value)(hero)
