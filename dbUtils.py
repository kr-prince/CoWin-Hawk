"""
This module handles all the database objects and related functionalities
"""

from datetime import datetime
from sqlalchemy import create_engine, exc
from sqlalchemy import Table, Column, Integer, String, Text, DateTime, MetaData, UniqueConstraint, select

engine = create_engine('sqlite:///CoWinQuery.db')
meta = MetaData(engine)
# conn = None


userQuery = Table(
	'Query', meta,
	Column('id', Integer, primary_key = True),
	Column('name', String(50), nullable=False),
	Column('contact', String(10), nullable=False),
	Column('pincodeDistrictId', String(10), nullable=False),
	Column('districtName', String(50), default='NA'),
	Column('status', String(15), default='Accepted'),
	Column('message_text', Text, default='Accepted for monitoring'),
	Column('timestamp', DateTime, default=datetime.now()),

	# Constraints
	UniqueConstraint('contact', 'pincodeDistrictId', name='contact_pincodeDistrict_uc')
)


def addQuery(record):
	""" This will add new record in the userQuery table
	"""
	try:
		with engine.begin() as conn:
			conn.execute(userQuery.insert(), [record])
	except exc.IntegrityError:
		raise Exception('Duplicate contact and Pincode/District.')
	except Exception as ex:
		print(ex)
		raise Exception('Error Occurred.')


def getAllQuery():
	""" This will get all the records in the userQuery table
	"""
	rows = []
	with engine.begin() as conn:
		sel = userQuery.select()
		rows = conn.execute(sel).fetchall()
	return rows


def getQuerysByStatus(status):
	"""  This will get the records with specified status 
	"""
	rows = []
	with engine.begin() as conn:
		sel = userQuery.select().where(userQuery.c.status==status)
		rows = conn.execute(sel).fetchall()
	return rows


def setMonitoringQuerys():
	"""  This will set the 'Accepted' Queries to 'Monitoring' 
	"""
	rows = 0
	with engine.begin() as conn:
		upd = userQuery.update().where(userQuery.c.status=='Accepted').values(
			status='Monitoring', message_text='CoWin Hawk is monitoring.',
			timestamp=datetime.now())
		rows = conn.execute(upd)
	if rows.rowcount > 0:
		print("%d Query(s) added for monitoring.." %(rows.rowcount))


def setNotifiedQuerys(id, message_text):
	"""  This will set the status to 'Notified' and add details based on Id
	"""
	rows = 0
	with engine.begin() as conn:
		upd = userQuery.update().where(userQuery.c.id==id).values(
				status='Notified', message_text=message_text,timestamp=datetime.now())
		rows = conn.execute(upd)

