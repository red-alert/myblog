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

@app.route('/')
@app.route('/index')
@cache.cached(timeout=300)
def index():
    pictures = Picture.objects()
    carousel_picutres = pictures.order_by('-create_time')[:3]
    print(pictures)
    return render_template('index.html', pictures=pictures, carousel_pictures=carousel_picutres)

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
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('upload')
            return redirect(next_page)
        return redirect(url_for('index'))
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

@app.route('/pictures/<filename>')
def serve_pictures(filename):
    return send_from_directory(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER']), filename)

@app.route('/static/<filename>')
def serve_static_files(filename):
    return send_from_directory(os.path.join(app.config['APP_DIR'], app.config['STATIC']), filename)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
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
            picture = Picture(filename=filename, description=form.description.data, shot_time=form.shot_time.data, place=form.place.data, tags=form.tags.data)
            picture.save()
            f= form.file.data
            print(f)
            f.save(os.path.join(app.config['APP_DIR'], app.config['UPLOAD_FOLDER'], filename))
            flash('Newpicture uploaded!')
            return redirect(url_for('upload', filename=filename))
    return render_template('upload.html', title='Upload', form=form)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
