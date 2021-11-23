# General
import librosa

ROUNDING = 3
TOP_N = 6

# Audio
AUDIO_EXTENSIONS = set(['.mp3', '.wav'])
SAMPLE_RATE = 22050
MONO = True

# DB & API Configs
DATA_CONFIGS = {
    'METADATA_DB_NAME': 'songs',
}

# Query by humming configs
"""
Baken, R. J. (2000). Clinical Measurement of Speech and Voice, 2nd Edition. London: Taylor and Francis Ltd. (pp. 177), ISBN 1-5659-3869-0. That in turn cites Fitch, J.L. and Holbrook, A. (1970). Modal Fundamental Frequency of Young Adults in Archives of Otolaryngology, 92, 379-382, Table 2 (p. 381).
"""
F_MIN = librosa.note_to_hz('C2')
F_MAX = librosa.note_to_hz('C6')

PITCHES_PER_SECOND = 12
FRAME_LENGTH = 8192
