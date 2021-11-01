import os
from flask_restful import reqparse, Resource
from werkzeug.datastructures import FileStorage
from app.configs import SONGS_DIR_NAME, TEMP_DIR_NAME
from kishikan import Kishikan
import librosa

ksk = Kishikan(os.getenv('MONGO_URI'))

dir = os.path.dirname(__file__)
songs_dir = os.path.join(dir, f'../../{SONGS_DIR_NAME}')

parser = reqparse.RequestParser()
# Allow parse to handle audio file upload
parser.add_argument('audio', type=FileStorage, location='files')

class SongRecognizer(Resource):
    def post(self):
        args = parser.parse_args()
        audio_file = args['audio']
        return ksk.match(librosa.load(audio_file.stream), preloaded=True)
