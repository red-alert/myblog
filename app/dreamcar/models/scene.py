from app.dreamcar.models.event import Event


class Scene(object):
    def __init__(self,hero=None,story=None,options=None,message=None, event=None):
        self.hero = hero
        self.story = story
        self.message = message
        self.options = options
        self.event = event
        self.init()

    def init(self):
        self.event = Event.factory(self.hero)
        self.story = self.event.story
        self.options = self.event.options
        self.message = self.event.message

    def factory(self):
        pass

    def update(self,choice):
        self.event.run(choice)
        self.init()
