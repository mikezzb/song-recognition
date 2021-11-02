import os
from flask_restful import reqparse, Resource
from werkzeug.datastructures import FileStorage
from kishikan import Kishikan
import librosa

ksk = Kishikan(os.getenv('MONGO_URI'))

parser = reqparse.RequestParser()
# Allow parse to handle audio file upload
parser.add_argument('audio', type=FileStorage, location='files')

class SongRecognizer(Resource):
    def post(self):
        args = parser.parse_args()
        audio_file = args['audio']
        return ksk.match(librosa.load(audio_file.stream), preloaded=True)
