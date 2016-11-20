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

	def __create_password(self, password):
		return generate_password_hash(password)

	@classmethod
	def new(cls, username, email, password):
		user = User(username, email, password)
		result = user.__validate_username_and_email()

		if result is None:
			db.session.add(user)
			db.session.commit()
			return user

		print result
		return None

	def __validate_username_and_email(self):
		user = User.query.with_entities(User.username, User.email).filter(User.username == self.username or User.email == self.email).first()
		
		if user is not None:
			if user.username == self.username:
				return "Username ya registrado en la base de datos!"
			elif user.email == self.email:
				return "Email ya registrado en la base de datos!"



