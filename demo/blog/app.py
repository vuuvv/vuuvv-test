#from flask import Flask
#from sqlalchemy.schema import MetaData
#from sqlalchemy.engine import create_engine
#from sqlalchemy.engine.url import URL
#
#def make_app():
#	app = Flask(__name__)
#	load_config(app)
#	register_blueprints(app)
#	return app
#
#def load_config(app):
#	from vuuvv import config as default_config
#	app.config.from_object(default_config)
#	import config
#	app.config.from_object(config)
#
#def register_blueprints(app):
#	blue_prints = app.config['BLUEPRINTS'] 
#	default = None 
#	if app.config['DEFAULT_BLUEPRINT'] is None and blue_prints:
#		default = app.config['DEFAULT_BLUEPRINT'] = blue_prints[0]
#
#	for b in blue_prints:
#		module = __import__(b)
#		url_prefix = None if b == default else b
#		app.register_blueprint(module.blueprint, url_prefix=url_prefix)
#
#app = make_app()
#
#@app.before_first_request
#def init_database():
#	from flask import current_app as app, g
#	config = app.config
#	args = [config[name] for name in ('DRIVERNAME', 'USERNAME', 'PASSWORD', 'HOST', 'PORT', 'DATABASE')]
#	url = URL(*args)
#	g.db_engine = create_engine(str(url), echo = config['DEBUG'])
#	g.db_meta = MetaData()
#	g.db_session = scoped_session(sessionmaker(sutocommit=False, autoflush=False, bind=engine))
#
#@app.teardown_request
#def remove_db_session():
#	g.db_session.remove()
#
#@app.route("/")
#def hello():
#	print app.url_map
#	return "Hello! World!!"
#
#app.run()

import sys
sys.path.insert(0, "../..")

from vuuvv.core import Application
app = Application(__name__)
app.run()
