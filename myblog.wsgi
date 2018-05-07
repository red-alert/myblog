#!/usr/bin/python

import sys
activate_this = '/var/www/myblog/venv/bin/activate_this.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))
print("activated!")
print(sys.path)
sys.path.insert(0, '/var/www/myblog/')

from app import app as application
application.secret_key = 'you will never guess!'
