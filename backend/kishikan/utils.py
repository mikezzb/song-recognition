import hashlib
import os
import numpy as np
from collections import deque
from kishikan.configs import AUDIO_EXTENSIONS, FFT_OVERLAP_RATIO, FFT_WSIZE, ROUDING, SAMPLE_RATE

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

def offset_to_seconds(offset: int) -> int:
    return round(offset / SAMPLE_RATE * FFT_WSIZE * FFT_OVERLAP_RATIO, ROUDING)

def max_sliding_window(nums: np.ndarray, k: int):
    result = []
    end_index = 0
    dq = deque()
    for i in range(len(nums)):
        while dq and nums[dq[-1]] < nums[i]:
            dq.pop()
        dq.append(i)
        while dq and i - dq[0] >= k:
            dq.popleft()
        if i >= k - 1:
            result.append(nums[dq[0]])
            end_index = i
    # Remove dup by return len(result)
    return sum(result), end_index - k
