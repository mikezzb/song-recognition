import hashlib
import os
from tempfile import SpooledTemporaryFile
import numpy as np
import multiprocessing as mp
from multiprocessing.pool import ThreadPool
import librosa
from collections import deque
from tinytag import TinyTag
import base64
from PIL import Image
from kishikan.configs import AUDIO_EXTENSIONS, FFT_OVERLAP_RATIO, FFT_WSIZE, MONO, ROUNDING, SAMPLE_RATE
from typing import Callable, List, Union

NUM_CPU = mp.cpu_count()

# Flask load the uploaded audio file in memory already, so the file can be in memory
def load_audio(file: Union[str, SpooledTemporaryFile], offset=0.0, duration=None):
    return librosa.load(file, sr=SAMPLE_RATE, mono=MONO, offset=offset, duration=duration)

def max_sliding_window(nums: np.ndarray, k: int):
    if k == 1:
        return nums
    d = deque()
    cur_max = 0
    cur_max_index = 0
    for i, n in enumerate(nums):
        while d and nums[d[-1]] < n:
            d.pop()
        d.append(i)
        if d[0] == i-k:
            d.popleft()
        if i >= k-1 and nums[d[0]] > cur_max:
            cur_max = nums[d[0]]
            cur_max_index = i
    return cur_max, cur_max_index

def parallel(f: Callable, iter: List):
    return list(map(f, iter))


""" Non-FP related utils """
def get_audio_files(path: str, is_dir=True):
    audio_files = []
    if is_dir:
        for root, dirs, files in os.walk(path):
            for f in files:
                name, ext = os.path.splitext(f)
                if ext in AUDIO_EXTENSIONS:
                    audio_files.append((os.path.join(root, f), name, ext))
    else:
        name, ext = os.path.splitext(path)
        if ext in AUDIO_EXTENSIONS:
            audio_files.append((path, name, ext))
    return audio_files

def offset_to_seconds(offset: int) -> int:
    return round(offset / SAMPLE_RATE * FFT_WSIZE * FFT_OVERLAP_RATIO, ROUNDING)

def get_song_metadata(file):
    tag = TinyTag.get(file, image=True)
    # Get image and convert to base64 for easier frontend display
    cover = base64.b64encode(tag.get_image()).decode('utf-8')
    tag = tag.as_dict()
    tag["cover"] = cover
    return tag

# Generate a hash for audio file
# Adopted from https://stackoverflow.com/a/3431838
def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
