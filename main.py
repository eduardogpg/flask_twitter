#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask
from config import DevelopmentConfig

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)

__author__ = 'Eduardo Ismael García Pérez'

@app.errorhandler(404)
def not_found(error):
	return "Not Found."


@app.route('/', methods=['GET'])
def index():
	return "Hello World."


if __name__ == '__main__':
	app.run()
