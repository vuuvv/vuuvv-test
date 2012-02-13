from sqlalchemy.schema import Table, DDLElement, Column, Constraint, MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.types import Integer
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.util import OrderedProperties

engine = create_engine("sqlite:///:memory:", echo=True)
meta = MetaData()

class CreateTable(DDLElement):
	def __init__(self, table):
		self.element = table

@compiles(CreateTable)
def visit_create_table(element, compiler, **kw):
	return compiler.visit_create_table(element)

class DropTable(DDLElement):
	def __init__(self, table):
		self.element = table

@compiles(DropTable)
def visit_drop_table(element, compiler, **kw):
	return compiler.visit_drop_table(element)

class AddColumn(DDLElement):
	def __init__(self, table, column):
		self.table = table
		self.column = column

@compiles(AddColumn)
def visit_add_column(element, compiler, **kw):
	return "ALTER TABLE %s ADD %s" %(
		element.table, 
		compiler.get_column_specification(element.column)
	)

class RemoveColumn(DDLElement):
	def __init__(self, table, column):
		self.table = table
		self.column = column

@compiles(RemoveColumn)
def visit_remove_column(element, compiler, **kw):
	return "ALTER TABLE %s DROP %s" %(
			element.table, element.column)

def create_table(table_name):
	def wrap(fn):
		table_definition = OrderedProperties()
		fn(table_definition)
		table = Table(table_name, meta)
		for attrname in table_definition.keys():
			value = table_definition[attrname]
			if isinstance(value, Column):
				table.append_column(value)
			elif isinstance(value, Constraint):
				table.append_constraint(value)
		table.create(engine)

	return wrap

@create_table('test_table')
def action(t):
	t.id = Column('id', Integer, primary_key=True)
	t.abc = 2
	t.ccc = 3
	t.add = 4
	t.cfg = 5

if __name__ == '__main__':
	from sqlalchemy import *
	e = create_engine("sqlite:///:memory:", echo=True)
	m = MetaData()
	users = Table('usertable', m,
			  Column('id', Integer, primary_key=True),
			  Column('name', String(50), server_default="test"),
	)
	print CreateTable(users)
	print DropTable(users)
	print AddColumn(users, Column('passwd', String(30), nullable=False, unique=True))
