from config import app_config
from app import create_app, db
from app.models import User

from flask_script import Manager
from flask_script import Shell

from flask_migrate import Migrate, MigrateCommand

import os
config_name = os.getenv('ENVIROMENT_FLASK_CONFIG') or 'development'

app = create_app(config_name)
migrate = Migrate(app, db)
manager = Manager(app)

def console():
	return dict(app=app, db=db, User=User)

@manager.command
def test():
	import unittest
	tests = unittest.TestLoader().discover('tests')
	unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command('console', Shell(make_context = console))
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
	manager.run()
