from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User, Picture
from app import app

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class PictureForm(FlaskForm):
    description = TextAreaField('description', validators=[Length(min=0, max=255)])
    shot_time = StringField('shot time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=['高山', '流水', '万物', '人间', '我'], validators=[DataRequired()])
    direction = RadioField(choices=['Vertical', 'Horizontal'], validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
