#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import request
from flask import flash

from flask_wtf.csrf import CsrfProtect

from config import DevelopmentConfig
from models import db, User


from forms import RegistrationForm

app = Flask(__name__)
csrf = CsrfProtect()

app.config.from_object(DevelopmentConfig)

__author__ = 'Eduardo Ismael García Pérez'
	
@app.errorhandler(404)
def not_found(error):
	return "Not Found."

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm(request.form)
	if request.method == 'POST' and form.validate():
		user = User.new(username = form.username.data, password = form.password.data, email = form.email.data)

		if user.save():
			flash("Usuario creado exitosamente")
		else:
			print user.errors
			for field in user.errors:
				form[field].errors.append(user.errors[field])
			flash("Ooops no podemos crear tu cuenta, verifica tus datos!")

	return render_template('register.html', form = form)

@app.route('/', methods=['GET'])
def index():
	return "Hello World."


if __name__ == '__main__':
	csrf.init_app(app)
	db.init_app(app)

	with app.app_context():
		db.create_all()

	app.run(port = 8000)
