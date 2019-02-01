import pdb

from app import db

from app.dreamcar.models.option import OptionDB, Option
from app.dreamcar.models.contract import Contract, ContractDB

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
        if choice == "garage":
            self.story = "车行里停着两辆车："
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 5
            self.hero.update()
        elif choice == "house":
            self.story = "你找到两处出租的房子："
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 4
            self.hero.update()
        elif choice == "contract":
            self.hero.last_scene = self.hero.scene
            self.hero.scene = 6
            self.hero.update()
        elif choice in ['0','1','2']:
            self.option_processor(self.options[int(choice)])
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
    pass

class EventTwo(Event):
    pass

class EventThree(Event):
    pass

class EventHouse(Event):
    pass

class EventGarage(Event):
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
