#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_script import Manager
from flask_script import Shell

from models import db, User
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

manager = Manager(app)

def migrate():
    pass

def console():
    return dict(app=app, db=db, User=User)


@app.route('/', methods=['GET'])
def index():
    return "Index"


manager.add_command('console', Shell(make_context = console))

if __name__ == "__main__":
    db.init_app(app)

    with app.app_context():
        db.create_all()

    manager.run()


    