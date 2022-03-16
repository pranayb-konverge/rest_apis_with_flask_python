from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
import uuid
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = str(uuid.uuid4()) # make a random UUID
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be blank!"
    )
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x["name"] == name, items), None)
        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {"message": f"An item with name '{name}' already exist."}, 400
        
        request_data = Item.parser.parse_args()
        price = request_data["price"]
        item = {"name":name, "price":price}
        items.append(item)
        return item, 201

    def delete(self,name):
        global items
        items = list(filter(lambda x: x["name"] != name, items))
        return {"message" : "Item Deleted!"}
    
    def put(self, name):        
        data = Item.parser.parse_args()

        # Once again, print something not in the args to verify everything works
        item = next(filter(lambda x: x["name"] == name, items), None)
        if item is None:
            item = {"name" : name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)
        
        return item

class ItemsList(Resource):
    def get(self):
        return jsonify({"items":items})


api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemsList, '/items') 

app.run(port=5000)