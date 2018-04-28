from app import app
from app import db
from datetime import datetime
from flask import render_template, flash, redirect, url_for
from flask import request
from app.models import Picture, User
from app.forms import LoginForm, PictureForm

from flask_login import current_user, login_user, login_required, logout_user

from werkzeug.utils import secure_filename
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
def index():
    pictures = Picture.objects()
    context = {}
    return render_template('index.html', pictures=pictures)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects.get(username=form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirct(url_for('index'))

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = PictureForm()
    if form.validate():
    # if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File!')
            return redirect(url_for('upload.html'))
        if file.filename == '':
            flash('No Selected File!')
            return redirect(url_for(''))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            picture = Picture(filename=filename, description=form.description.data, shot_time=form.shot_time.data, place=form.place.data, tags=form.tags.data, direction=form.direction.data)
            picture.save()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Newpicture uploaded!')
            return redirect(rul_for('upload', filename=filename))
    return render_template('upload.html', form=form)

def allowed_file(filename):
    return '.' in filename and fsilename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
