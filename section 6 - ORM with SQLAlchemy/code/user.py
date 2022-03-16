import sqlite3
from flask_restful import Resource, reqparse

#create User class for auth mapping
class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, username):
        user = None
        # creat db connection
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # retirve the data row for the given username
        select_query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(select_query, (username,))
        row = result.fetchone() # get the first row
        if row:
            # passing positional parameters for id, username, password
            # as a classmethod we can use cls instead of Users class
            user = cls(*row) 

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        user = None
        # creat db connection
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        # retirve the data row for the given id
        select_query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(select_query, (_id,))
        row = result.fetchone() # get the first row
        if row:
            # passing positional parameters for id, username, password
            # as a classmethod we can use cls instead of Users class
            user = cls(*row) 

        connection.close()
        return user

class UserRegister(Resource):

    # when the /register route will send the data we will capture it in the parser object
    # and validate the username and password
    parser = reqparse.RequestParser()

    parser.add_argument('username',
            type=str,
            required=True,
            help="Username cannot be blank!"
    )

    parser.add_argument('password',
            type=str,
            required=True,
            help="Password cannot be blank!"
    )

    # registration of a user will be a post call
    def post(self):
        data = UserRegister.parser.parse_args()

        if User.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        insert_query = "INSERT INTO users VALUES (NULL, ?,?)"
        cursor.execute(insert_query, (data["username"], data["password"]))

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201
