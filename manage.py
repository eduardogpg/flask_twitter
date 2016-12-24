from config import app_config
from app import create_app, db
from app.models import User

from flask_script import Manager
from flask_script import Shell

from flask_migrate import Migrate, MigrateCommand

#import os
#config_name = os.getenv('FLASK_CONFIG')

app = create_app(app_config['development'])
migrate = Migrate(app, db)

def console():
	return dict(app = app, db = db, User = User)


manager = Manager(app)
manager.add_command('console', Shell(make_context = console))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
	manager.run()
