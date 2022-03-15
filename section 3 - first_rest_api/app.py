from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

stores = [{
    'name': 'My Store',
    'items': [{'name':'my item', 'price': 15.99 }]
}]

# POST method to create/receive data
# GET method is to only send back the data

# home page
@app.route("/")
def home():
    return render_template('index.html')


# POST /store data:{name:} | create new store with name
@app.route("/store", methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        "name": request_data["name"],
        "items": []
    }
    stores.append(new_store)
    return jsonify({'stores':stores})

# GET /store/<string:store_name>| get store  for name and its data
@app.route('/store/<string:store_name>')
def get_store(store_name):
    # iterate over storest list
    print("11111111111111111111  ",stores)
    for store in stores:
        
        if store['name'] == store_name:
            # If the store name matches return it
            return jsonify(store)
    # if does not return message
    return jsonify({"messge": f"{store_name} store name not found."})
            
# GET /store/ | list of all store
@app.route("/store/")
def get__all_store():
    return jsonify({'stores':stores})

# POST /store/<string:store_name>/item {name:,price:} | create items for the given name of store
@app.route("/store/<string:store_name>/item", methods=['POST'])
def create_item_in_store(store_name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == store_name:
            new_item = {
                "name": request_data["name"],
                "price": request_data["price"]
            }
            store['items'].append(new_item)
            return jsonify(store)

    return jsonify({"messge": f"{store_name} store name not found."})

# GET /store/<string:store_name>/item | get items for the given name of store
@app.route("/store/<string:store_name>/item")
def get_item_in_store(store_name):
    # iterate over storest list
    for store in stores:
        if store['name'] == store_name:
            # If the store name matches return items
            return jsonify({"items":store["items"]})
    # if does not return message
    return jsonify({"messge": f"{store_name} store name not found."})

app.run(port=5000)