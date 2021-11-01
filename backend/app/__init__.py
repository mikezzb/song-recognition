from dotenv import load_dotenv
from flask import Flask
from app.routes.songs import SongRecognizer
from kishikan import Kishikan
from flask_restful import reqparse, abort, Api, Resource

# load environment variables from .env
load_dotenv()

app = Flask(__name__)
api = Api(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


api.add_resource(SongRecognizer, '/songs/recognize')
