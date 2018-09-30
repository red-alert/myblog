from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, request, flash
from flask import current_app
from flask_login import login_required
from app.admin import bp
from app.models import Picture
from app.admin.forms import EditPictureForm, PictureForm
from app.admin.handler import picture_handler, picture_remover

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PictureForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No File!')
            return redirect(url_for('admin.upload'))
        if form.file.data.filename == '':
            flash('No Selected File!')
            return redirect(url_for('admin.upload'))
        if form.file and allowed_file(form.file.data.filename):
            filename = secure_filename(form.file.data.filename)
            extension = filename.rsplit('.', 1)[1].lower()
            picture = Picture(extension=extension,
                              description=form.description.data,
                              shot_time=form.shot_time.data,
                              place=form.place.data,
                              tags=form.tags.data)
            picture.save()
            unified_filename = str(picture.id) + '.' + extension
            f = form.file.data
            try:
                picture_handler(f, unified_filename)
            except:
                print("picture file may not be updated")
            flash('New picture uploaded!')
            return redirect(url_for('admin.upload'))
    return render_template('admin/upload.html', title='Upload', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in \
                current_app.config['ALLOWED_EXTENSIONS']

@bp.route('/edit_pictures')
@login_required
def edit_pictures():
    """
    list all photos ordered by create time
    """
    pictures = Picture.objects.order_by('-create_time')
    return render_template('admin/edit_pictures.html', pictures=pictures)

@bp.route('/edit_pictures/<id>', methods=['GET', 'POST'])
@login_required
def edit_picture(id):
    picture = Picture.objects.get(id=id)
    form = EditPictureForm(description=picture.description,
                           shot_time=picture.shot_time,
                           place=picture.place,
                           tags=picture.tags)
    if form.validate_on_submit():
        if form.delete.data:
            try:
                picture_remover(picture)
            except:
                print("image file removing unsuccessully, try manual")
            picture.delete()
            flash('picture deleted')
            return redirect(url_for('admin.edit_pictures'))
        picture.description = form.description.data
        picture.shot_time = form.shot_time.data
        picture.place = form.place.data
        picture.tags = form.tags.data
        picture.save()
        flash('picture info updated')
        return redirect(url_for('admin.edit_pictures'))
    return render_template('admin/edit_picture.html', form=form, picture=picture)
