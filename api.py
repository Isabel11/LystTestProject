from flask import Flask, request, json
from dbConnection import Connection


app = Flask(__name__)
db = None

@app.route('/rest/products/', methods=['PUT', 'GET'])
def products():
	error = None
	if request.method == 'GET':
		items = db.select('SELECT * FROM items')
		columns = db.select('PRAGMA table_info(items)')
		dicts = []
		for item in items:
			item_dict = {}
			for i, col in enumerate(columns):
				item_dict[col[1]] = item[i]
			dicts.append(item_dict)					
		jsonDumps = json.dumps({'result:':dicts})
		return jsonDumps

	elif request.method == 'PUT':
		body = request.data
		jsonBody = json.loads(body)
		insertItem(jsonBody)
		return "OK"


def insertItem(jsonBody):

	image_urls = json.dumps(jsonBody['image_urls'])
	stock_status = json.dumps(jsonBody['stock_status'])
	db.execute("INSERT OR REPLACE INTO items VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",			
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
	

if __name__ == '__main__':
	db = Connection('products.db')
	app.run(debug=True)

