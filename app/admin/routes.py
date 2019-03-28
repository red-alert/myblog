from werkzeug.utils import secure_filename
from flask import render_template, redirect, url_for, request, flash
from flask import current_app
from flask_login import login_required
from app.admin import bp
from app.models import Picture, Gallery, Photo, Video
from app.admin.forms import EditPictureForm, PictureForm, VideoForm, EditVideoForm, GalleryForm, DeletePhotoForm
from app.admin.handler import picture_handler, picture_remover

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PictureForm()
    if form.validate_on_submit():
        if 'file' not in request.files:
            flash('No File!')
            return redirect(url_for('upload'))
        if form.file.data.filename == '':
            flash('No Selected File!')
            return redirect(url_for('upload'))
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

@bp.route('/add_gallery', methods=['GET', 'POST'])
@login_required
def add_gallery():
    form = GalleryForm()
    if form.validate_on_submit():
        if request.files.getlist('photos'):
            ps = []
            for file in request.files.getlist('photos'):
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    photo = Photo(extension=extension)
                    photo.save()
                    ps.append(photo)
                    unified_filename = str(photo.id) + '.' + extension
                    f = file
                    try:
                        picture_handler(f, unified_filename)
                    except:
                        print("picture file may not be updated")
                    flash('New picture uploaded!')
            gallery = Gallery(name = form.name.data, description=form.description.data, photos=ps)
            gallery.save()
            return redirect(url_for('main.galleries'))
    return render_template('admin/add_gallery.html', title='Create Gallery', form=form)

@bp.route('/edit_gallery/<id>', methods=['GET', 'POST'])
@login_required
def edit_gallery(id):
    gallery = Gallery.objects.get(id=id)
    form = GalleryForm(name=gallery.name, description=gallery.description)
    if form.validate_on_submit():
        if request.files.getlist('photos'):
            ps = gallery.photos
            for file in request.files.getlist('photos'):
                print(dir(file))
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    extension = filename.rsplit('.', 1)[1].lower()
                    photo = Photo(extension=extension)
                    photo.save()
                    ps.append(photo)
                    unified_filename = str(photo.id) + '.' + extension
                    f = file
                    try:
                        picture_handler(f, unified_filename)
                    except:
                        print("picture file may not be updated")
                    flash('New picture uploaded!')
            gallery.photos = ps
        gallery.name = form.name.data
        gallery.description = form.description.data
        gallery.save()
        return redirect(url_for('main.galleries'))
    return render_template('admin/add_gallery.html', title='Create Gallery', form=form)

@bp.route('/delete_from_gallery/<id>', methods=['GET','POST'])
@login_required
def delete_from_gallery(id):
    gallery = Gallery.objects.get(id=id)
    form = DeletePhotoForm()
    choices = []
    for photos in gallery:
        choice = (str(photo.id), '.'.join([str(photo.id), str(photo.extension)]))
        choices.append(choice)
    form.photos.choices = choices
    if form.validate_on_submit():
        photos = form.photos.data
        for photo in photos:
            p_obj = Photo(id=photo)
            try:
                picture_remover(p_obj)
            except:
                print("image file removing unsuccessully, try manual")
            p_obj.delete()
        return redirect(url_for('admin.edit_galleries'))
    return render_template('admin/delete_from_gallery.html', form=form)

@bp.route('/add_video', methods=['GET', 'POST'])
@login_required
def add_video():
    form = VideoForm()
    if form.validate_on_submit():
        video = Video(description=form.description.data, url=form.url.data)
        video.save()
        return redirect(url_for('main.videos'))
    return render_template('admin/add_video.html', form=form)

@bp.route('/edit_video/<id>', methods=['GET', 'POST'])
@login_required
def edit_video(id):
    video = Video.objects.get(id=id)
    form = EditVideoForm(description=video.description, url=video.url)
    if form.validate_on_submit():
        if form.delete.data:
            video.delete()
            return redirect(url_for('main.videos'))
        video.description = form.description.data
        video.url = form.url.data
        video.save()
        return redirect(url_for('main.videos'))
    return render_template('admin/edit_video.html', form=form)
