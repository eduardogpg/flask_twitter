from wtforms import Form
from wtforms import BooleanField
from wtforms import StringField
from wtforms import PasswordField
from wtforms import validators

username_validator = [validators.Length(min=4, max=25, message = 'Username  es requerido necesario')]
password_validator = [validators.Length(min=6, max=35, message = 'Email es requerido necesario')]
email_validator = [validators.DataRequired(message='El Password es requerido') ]

class RegistrationForm(Form):
    username = StringField('Username', username_validator)
    email = StringField('Email', password_validator)
    password = PasswordField('Password', email_validator )
    