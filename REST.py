# jsonify converts to JSON, request will be used when client send data to be posted IT
# render_template is for our html files. don't remember what this does
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [
    {
        "name": "My Wonderful Store",
        "items": [
    		{
    		"name": "My Item:",
    		"price": 15.99
    		}
    	]	
    }
]

# returning out javascript and html code which prints "hello world" for out root endpoint
# so javascript is running from my browser and it has to call my api to retrieve data from it so 
# it can then show it on the web site
@app.route("/")
def home():
	return render_template("index.html")


# POST - used to receive data
# GET - used to send data back only


# POST /store data: {name:}
@app.route("/store", methods = ["POST"])
def create_store():
	request_data = request.get_json()
	new_store = {
			"name": request_data["name"],
			"items": []
	}
	stores.append(new_store)
	return jsonify(new_store)

# GET /store/<string:name>
@app.route("/store/<string:name>")     # "http://127.0.0.1:5000/store/some_name"
def get_store(name):
	# iterate over stores
	# if store name matches, return that one
	# if none matches, return error message
	for store in stores:
		if store["name"] == name:
			return jsonify(store)
	return jsonify({"message": "store not found"}) # don't forget parenthesis because it needs to be a dictionary

# GET /store
@app.route("/store")
def get_stores():
	return jsonify({"stores": stores})


# POST /store/<string:name>/item data: {name:, price:}
@app.route("/store/<string:name>/item", methods = ["POST"])
def create_store_item_in_store(name):
	request_data =  request.get_json()
	for store in stores:
		if store["name"] == name:
			new_item = {
				"name": request_data["name"],
				"price": request_data["price"]
			}
			store["items"].append(new_item)
			return jsonify(new_item)
	return jsonify({"message": "store not found"})


# GET /store/<string:name>/item
@app.route("/store/<string:name>/item")
def get_item_in_store(name):
	for store in stores:
		if store["name"] == name:
			return jsonify({"items": store["items"]})
	return jsonify({"message": "store not found"})


app.run(port=5000)