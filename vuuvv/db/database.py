from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL

from vuuvv import config

def get_engine():
	url = URL(config.DRIVERNAME, config.USERNAME, config.PASSWORD,
			  config.HOST, config.PORT, config.DATABASE)
	return create_engine(str(url), echo = config.DEBUG)

engine = get_engine()
