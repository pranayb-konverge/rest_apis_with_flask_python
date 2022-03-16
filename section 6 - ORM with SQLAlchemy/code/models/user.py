import sqlite3
from db import db

# UserModel class for auth mapping
class UserModel(db.Model):
    TABLE_NAME = 'users'
    __tablename__ = TABLE_NAME

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))

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
