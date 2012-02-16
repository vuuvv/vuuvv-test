
import sys
sys.path.insert(0, "../..")

from vuuvv.core import Application

app = Application(__name__)

with app.test_request_context():
	app.connect_database(reflect_all=True)
	__import__("db.schema")
