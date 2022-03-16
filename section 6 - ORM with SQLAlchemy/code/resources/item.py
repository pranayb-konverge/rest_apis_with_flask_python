import sqlite3
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    TABLE_NAME = 'items'
    # when the /item route will send the data we will capture it in the parser object
    # and validate the price
    parser = reqparse.RequestParser()
    parser.add_argument("price",
        type=float,
        required=True,
        help="This field cannot be blank!"
    )

    @jwt_required() # this method requires the JWT token
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}
        
        # using the parser object we will collect the data
        data = Item.parser.parse_args()
        # here we are accesing the ItemModel class to create the item
        item = ItemModel(name, data['price'])

        try:
            # using the object of the ItemModel class we will insert the data
            item.insert()
        except:
            return {"message": "An error occurred inserting the item."}

        return item.json()

    # delete the item by name
    @jwt_required()
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM {table} WHERE name=?".format(table=self.TABLE_NAME)
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()

        return {'message': 'Item deleted'}
    
    def put(self, name):        
        data = Item.parser.parse_args()
        # existing item we got from the db
        item = ItemModel.find_by_name(name)        
        # new item we got from the User
        updated_item = ItemModel(name, data['price'])
        if item is None:
            try:
                updated_item.insert()
            except:
                return {"message": "An error occurred inserting the item."}, 500
        else:
            try:
                updated_item.update()
            except:
                return {"message": "An error occurred updating the item."}, 500
        return updated_item.json()


class ItemsList(Resource):
    TABLE_NAME = 'items'

    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM {table}".format(table=self.TABLE_NAME)
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        connection.close()

        return {'items': items}