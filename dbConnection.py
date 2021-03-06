import sqlite3 as lite
from threading import Thread
from Queue import Queue


class Connection(Thread):
	""" 	Database class that handles requests for inserting and selecting items to and from the database.
		A queue was used for the incoming requests because there was a threading issue with the web server and the database class
	"""
	def __init__(self, dbName):
		super(Connection, self).__init__()
		self.dbName = dbName
		self.requests = Queue()
		self.start()


	def run(self):
		connection = lite.connect(self.dbName)
    		cursor = connection.cursor()
		while True:
			request, arg, result = self.requests.get()
			if(request == '--close--'):break
			cursor.execute(request, arg)
			connection.commit()
			if result:
				for rec in cursor:
					result.put(rec)
				result.put(('--no more--', None, None))
		connection.close()

	def execute(self, request, arg=None, result =None):
		""" executes a more complex request, e.g. insertion"""

		self.requests.put((request, arg or tuple(), result))

	def select(self, request, arg =None):
		"""selects from a database """

		result = Queue()
		self.execute(request, arg, result)
		ret = []
		while True:
			rec = result.get()
			if rec[0] == '--no more--':break
			else: ret.append(rec)
		
		return ret
		
	def close(self):
		self.execute('--close--')





