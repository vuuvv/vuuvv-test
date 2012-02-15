from sqlalchemy.schema import Table, DDLElement, Column, Constraint, MetaData
from sqlalchemy.engine import create_engine
from sqlalchemy.types import Integer
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.util import OrderedProperties

from .database import engine

conn = engine.connect()
meta = MetaData()
meta.reflect(bind=engine)

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

def drop_table(table_name):
	table = meta.tables[table_name]
	table.drop()

def add_column(table, column):
	conn.execute(AddColumn(table, column))

def remove_column(table, column):
	conn.execute(RemoveColumn(table, column))

class CreateTable(DDLElement):
	def __init__(self, table):
		self.element = table

@compiles(CreateTable)
def visit_create_table(element, compiler, **kw):
	return compiler.visit_create_table(element)

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

