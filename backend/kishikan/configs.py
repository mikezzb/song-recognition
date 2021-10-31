from typing import Final

DATA_CONFIGS = {
    'DB_NAME': 'kishikan',
    'DIR_NAME': '../songs',
}

# Audio
AUDIO_EXTENSIONS = ('.mp3', '.wav')
SAMPLE_RATE = 22050

# Fingerprinting
FFT_WSIZE = 4096
FFT_OVERLAP_RATIO = 0.5
FAN_VALUE = 15
LOCAL_MAX_EPSILON = 10
AMP_MIN = 10

MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200
FINGERPRINT_REDUCTION = 20