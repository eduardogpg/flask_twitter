#!/usr/bin/env python
# -*- coding: utf-8 -*-

from . import db
import datetime
from sqlalchemy import or_
from sqlalchemy.exc import InvalidRequestError

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

"""
User.query.filter_by(id=123).delete() or User.query.filter(User.id == 123).delete()
"""

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, index = True)
	email = db.Column(db.String(50), unique=True)
	encrypted_password = db.Column(db.String(66))
	created_at = db.Column(db.DateTime, default = datetime.datetime.now())

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
		
	@property
	def password(self):
		return self.encrypted_password
	
	@password.setter
	def password(self, password):
		self.encrypted_password = generate_password_hash(password)

	@staticmethod
	def new(username = '', password = '', email = ''):
		return User(username, password, email)

	@staticmethod
	def create(username = '', password = '', email = ''):
		user = User.new(username, password, email)
		if user.save():
			return user
		return user.errors #Raise error?
		
	@staticmethod
	def find(id):
		return User.query.get(id)

	@staticmethod
	def authenticated(identifier, password):
		user = User.find_by_identifier(identifier)
		if user is not None:
			return user.verify_password(password)

	@classmethod
	def find_by_identifier(cls, identifier):
		conditional = or_(User.username == identifier, User.email == identifier)
		return User.query.filter(conditional).first()

	@classmethod
	def select_all(cls):
		pass

	@classmethod
	def delete_all(cls):
		db.session.query(User).delete()
		db.session.commit()

	def verify_password(self, password):
		return check_password_hash(self.encrypted_password, password)

	def save(self):
		if self.is_valid_to_save():
			db.session.add(self)
			db.session.commit()
			return True

	def destroy(self):
		try:
			db.session.delete(self)
			return True
		except InvalidRequestError:
			return False

	def is_valid_to_save(self):
		self.errors = {}
		if not self.is_valid_email():
			self.errors['email'] = 'El email no es correcto.'
		if not self.is_valid_username_len():
			self.errors['username'] = 'Maximo de 50 caracteres.'

		if not self.errors:
			return True
	
	def is_valid_email(self):
		import re
		return re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", self.email)

	def is_valid_username_len(self):
		return not len(self.username) > 50

	def is_validate_username(self):
		return ' ' not in self.username

	def __str__(self):
		return self.username



