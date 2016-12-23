from wtforms import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

from models import User

username_validator = [validators.Length(min=4, max=25, message = 'Minimo 4 caracteres maximo 25 caracteres')]
password_validator = [validators.DataRequired(message = 'El Password es requerido.')]
email_validator = [validators.Email(message ='Error en la estructura del Email.'), validators.DataRequired(message='Email es requerido necesario.') ]
name_validator = [validators.Length(min=5, max=25, message = 'Minimo 5 caracteres maximo 25 caracteres')]

class RegistrationForm(Form):
    username = StringField('Username', username_validator)
    email = StringField('Email', email_validator)
    password = PasswordField('Password', password_validator )
    
    def validate_username(form, field):
    	if ' ' in field.data:
    		raise validators.ValidationError('Error en la estructura del username')

class LoginForm(Form):
	username = StringField('Username', username_validator)
	password = PasswordField('Password', password_validator )


class EditUser(Form):
	username = StringField('Username', username_validator)
	email = StringField('Email', email_validator)
	password = PasswordField('Password', password_validator )
	first_name = StringField('First Name', name_validator)
	last_name = StringField('Last Name', name_validator)
	




