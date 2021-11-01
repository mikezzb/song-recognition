import os
from dotenv import load_dotenv
from flask import Flask
from kishikan import Kishikan

# load environment variables from .env
load_dotenv()

ksk = Kishikan(os.getenv('MONGO_URI'))

ksk.fingerprint("songs")

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"
