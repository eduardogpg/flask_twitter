from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

import datetime

db = SQLAlchemy()

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True)
	email = db.Column(db.String(50), unique=True)
	password = db.Column(db.String(66))
	created_at = db.Column(db.DateTime, default=datetime.datetime.now())

	def __init__(self, username, password, email):
		self.username = username
		self.password = self.__create_password(password)
		self.email = email
		self.errors = {}

	def __create_password(self, password):
		return generate_password_hash(password)

	@classmethod
	def new(cls, username, password, email):
		return User(username, password, email )
			
	def save(self):
		self.validate_fields()
		if not self.errors:
			db.session.add(self)
			db.session.commit()
			return True
		
	def validate_fields(self):
		self.errors.clear()
		user = User.query.with_entities(User.username, User.email).filter(User.username == self.username or User.email == self.email).first()
				
		if user is not None:
			if user.username == self.username:
				self.errors['username'] = "Username ya se encuentra registrado en la base de datos!"
			if user.email == self.email:
				self.errors['email'] = "Email ya se encuentra registrado en la base de datos!"
		
