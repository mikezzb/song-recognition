import os
from dotenv import load_dotenv
from flask import Flask
from kishikan import Kishikan

# load environment variables from .env
load_dotenv()

k = Kishikan(os.getenv('MONGO_URI'))

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
