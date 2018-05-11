from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Length
from app.models import User, Picture
from app import app

tag_choices = [('none', 'None'), ('mountain', '高山'), ('water', '流水'), ('things', '万物'), ('people', '人间'), ('me', '我')]

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign in')

class PictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    # direction = RadioField(choices=[('vertical', 'Vertical'), ('horizontal', 'Horizontal')], validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(), FileAllowed(app.config['ALLOWED_EXTENSIONS'])])
    submit = SubmitField('Upload')

class EditPictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot_time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    submit = SubmitField('Update') # handle update function
    delete = SubmitField('Delete') # handle delete function
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    password2 = PasswordField('password2', validators=[DataRequired()])
    submit = SubmitField('register')
