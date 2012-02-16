import re
import sys

from flask import Flask
from flask import current_app as app, g

from sqlalchemy.engine.url import URL
from sqlalchemy.engine import create_engine
from sqlalchemy.schema import MetaData, Table
from sqlalchemy.orm import scoped_session, sessionmaker, mapper

def camel_convert(name):
	s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class Application(Flask):
	def __init__(self, import_name, **kw):
		Flask.__init__(self, import_name, **kw)
		self.load_config()
		self.register_blueprints()
		self.init_database()

	def load_config(self):
		from vuuvv import default_config
		self.config.from_object(default_config)
		import config
		self.config.from_object(config)

	def register_blueprints(self):
		blue_prints = self.config['BLUEPRINTS'] 
		default = None 
		if self.config['DEFAULT_BLUEPRINT'] is None and blue_prints:
			default = self.config['DEFAULT_BLUEPRINT'] = blue_prints[0]

		for b in blue_prints:
			module = __import__(b)
			url_prefix = None if b == default else b
			self.register_blueprint(module.blueprint, url_prefix=url_prefix)

	def connect_database(self, reflect_all=False):
		config = self.config
		args = [config[name] for name in ('DRIVERNAME', 'USERNAME', 
			'PASSWORD', 'HOST', 'PORT', 'DATABASE')]
		url = URL(*args)
		self.db_engine = create_engine(str(url), echo = config['DEBUG'])
		self.db_meta = MetaData()
		if reflect_all:
			self.db_meta.reflect(bind=self.db_engine)
		self.db_session_cls = scoped_session(sessionmaker(
			autocommit=False, autoflush=False, bind=self.db_engine))

	def init_database(self):
		self.connect_database()
		self.find_models()

		@self.before_request
		def func():
			g.db_session = app.db_session_cls()

		@self.teardown_request
		def func(exc):
			g.db_session.commit()

	def find_models(self):
		blue_prints = self.config['BLUEPRINTS'] 
		meta = self.db_meta
		engine = self.db_engine
		for b in blue_prints:
			name = "%s.models" % b
			__import__(name)
			m = sys.modules[name]
			for modelname in m.__all__:
				model = getattr(m, modelname)
				tablename = camel_convert(modelname)
				table = Table(tablename, meta, autoload=True, autoload_with=engine)
				mapper(model, table)

