from flask import Flask

app = Flask(__name__)

# Define your routes here
@app.route('/')
def home():
    return "Welcome to the Flask app!"
