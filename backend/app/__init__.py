from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from app.routes.songs import Song, SongRecognizer, QueryByHummingRecognizer
from app.routes.player import Player
from flask_restful import Api

# load environment variables from .env
load_dotenv()

app = Flask(__name__)
CORS(app)
api = Api(app)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


api.add_resource(SongRecognizer, '/songs/recognize')
api.add_resource(QueryByHummingRecognizer, '/songs/query-by-humming')
api.add_resource(Song, '/songs')
api.add_resource(Player, '/player/<string:filename>')
