from flask import flash
from flask import Markup

def bootstrap_message(message = '', type_msg= 'info'):
	return Markup('<div class="alert alert-{type}" role="alert"> {msg} </div>'.format(type=type_msg, msg = message) )

def add_success_message(message):
	flash(bootstrap_message(message, 'success'))

def add_error_message(message):
	flash(bootstrap_message(message, 'danger'))

def add_warning_message(message):
	flash(bootstrap_message(message, 'warning'))
