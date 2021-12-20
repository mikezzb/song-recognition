import os
from flask_restful import abort, reqparse, Resource
from werkzeug.datastructures import FileStorage
from nazo import Nazo
from kishikan import Kishikan
from app.utils import load_audio
from app.db import db

ksk = Kishikan(os.getenv('MONGO_URI'))

parser = reqparse.RequestParser()
# Allow parse to handle audio file upload
parser.add_argument('audio', type=FileStorage, location='files')

class SongRecognizer(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            audio_file = args['audio']
            audio = load_audio(audio_file.stream)
            return ksk.match(audio, preloaded=True)
        except Exception as e:
            print(e)
            abort(400, description='Cannot convert audio')


nz = Nazo(os.getenv('MONGO_URI'))

class QueryByHummingRecognizer(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            audio_file = args['audio']
            audio = load_audio(audio_file.stream)
            return nz.query(audio, preloaded=True)
        except Exception as e:
            print(e)
            abort(400, description='Cannot convert audio')


parser.add_argument('mode', type=int, location='args')

class Song(Resource):
    def get(self):
        # Get all songs metadata
        args = parser.parse_args()
        return list(db.get_all_songs(args.get('mode')))
