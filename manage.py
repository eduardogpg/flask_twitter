from config import app_config
from app import create_app
#import os
#config_name = os.getenv('FLASK_CONFIG')

app = create_app(app_config['development'])

@app.route('/')
def index():
	return "Index"

if __name__ == '__main__':
	app.run()
