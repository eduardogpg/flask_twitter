#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from app import create_app, db
from app.models import User
#http://docs.python-guide.org/en/latest/writing/tests/

class UserTestCase(unittest.TestCase):
	def setUp(self):
		self.app = create_app('testing')
		self.app_context = self.app.app_context()
		self.app_context.push()
		self.params = self.get_params()
		self.invalid_params = self.get_invalid_params()
		self.create_table()
		
	def tearDown(self):
		self.app_context.pop()

	def test_new_user(self):
		user = self.new_user(self.params) 
		self.assertTrue(user is not None)

	def test_validate_email_user(self):
		user = self.new_user(self.params)
		user.email = 'invalid email'
		self.assertFalse(user.is_valid_email())

	def test_validate_len_username_user(self):
		user = self.new_user(self.params)
		user.username = 'eduardo'*50
		self.assertFalse(user.is_valid_username_len())

	def test_validate_username(self):
		user = self.new_user(self.params)
		user.username = 'eduardo ismael'
		self.assertFalse(user.is_validate_username())

	def test_save_user(self):
		user = self.new_user(self.params)
		user.save()
		self.assertTrue( user is not None and user.id > 0)

	def test_save_user_invalid_email(self):
		user = self.new_user(self.params)
		user.email = 'invalid email'
		user.save()
		email_error = user.errors.get('email', '')
		self.assertEqual(email_error, 'El email no es correcto.')

	def test_save_user_invalid_username(self):
		user = self.new_user(self.params)
		user.username = 'eduardo'*50
		user.save()
		username_error = user.errors.get('username', '')
		self.assertEqual(username_error, 'Maximo de 50 caracteres.')

	def test_create_user(self):
		user = self.create_user(self.params)
		self.assertTrue(user.id > 0)

	def test_create_user_with_invalid_params(self):#Debemos de arreglar esta prueba de aceptación
		response = self.create_user(self.invalid_params)
		self.assertIsInstance(response, dict)
		
	def test_find_user(self):
		self.create_user(self.params)
		user = User.find(1)
		response = user.username is not None and user.id == 1 and user.username == self.params['username']
		self.assertTrue(response)

	def test_update_username_user(self):
		self.create_user(self.params)
		user = User.find(1)
		new_username = 'new username'
		user.username = new_username
		user.save()
		user = User.find(1)
		self.assertTrue(user.username == new_username)

	def test_encrypted_password(self):
		user = self.create_user(self.params)
		self.assertTrue( user.password != self.params['password'] and len(user.password) == 66)

	def test_find_user_by_username(self):
		self.create_user(self.params)
		user = User.find_by_identifier(self.params['username'])
		self.assertEqual(user.id, 1)
	
	def test_find_user_by_email(self):
		self.create_user(self.params)
		user = User.find_by_identifier(self.params['email'])
		self.assertEqual(user.id, 1)

	def test_login_user(self):
		self.create_user(self.params)
		user = User.authenticated(self.params['email'], self.params['password'])
		self.assertTrue(user is not None)

	def create_table(self):
		db.drop_all()
		db.create_all()
	
	def create_user(self, params):
		return User.create(params['username'], params['password'], params['email'])

	def new_user(self, params):
		return User.new(params['username'], params['password'], params['email'])

	def get_params(self):
		return {
				'username' : 'eduardo78d',
				'password' : 'password',
				'email' : 'eduardo78d@gmail.com'
		}

	def get_invalid_params(self):
		return {
				'username' : 'eduardo78d' * 10,
				'password' : 'password',
				'email' : 'eduardo78dgmailcom'
		}


