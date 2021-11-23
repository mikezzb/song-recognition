import hashlib
import os
from tempfile import SpooledTemporaryFile
import librosa
from nazo.configs import AUDIO_EXTENSIONS, MONO, SAMPLE_RATE
from typing import Union


# Flask load the uploaded audio file in memory already, so the file can be in memory
def load_audio(file: Union[str, SpooledTemporaryFile], offset=0.0, duration=None):
    return librosa.load(file, sr=SAMPLE_RATE, mono=MONO, offset=offset, duration=duration)


""" Non-FP related utils """
def get_audio_files(path: str, is_dir=True, extensions: set = AUDIO_EXTENSIONS):
    audio_files = []
    if is_dir:
        for root, dirs, files in os.walk(path):
            for f in files:
                name, ext = os.path.splitext(f)
                if ext in extensions:
                    audio_files.append((os.path.join(root, f), name, ext))
    else:
        name, ext = os.path.splitext(path)
        if ext in AUDIO_EXTENSIONS:
            audio_files.append((path, name, ext))
    return audio_files

# Generate a hash for audio file
# Adopted from https://stackoverflow.com/a/3431838
def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
