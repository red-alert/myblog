import os
from flask import current_app
from PIL import Image

def picture_handler(picture, filename):
    """
    resize uploaded photos to a reasonable size
    and save to local file system
    """
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
    resized_picture = picture.resize((new_width,new_height), Image.ANTIALIAS)
    croped_picture = resized_picture.crop(box)
    croped_picture = croped_picture.resize((500,500))

    picture.save(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'origin', filename))
    resized_picture.save(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'resized', filename))
    croped_picture.save(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'thumbnail', filename))

    return print("picture successfully handled")

def picture_remover(picture):
    """
    remove photo from file system
    """
    os.remove(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'origin', str(picture.id)+'.'+picture.extension))
    os.remove(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'resized', str(picture.id)+'.'+picture.extension))
    os.remove(os.path.join(current_app.config['APP_DIR'], current_app.config['UPLOAD_FOLDER'], 'thumbnail', str(picture.id)+'.'+picture.extension))

    return print("picture file removed")
