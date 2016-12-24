from . import db
import datetime

class User(db.Model):
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
