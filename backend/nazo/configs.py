# General
import librosa

ROUNDING = 3
TOP_N = 3
MODE = 1  # Indicating QbSH

# Audio
AUDIO_EXTENSIONS = set(['.mp3', '.wav'])
SAMPLE_RATE = 22050
MONO = True

# DB & API Configs
DATA_CONFIGS = {
    'METADATA_DB_NAME': 'songs',
}

# Query by humming configs
F_MIN = librosa.note_to_hz('E2')
F_MAX = librosa.note_to_hz('C6')

PITCHES_PER_SECOND = 16
FRAME_LENGTH = 5568
