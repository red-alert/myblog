from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired
from wtforms import StringField,TextAreaField, DateField, SubmitField
from wtforms import RadioField, SelectField
from flask import current_app

tag_choices = [('none', 'None'),
               ('mountain', '高山'),
               ('water', '流水'),
               ('things', '万物'),
               ('people', '人间'),
               ('me', '我')]
file_allowed = current_app.config['ALLOWED_EXTENSIONS']

class PictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(),
                     FileAllowed(file_allowed)])
    submit = SubmitField('Upload')

class EditPictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot_time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    submit = SubmitField('Update') # handle update function
    delete = SubmitField('Delete') # handle delete function
