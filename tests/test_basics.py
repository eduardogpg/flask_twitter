import unittest

from flask import current_app
from app import create_app, db

class BasicsTestCase(unittest.TestCase):
	def setUp(self):
		"""El metodo se ejecuta antes de cada test"""
		self.app = create_app('testing')
		self.app_context = self.app.app_context() #app context?
		self.app_context.push() #Que hace push
		db.create_all()

	def tearDown(self):
		"""El metodo se ejecuta despues de cada test"""
		db.drop_all()
		self.app_context.pop()

	def test_app_exists(self):
		self.assertTrue(current_app is not None)

