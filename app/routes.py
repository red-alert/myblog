import os
from app import app
from app import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask import request
from flask import send_from_directory
from app.models import Picture, User
from app.forms import LoginForm, PictureForm, RegistrationForm
from flask_login import current_user, login_user, login_required, logout_user
from app import cache
from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse
from PIL import Image
from collections import defaultdict

@app.route('/')
@app.route('/index')
@cache.cached(timeout=5)
def index():
    pictures = Picture.objects().order_by('-shot_time')
    carousel_pictures = pictures.order_by('-create_time')[:3]
    return render_template('index.html', pictures=pictures, carousel_pictures=carousel_pictures)

@app.route('/about')
def about():
    pictures = Picture.objects()
    carousel_pictures = pictures.order_by('-create_time')[:3]
    return render_template('about.html', carousel_pictures=carousel_pictures)

@app.route('/pictures_by_year')
def pictures_by_year():
    pictures = Picture.objects().order_by('-shot_time')
    year = 0
    pictures_by_year = defaultdict(list)
    for picture in pictures:
        year = picture.shot_time.year
        print(year)
        pictures_by_year[year].append(picture)
    return render_template('pictures_by_year.html', pictures_by_year=pictures_by_year)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        print(user.username)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        # next_page = request.args.get('next')
        # if not next_page or url_parse(next_page).netloc != '':
        #     next_page = url_for('index')
        #     return redirect(next_page)
        return redirect(url_for('upload'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirct(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        user.save()
        flash('You are now registered')
        return redirect(url_for('index'))
    return render_template('register.html', title='Register', form=form)

@app.route('/pictures/<path:filename>')
def serve_pictures(filename):
    return send_from_directory(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER']), filename)

@app.route('/static/<path:filename>')
def serve_static_files(filename):
    return send_from_directory(os.path.join(app.config['APP_DIR'], app.config['STATIC']), filename)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if current_user.is_authenticated:
        form = PictureForm()
        if form.validate_on_submit():
        # if request.method == 'POST':
            if 'file' not in request.files:
                flash('No File!')
                return redirect(url_for('upload'))
            if form.file.data.filename == '':
                flash('No Selected File!')
                return redirect(url_for('upload'))
            if form.file and allowed_file(form.file.data.filename):
                filename = secure_filename(form.file.data.filename)
                extension = filename.rsplit('.', 1)[1].lower()
                picture = Picture(extension=extension, description=form.description.data, shot_time=form.shot_time.data, place=form.place.data, tags=form.tags.data)
                picture.save()
                unified_filename = str(picture.id) + '.' + extension
                f = form.file.data
                picture_handler(f, unified_filename)
                flash('New picture uploaded!')
                return redirect(url_for('upload'))
        return render_template('upload.html', title='Upload', form=form)
    else:
        return redirect(url_for('login'))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def picture_handler(picture, filename):
    picture = Image.open(picture)
    width = picture.width
    height = picture.height
    if width > height:
        new_width = int(width / height * 1080)
        new_height = 1080
        left = int((new_width - new_height)/2)
        top = 0
        right = int((new_width + new_height)/2)
        bottom =1080
    else:
        new_height = int(height / width * 1080)
        new_width = 1080
        left = 0
        top = int((new_height-new_width)/2)
        right = 1080
        bottom = int((new_width+new_height)/2)
    box = (left, top, right, bottom)
    resized_picture = picture.resize((new_width,new_height))
    croped_picture = resized_picture.crop(box)
    croped_picture = croped_picture.resize((500,500))

    picture.save(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER'], 'origin', filename))
    resized_picture.save(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER'], 'resized', filename))
    croped_picture.save(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER'], 'thumbnail', filename))

    return print("picture successfully handeled")
