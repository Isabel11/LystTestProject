from flask import Flask, request, json, render_template
from dbConnection import Connection
import datetime
import time

app = Flask(__name__)
db = None


@app.route('/rest/products/', methods=['GET','PUT'])
def products():
	""" distinguishes between PUT and GET requests and performs actions accordingly"""


	if request.method == 'GET':
		if(request.args.get('since') != None):
			db.execute("DELETE FROM items WHERE last_updated < '%s'"%__getDateString(since))

		dbrequest = db.select('SELECT * FROM items')
		columns = db.select('PRAGMA table_info(items)')
		dicts = []

		for item in dbrequest:
			item_dict = {}
			for i, col in enumerate(columns):
				item_dict[col[1]] = item[i]
			dicts.append(item_dict)		
		return  json.dumps({'result:':dicts})
	
	elif request.method == 'PUT':
		body = request.data
		jsonBody = json.loads(body)
		exists = __rowExists(jsonBody['code'], jsonBody['raw_color'])
		if(exists):
			__updateItem(jsonBody)
			return  json.dumps({'result:':'updated'})
		else: 
			__insertItem(jsonBody)
			return json.dumps({'result:':'added'})


@app.route('/rest/products/render')
def render():
	""" I used this for testing purposes and to analyse if output data was correct """

	error = None
	if request.method == 'GET':
		if(request.args.get('since') != None):
			db.execute("DELETE FROM items WHERE last_updated < '%s'"%__getDateString(since))

		dbrequest = db.select('SELECT * FROM items')
		columns = db.select('PRAGMA table_info(items)')
		dicts = []
		for item in dbrequest:
			item_dict = {}
			for i, col in enumerate(columns):
				item_dict[col[1]] = item[i]
			dicts.append(item_dict)					
		return render_template('lystTemplateReduced.html', items = dicts)		
		

def __insertItem(jsonBody):
	""" calls the database and inserts the values"""

	image_urls = json.dumps(jsonBody['image_urls'])
	stock_status = json.dumps(jsonBody['stock_status'])
	db.execute("INSERT INTO items VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",			
			[ 			
			 jsonBody['code'],
			 jsonBody['description'],
			 jsonBody['designer'],
			 jsonBody['gbp_price'],
			 jsonBody['gender'],
			 image_urls,
			 jsonBody['name'],
			 jsonBody['raw_color'],
			 jsonBody['sale_discount'],
			 jsonBody['source_url'],
			 stock_status,
			 jsonBody['last_updated'],
			 jsonBody['type'],
			 ])

def __rowExists(code, raw_color):
	""" tests if a row with unique identifier exists """
	
	items = db.select("SELECT EXISTS(SELECT * FROM items WHERE code = '%s' AND raw_color = '%s')"% (code, raw_color))
	return items[0][0]


def __updateItem(jsonBody):
	""" updates an item in the database"""

	update = "UPDATE items SET last_updated = '%s' WHERE code = '%s' AND raw_color = '%s' "% ( jsonBody['last_updated'],  jsonBody['code'],  jsonBody['raw_color'])
	db.execute(update)


def __getDateString(parameter):
	""" converts the parameter from the URL into a string that can be used for a databaseRequest """
	
	formatted = datetime.datetime.strptime(parameter, "%d-%m-%Y")
	return formatted.strftime("%Y-%m-%d %H:%M:%S")

if __name__ == '__main__':
	db = Connection('products.db')
	app.run(debug=True)


