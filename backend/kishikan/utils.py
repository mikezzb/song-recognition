import hashlib
import os
from kishikan.configs import AUDIO_EXTENSIONS

def get_audio_files(path: str, is_dir=True):
    audio_files = []
    if is_dir:
        for f in os.listdir(path):
            if f.endswith(AUDIO_EXTENSIONS):
                audio_files.append(os.path.join(path, f))
    else:
        if path.endswith(AUDIO_EXTENSIONS):
            audio_files.append(path)
    return audio_files

# Generate a hash for audio file
# Adopted from https://stackoverflow.com/a/3431838
def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
