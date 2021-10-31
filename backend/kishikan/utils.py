import hashlib
import os
from kishikan.configs import AUDIO_EXTENSIONS

import pydub
import numpy as np

def read_audiofile(filename):
    audiofile = pydub.AudioSegment.from_file(filename)
    data = np.fromstring(audiofile.raw_data, np.int16)

    channels = []
    for chn in range(audiofile.channels):
        channels.append(data[chn::audiofile.channels])

    return channels, audiofile.frame_rate

def get_audio_files(path: str, is_dir=True):
    audio_files = []
    if is_dir:
        for f in os.listdir(path):
            name, ext = os.path.splitext(f)
            if ext in AUDIO_EXTENSIONS:
                audio_files.append((os.path.join(path, f), name, ext))
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
