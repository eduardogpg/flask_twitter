from flask import flash
from flask import Markup

def bootstrap_message(message = '', category= ''):
	return Markup('<div class="alert alert-{type}" role="alert"> {msg} </div>'.format(type=category, msg = message) )

def add_success_message(message):
	flash(bootstrap_message(message, 'success'))

def add_warning_message(message):
	flash(bootstrap_message(message, 'warning'))

def add_info_message(message):
	flash(bootstrap_message(message, 'info'))

def add_error_message(message):
	flash(bootstrap_message(message, 'danger'))
