import unittest
from app import create_app, db
from app.models import User


class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		db.create_all()
		
	def tearDown(self):
		db.drop_all()
		self.app_context.pop()

	def test_new_user(self):
		username = 'eduardo'
		password = 'password'
		email = 'eduardo78d@gmail.com'

		self.user = User.new(username, password, email)
		response = self.user.username == username and self.user.password == password and self.user.email == email
		self.assertTrue(response)

	def test_save_user(self):
		response = self.user.save() and self.user.id is not None and self.user.id > 0
		self.assertTrue(response)



