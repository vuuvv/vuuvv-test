from vuuvv.db import *
from sqlalchemy import *

@create_table('user')
def user(t):
	t.id = Column('id', Integer, primary_key=True)
	t.username = Column('username', String(50), nullable=False)
