from vuuvv.db import *
from sqlalchemy.types import *
from sqlalchemy.schema import *
from sqlalchemy.orm import *

@create_table('user')
def func(t):
	t.id = Column('id', Integer, primary_key=True)
	t.name = Column('name', String(50))
	t.fullname = Column('fullname', String(50))
	t.password = Column('password', String(50))

@create_table('province')
def func(t):
	t.id = Column('id', Integer, primary_key=True)
	t.name = Column('name', String(50))

@create_table('address')
def func(t):
	t.id = Column('id', Integer, primary_key=True)
	t.user_id = Column('user_id', Integer, ForeignKey('user.id'))
	t.province_id = Column('province_id', Integer, ForeignKey('province.id'))
	t.email_address = Column('email_address', String(50))

class User(object):
	pass

class Address(object):
	pass

class Province(object):
	pass

meta = MetaData()
user = Table('user', meta, autoload=True, autoload_with=engine)
address = Table('address', meta, autoload=True, autoload_with=engine)
province = Table('province', meta, autoload=True, autoload_with=engine)

mapper(User, user)
mapper(Province, province)

p = {}
for fk in address.foreign_keys:
	column = fk.column
	table_name = column.table.name
	key = column.key
	p[table_name] = relationship(globals()[table_name.capitalize()],
		backref=backref("addresses"))

mapper(Address, address, properties=p)

import pdb;pdb.set_trace()
Session = sessionmaker(bind=engine)
session = Session()

u = User()
u.name = "hi"
u.password = "HIHI"

p = Province()
p.name = "henan"

a = Address()
a.email_address = "a@163.com"
a.user = u
a.province = p

for addr in  u.addresses:
	print addr.email_address
session.add(a)
session.commit()


