from app import db
from app import login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class Picture(db.Document):
    extension = db.StringField(max_length=4)
    description = db.StringField()
    shot_time = db.DateTimeField()
    create_time = db.DateTimeField(default=datetime.utcnow())
    place = db.StringField(max_length=255)
    tags = db.StringField(max_length=60)

    # filename = db.StringField(max_length=60)
    # direction = db.StringField(max_length=10)

    def __repr__(self):
        return '<Picture {}>'.format(self.id)

class User(UserMixin, db.Document):
    username = db.StringField(max_length=60)
    password_hash = db.StringField(max_length=128)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(user_id):
    print("hello %s" % user_id)
    user = User.objects(id=user_id)[0]
    return user
