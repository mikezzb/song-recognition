# General
ROUNDING = 3
MODE = 0  # Indicating Audio Fingerprinting

# Audio
AUDIO_EXTENSIONS = set(['.mp3', '.wav'])
SAMPLE_RATE = 22050
MONO = True

# Fingerprinting
FFT_WSIZE = 2048
FFT_OVERLAP_RATIO = 0.25
FAN_VALUE = 5
LOCAL_MAX_EPSILON = 6
LOCAL_MAX_EPSILON_LOW_ENERGY = 5
AMP_MIN = 0

MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
FINGERPRINT_REDUCTION = 20

LOW_ENERGY_THREHOLD = 0.05

# DB & API Configs
DATA_CONFIGS = {
    'DB_NAME': 'kishikan',
    'DIR_NAME': '../songs',
    'METADATA_DB_NAME': 'songs',
}
QUERY_BATCH_SIZE = 1000
TOP_N = 3
MAX_PEAKS_PER_FRAME = 5
