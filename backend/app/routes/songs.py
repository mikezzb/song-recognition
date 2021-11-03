import os
from flask_restful import abort, reqparse, Resource
import numpy as np
from pydub import AudioSegment
from werkzeug.datastructures import FileStorage
from kishikan import Kishikan
import librosa

ksk = Kishikan(os.getenv('MONGO_URI'))

parser = reqparse.RequestParser()
# Allow parse to handle audio file upload
parser.add_argument('audio', type=FileStorage, location='files')

class SongRecognizer(Resource):
    def post(self):
        try:
            args = parser.parse_args()
            audio_file = args['audio']
            name, ext = os.path.splitext(audio_file.filename)
            if ext == ".wav":
                audio = librosa.load(audio_file.stream)
            elif ext == ".mp3":
                mp3_file = AudioSegment.from_mp3(audio_file.stream).set_channels(1).set_frame_rate(22050)
                audio_arr = mp3_file.get_array_of_samples()
                audio = (np.array(audio_arr).astype(np.float32), mp3_file.frame_rate)
            return ksk.match(audio, preloaded=True)
        except Exception as e:
            print(e)
            abort(400, description='Cannot convert audio')
