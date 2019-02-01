from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class HeroForm(FlaskForm):
    name = StringField('name', validators=[])
    submit = SubmitField('确定')

class EventForm(FlaskForm):
    pass
