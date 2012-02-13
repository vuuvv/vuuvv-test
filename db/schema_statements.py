from sqlalchemy.schema import DDLElement
from sqlalchemy.ext.compiler import compiles

class AddColumn(DDLElement):
	def __init__(self, table, column, type):
		self.table = table
		self.column = column
		self.type = type

@compiles(AddColumn)
def visit_add_column(element, compiler, **kw):
	return "ALTER TABLE %s ADD %s %s" %(
			element.table, element.column, element.type)

class RemoveColumn(DDLElement):
	def __init__(self, table, column):
		self.table = table
		self.column = column

@compiles(RemoveColumn)
def visit_remove_column(element, compiler, **kw):
	return "ALTER TABLE %s DROP %s" %(
			element.table, element.column)

