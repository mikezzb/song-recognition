import librosa
import traceback
from kishikan.configs import SAMPLE_RATE
from kishikan.utils import get_audio_files, md5
from kishikan.core import fingerprint
from kishikan.db import Database

class Kishikan:
    def __init__(self, db_uri, db_name="kishikan"):
        self.db = Database(db_uri, db_name)
        self.__load_song_hashes()

    def __load_song_hashes(self):
        self.song_hashes = set(self.db.get_song_hashes())
        print(self.song_hashes)

    def fingerprint(self, path, is_dir=True, save=True):
        for file_path, file_name, file_ext in get_audio_files(path, is_dir=is_dir):
            audio_md5 = md5(file_path)
            if audio_md5 in self.song_hashes and save:
                print(f'Skipped duplicated fingerprinting for {file_path}...')
                continue
            try:
                y, sr = librosa.load(file_path, mono=True, sr=SAMPLE_RATE)
                fp = fingerprint(y, sr=sr)
                if save:
                    # Add song hash in db
                    self.db.insert_fingerprints(fp, audio_md5)
                    self.song_hashes.add(audio_md5)
                    self.db.insert_song(audio_md5, meta={
                        "name": file_name,
                        "ext": file_ext,
                    })
                else:
                    return fp
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {file_path}:\n{e}')
    
    def match(self, path):
        fp = self.fingerprint(path, is_dir=False, save=False)

