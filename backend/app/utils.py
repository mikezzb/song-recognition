
from typing import Union
from tempfile import SpooledTemporaryFile
from pydub import AudioSegment
import librosa
import numpy as np

SAMPLE_RATE = 22050
MONO = True

# Flask load the uploaded audio file in memory already, so the file can be in memory
def load_audio(file: Union[str, SpooledTemporaryFile], offset=0.0, duration=None):
    sound_file = AudioSegment.from_mp3(file).set_channels(1)
    samples = sound_file.get_array_of_samples()
    y = np.array(samples).astype(np.float32)/32768
    y = librosa.core.resample(y, sound_file.frame_rate, SAMPLE_RATE, res_type='kaiser_best')
    return (y, SAMPLE_RATE)
