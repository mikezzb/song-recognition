import os
import wave
from flask import Response
from flask_restful import Resource, reqparse
from app.configs import SONGS_DIR_NAME

dir = os.path.dirname(__file__)
songs_dir = os.path.join(dir, f'../../{SONGS_DIR_NAME}')

parser = reqparse.RequestParser()

class Player(Resource):
    def get(self, filename):
        return Response(wave.open(f"{songs_dir}/{filename}", "r"), mimetype="audio/x-wav")
