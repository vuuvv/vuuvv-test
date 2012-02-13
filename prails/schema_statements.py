from sqlalchemy import *

e = create_engine("sqlite:///:memory:", echo=True)
m = MetaData()

t1 = Table('t1', m,
			Column("x", Integer)
)

m.create_all(e)

from sqlalchemy.ext.compiler import compiles
from sqlalchemy.sql.expression import Executable, ClauseElement
from sqlalchemy import select

class InsertFromSelect(Executable, ClauseElement):
	def __init__(self, table, select):
		self.table = table
		self.select = select

@compiles(InsertFromSelect)
def visit_insert_from_select(element, compiler, **kw):
	import pdb;pdb.set_trace()
	return "INSERT INTO %s (%s)" % (
		compiler.process(element.table, asfrom=True),
		compiler.process(element.select)
	)
insert = InsertFromSelect(t1, select([t1]).where(t1.c.x>5))
print insert

users = Table('usertable', m,
			  Column('id', Integer, primary_key=True),
			  Column('name', String(50)),
)
s1 = select([users.c.id.label('uid'), users.c.id.label('uname')])

