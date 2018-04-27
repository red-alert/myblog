from app import app
from app import db

from flask import render_template, flash, redirect, url_for
from flask import request
from app.models import Picture, User
from datetime import datetime

from werkzeug.utils import secure_filename

@app.route('/')
@app.route('/index')
def index():
    return "Hello world!"

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File!')
            return redirect(url_for(''))
        if file.filename == '':
            flash('No Selected File!')
            return redirect(url_for(''))
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(rul_for('upload_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

def allowed_file(filename):
    return '.' in filename and fsilename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']
