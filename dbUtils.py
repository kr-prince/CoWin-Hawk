"""
This module handles all the database objects and related functionalities
"""

from sqlalchemy.sql import func
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData, UniqueConstraint, select

engine = create_engine('sqlite:///CoWinQuery.db')
meta = MetaData(engine)
conn = None


userQuery = Table(
	'Query', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String(50), nullable=False),
	Column('contact', String(10), nullable=False),
	Column('pincodeDistrict', String(50)),
	Column('status', String(15), default='Accepted'),
	Column('message_text', Text, default=''),
	Column('timestamp', DateTime, default=func.now()),

	# Constraints
	UniqueConstraint('contact', 'pincodeDistrict', name='contact_pincodeDistrict_uc')
)

def addQuery(record):
	""" This will add new record in the userQuery table
	"""
	conn = engine.connect()
	ins = userQuery.insert().values(name=record['name'], contact=record['contact'],
					pincodeDistrict=record['pincode'])
	conn.execute(ins)

def showDbData():
	""" This will show the current records in userQuery table
	"""
	conn = engine.connect()
	query = select([userQuery])
	result = conn.execute(query)
	return result



