import sqlite3 as lite
from threading import Thread
from Queue import Queue


class Connection(Thread):

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
			print request
			print type(arg)
			if(request == '--close--'):break
			cursor.execute(request, arg)
			connection.commit()
			if result:
				for rec in cursor:
					result.put(rec)
				result.put(('--no more--', None, None))
		connection.close()

	def execute(self, request, arg=None, result =None):
		self.requests.put((request, arg or tuple(), result))

	def select(self, request, arg =None):
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





