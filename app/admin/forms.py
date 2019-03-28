from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed, DataRequired
from wtforms import StringField,TextAreaField, DateField, SubmitField
from wtforms import RadioField, SelectField, SelectMultipleField

from flask import current_app

tag_choices = [('none', 'None'),
               ('mountain', '高山'),
               ('water', '流水'),
               ('things', '万物'),
               ('people', '人间'),
               ('me', '我')]
file_allowed = current_app.config['ALLOWED_EXTENSIONS']

class MultiCheck(object):
    def __call__(self, field, **kwargs):
        field_id = kwargs.pop('id', field.id)
        html = [u'']
        html.append(u'<table>')

        for value, label in field.iter_choices():
            html.append(u'<tr>\n')
            html.append(u'<td><input type="checkbox" name="%s" value="%s"/></td>\n' % (field_id, value))
            html.append(u'<td><img class="mini-img" src="../static/pictures/thumbnail/%s" /></td></tr>\n' % label )
        html.append(u'</table>\n')
        return u''.join(html)

class MultiPicField(SelectMultipleField):
    widget = MultiCheck()

class FileInput(object):
    """
    Renders a file input chooser field.
    """

    def __call__(self, field, **kwargs):
        kwargs.setdefault('id', field.id)
        html = [u'']
        html.append('<input name="%s" type="file", multiple="multiple">' % field.name)
        return u''.join(html)

class MultipleFileField(FileField):
    widget = FileInput()

class PictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    file = FileField('File', validators=[FileRequired(),
                     FileAllowed(file_allowed)])
    submit = SubmitField('upload')

class EditPictureForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    shot_time = DateField('shot_time', validators=[])
    place = StringField('place', validators=[])
    tags = SelectField(choices=tag_choices, validators=[DataRequired()])
    submit = SubmitField('Update') # handle update function
    delete = SubmitField('Delete') # handle delete function

class GalleryForm(FlaskForm):
    name = StringField('name')
    description = TextAreaField('description')
    photos = MultipleFileField('photos')
    submit = SubmitField('upload')

class DeletePhotoForm(FlaskForm):
    photos = SelectMultipleField('photos')
    delete = SubmitField('Delete')

class VideoForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    url = TextAreaField('url', validators=[DataRequired()])
    submit = SubmitField('submit')

class EditVideoForm(FlaskForm):
    description = TextAreaField('description', validators=[DataRequired()])
    url = TextAreaField('url', validators=[DataRequired()])
    submit = SubmitField('update')
    delete = SubmitField('delete')
