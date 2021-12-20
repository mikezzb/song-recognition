import os
import wave
from flask import Response
from flask_restful import Resource, reqparse
from app.configs import SONGS_DIR_NAME

dir = os.path.dirname(__file__)
songs_dir = os.path.join(dir, f'../../../{SONGS_DIR_NAME}')

parser = reqparse.RequestParser()

def generate(filename):
    with open(f"{songs_dir}/{filename}", "rb") as f:
        data = f.read(1024)
        while data:
            yield data
            data = f.read(1024)
class Player(Resource):
    def get(self, filename):
        return Response(generate(filename), mimetype="audio/mpeg")
