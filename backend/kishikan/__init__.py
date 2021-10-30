import librosa
import traceback
from kishikan.configs import SAMPLE_RATE
from kishikan.utils import get_audio_files, md5
from kishikan.core import fingerprint
from kishikan.db.mongodb import get_db

class Kishikan:
    def __init__(self, db_uri, db_name="kishikan"):
        self.db = get_db(db_uri, db_name)
        self.__load_song_hashes()

    def __load_song_hashes(self):
        self.song_hashes = set()

    def fingerprint(self, path, is_dir=True):
        for audio_file in get_audio_files(path, is_dir=is_dir):
            audio_md5 = md5(audio_file)
            if audio_md5 in self.song_hashes:
                print(f'Skipped duplicated fingerprinting for {audio_file}...')
                continue
            try:
                y, sr = librosa.load(audio_file, mono=False, sr=SAMPLE_RATE)
                fp = fingerprint(y, sr=sr)
                # Add fp in db
                self.song_hashes.add(audio_md5)
            except Exception as e:
                traceback.print_exc()
                print(f'Failed to fingerprint {audio_file}:\n{e}')
