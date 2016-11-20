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
	password = db.Column(db.String(66))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, username, password, email):
		self.username = self.__generate_username(username)
		self.password = self.__generate_password(password)
		self.email = email
		self.__errors = {}

	def __generate_password(self, password):
		return generate_password_hash(password)

	def __generate_username(self, username):
		return username.lower()
		
	@staticmethod
	def get_conditional(username, email):
		#http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
		return or_(User.username == username, User.email == email)

	@classmethod
	def new(cls, username, password, email):
		return User(username, password, email )
			
	@classmethod 
	def login(cls, key, password):
		user = User.query.filter(User.get_conditional(key, key)).first()
		return user if user is not None and check_password_hash(user.password, password) else None
	
	@classmethod
	def find(cls,user_id):
		return User.query.filter(User.id == user_id).first()

	@property
	def errors(self):
		return self.__errors

	@property
	def arroba(self):
		return "@{username}".format(username = self.username)


	def get_username(self):
		return self.username[1::]

	def save(self):
		if self.is_valid_to_save():
			db.session.add(self)
			db.session.commit()
			return True
		
	def is_valid_to_save(self):
		self.__errors.clear()
		conditional = User.get_conditional(self.username, self.email)
		user = User.query.with_entities(User.username, User.email).filter(conditional).first()
			
		if user is not None:
			if user.username == self.username:
				self.__errors['username'] = "Username ya se encuentra registrado en la base de datos!"
			if user.email == self.email:
				self.__errors['email'] = "Email ya se encuentra registrado en la base de datos!"
			return False
		return True







