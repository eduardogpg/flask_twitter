#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import app_config

__author__ = 'Eduardo Ismael García Pérez'

db = SQLAlchemy()

def create_app(config_name):
	print "Enviroment " + config_name
	
	app = Flask(__name__)
	app.config.from_object(app_config[config_name])
	db.init_app(app)

	@app.route('/')
	def index():
		return "Hola Mundo desde un paquete!"

	return app