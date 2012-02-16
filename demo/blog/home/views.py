from .blueprint import blueprint
from flask import g
from .models import User

@blueprint.route("/")
def hello():
	g.db_session.add(User('jack'))
	g.db_session.commit()
	return str(dir(User))
