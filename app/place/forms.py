from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

class TestForm(FlaskForm):
    x = StringField('x', validators=[])
    y = StringField('y', validators=[])
    color = StringField('color', validators=[])
    submit = SubmitField('submit')
