
class ColumnDefinition(object):
	def __init__(self, base=None, name=None, type=None, limit=None,
			  precision=None, scale=None, default=None, null=None):
		self.base = base
		self.name = name
		self.type = type
		self.limit = limit
		self.precision = precision
		self.scale = scale
		self.default = default
		self.null = null

	def to_sql(self):
		pass

class TableDefinition(object):
	def __init__(self, base):
		self.columns = []
		self.columns_hash = {}
		self.base = base

	def primary_key(self, name):
		self.column(name, "primary_key")
