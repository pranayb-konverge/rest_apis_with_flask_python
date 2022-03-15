from flask import Flask

app = Flask(__name__)

@app.route('/') # home page - ex. http://www.google.com
def home():
    return "Hello User!"

app.run(port=5000)