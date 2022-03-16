from flask import Flask
from flask_restful import Api
import uuid
from flask_jwt import JWT

from security import authenticate, identity
from user import UserRegister
from item import Item, ItemsList

app = Flask(__name__)
app.secret_key = str(uuid.uuid4()) # make a random UUID
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

api.add_resource(Item, '/item/<string:name>') 
api.add_resource(ItemsList, '/items') 
api.add_resource(UserRegister, '/register') # user registration route 

app.run(port=5000, debug=True)