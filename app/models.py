from . import db
import datetime

class User(db.Model):
	__tablename__ = 'users'

	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(50), unique=True, index = True)
	email = db.Column(db.String(50), unique=True)
	encrypted_password = db.Column(db.String(66))
	created_at = db.Column(db.DateTime, default = datetime.datetime.now())

	def __init__(self, username, password, email):
		self.username = username
		self.encrypted_password = password
		self.email = email
	
	@property
	def password(self):
		return self.encrypted_password

	@staticmethod
	def new(username = '', password = '', email = ''):
		return User(username, password, email)

	@staticmethod
	def create(username = '', password = '', email = ''):
		user = User.new(username, password, email)
		if user.save():
			return user
			
	@staticmethod
	def find(user_id):
		return User.query.get(User.id == user_id)

	@classmethod
	def delete_all(cls):
		db.session.query(User).delete()
		db.session.commit()

	def save(self):
		db.session.add(self)
		db.session.commit()
		return True

