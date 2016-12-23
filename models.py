from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from flask_login import UserMixin

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, index = True)
	email = db.Column(db.String(50), unique=True)
	encrypted_password = db.Column(db.String(66))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, username, password, email):
		self.username = username
		self.password = password
		self.email = email
		self.__errors = {}

	
	@classmethod
	def new(cls, username, password, email):
		return User(username, password, email)

	@classmethod
	def find(cls,user_id):
		return User.query.get(User.id == user_id)
	
	@classmethod
	def find_by_identifier(cls, username = '', email = ''):
		conditional = or_(User.username == username, User.email == email)
		return User.query.filter(User.id == user_id).first()

	@property
	def user(self):
		return "@{username}".format(username = self.username)
	
	@property
	def password(self):
		return None

	@password.setter
	def password(self, password):
		self.encrypted_password = generate_password_hash(password)
		
	def verify_password(self, password):
		return check_password_hash(self.encrypted_password, password)

	@property
	def errors(self):
		return self.__errors

	def save(self):
		if self.is_valid_to_save():
			db.session.add(self)
			db.session.commit()
			self.__errors.clear()
			return True

	def __set_errors(self, model):
		self.__errors.clear()

		if model is not None:
			if model.username == self.username:
				self.__errors['username'] = "Username ya se encuentra registrado en la base de datos!"
			if model.email == self.email:
				self.__errors['email'] = "Email ya se encuentra registrado en la base de datos!"

		return True if self.__errors else False

	def is_valid_to_save(self):
		return self.is_valid_to_create() if self.id is None else self.is_valid_to_update()
		
	def is_valid_to_update(self):
		response = User.find_by_identifier(self.username, self.email)
		if response is not None and response.id != self.id:
			return not self.__set_errors(response)
		return True

	def is_valid_to_create(self):
		response = User.find_by_identifier(self.username, self.email)
		return not self.__set_errors(response)
		

