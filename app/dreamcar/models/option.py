from app import db

class OptionDB(db.Document):
    choice = db.StringField()
    results = db.DictField()

# ```
# choice = "short story here"
# results = {
#     "health": , +-int
#     "mood": , +-int
#     "saving": , +-int
#     "girl": , // "get" or "lose"
#     "house": , // "raise_rent"
#     "job": , // "get" "lose" "raise_salary"
#     "car": , // "get" "sell" "destroy"
#     "contract":, //"get" "payoff"
#     "extra": ,
#     "next":
# }
# ```

class Option(object):
    def __init__(self, choice_message=None, results=None):
        self.db = None
        self.choice_message = choice_message
        self.results = results
