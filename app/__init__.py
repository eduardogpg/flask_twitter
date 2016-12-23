#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CsrfProtect
from flask_login import LoginManager

from bootstrap import bootstrap_message

__author__ = 'Eduardo Ismael García Pérez'

db = SQLAlchemy()
csrf = CsrfProtect()
login = LoginManager()
	
def create_app(config_class):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	login.init_app(app)
	csrf.init_app(app)

	login.login_view = 'login'
	login.login_message = bootstrap_message("Es necesario que te iniciar sesion", "warning")
	
	return app