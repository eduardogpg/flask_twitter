#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask_wtf.csrf import CsrfProtect

from bootstrap import *

from config import DevelopmentConfig
from models import db, User

from forms import RegistrationForm
from forms import LoginForm
from forms import EditUser

import flask_login

app = Flask(__name__)
csrf = CsrfProtect()
login_manager = flask_login.LoginManager()

app.config.from_object(DevelopmentConfig)
#https://flask-login.readthedocs.io/en/latest/ <--- Doc Login

__author__ = 'Eduardo Ismael García Pérez'

def authenticated(func):
	def new_function(*args, **kwargs):
		if flask_login.current_user is not None:
			return redirect(url_for('protected'))
		else:
			return func(*args, **kwargs)
	return new_function


@login_manager.user_loader
def user_loader(user_id):
	return User.find(user_id)

@app.errorhandler(404)
def not_found(error):
	return "Not Found."

@app.route('/register', methods=['GET', 'POST'])
@authenticated
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User.new(username = form.username.data, password = form.password.data, email = form.email.data)
		if user.save():
				add_success_message("Usuario registrado exitosamente.")
		else:
			for field in user.errors: form[field].errors.append(user.errors[field])
			add_error_message("Problemas al registrar el Usuario.")
	return render_template('register.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User.login( form.username.data, form.password.data)
		if user is not None:
			add_success_message("Bienvenido usuario")
			flask_login.login_user(user)
			return redirect(url_for('protected'))
		else:
			add_error_message('Usuario o password no validos!')
	return render_template('login.html', form = form)

@app.route('/protected')
@flask_login.login_required
def protected():
	return 'Logged in as: ' + flask_login.current_user.username

@app.route('/edit', methods=['GET', 'POST'])
def edit():
	form = EditUser(request.form, obj=flask_login.current_user )
	if request.method == 'POST' and form.validate():
		pass
		
	return render_template('edit.html', form = form)

@app.route('/logout')
def logout():
	flask_login.logout_user()
	return 'Logged out'

@app.route('/', methods=['GET'])
def index():
	return "Index"

if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	login_manager.login_view = 'login'
	login_manager.login_message = bootstrap_message("Es necesario que te iniciar sesion", "warning")
	

	with app.app_context():
		db.create_all()

	app.run(port = 8000)
