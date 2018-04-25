from app import db

class Pictures(db.Document):
    filename = db.StringField(max_length=60)
    description = db.StringField(max_length=255)
    time = db.DateTimeField()
    place = db.StringField(max_length=20)
    tags = db.ListField(db.StringField(max_length=60))
    direction = db.StringField(max_length=10)
