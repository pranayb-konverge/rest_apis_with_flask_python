from user import User
from hmac import compare_digest

users = [
    User(1,"admin", "admin"),
    User(2,"Pranay", "sanz")
]

# indexing the user by admin name 
username_wrapping = { user.username: user for user in users}

userid_mapping = { user.id: user for user in users}

def authenticate(username, password):
    user = username_wrapping.get(username, None)
    # check if the user is available and the password matches
    if user and compare_digest(user.password, password):
        return user

def identity(payload):
    # get the identity from the user payload and check if it matches with the userid_mapping
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)