import hashlib
from typing import List
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max
from kishikan.types import Fingerprint
from kishikan.configs import AMP_MIN, FAN_VALUE, FFT_OVERLAP_RATIO, FFT_WSIZE, LOCAL_MAX_EPSILON, SAMPLE_RATE, MIN_HASH_TIME_DELTA, MAX_HASH_TIME_DELTA, FINGERPRINT_REDUCTION

FREQ_INDEX = 0
TIME_INDEX = 1

# Generate audio fingerprint from audio timeseries
def fingerprint(ch: np.ndarray, sr=SAMPLE_RATE, verbose=False) -> List[Fingerprint]:
    fps = set()
    for audio in ch:
        # Spectrogram
        sgram = mlab.specgram(
            audio,
            NFFT=FFT_WSIZE,
            Fs=sr,
            window=mlab.window_hanning,
            noverlap=int(FFT_WSIZE * FFT_OVERLAP_RATIO)
        )[0]
        # Convert to db and ignore warning
        with np.errstate(divide='ignore'):
            sgram = np.ma.log10(sgram) * 10
            sgram[np.isneginf(sgram)] = 0
        peaks = _get_img_peaks(sgram, verbose)
        fps.update(_fingerprint_hashes(peaks)) 
    return list(fps)

def _get_img_peaks(im: np.ndarray, verbose: bool):
    # Find local max within neighborhood of LOCAL_MAX_EPSILON
    peaks = peak_local_max(im, min_distance=LOCAL_MAX_EPSILON, exclude_border=False)
    # Filter out noise peaks with amp lower than amp min
    amps = im[tuple(peaks.T)]
    peaks = peaks[amps > AMP_MIN]
    # plt the peaks
    print(f'Detected peaks {peaks.shape}')
    if verbose:
        plt.imshow(im)
        plt.scatter(peaks[:, TIME_INDEX], peaks[:, FREQ_INDEX], c='#DC143C', s=1)
        plt.gca().invert_yaxis()
        plt.show()
    return peaks

# https://www.ee.columbia.edu/~dpwe/papers/Wang03-shazam.pdf
def _fingerprint_hashes(peaks: np.ndarray) -> List[Fingerprint]:
    n = peaks.shape[0]
    fp = []
    # Sort peaks with respect to time
    peaks = peaks[peaks[:, TIME_INDEX].argsort()]
    # For every peaks[i] as an anchor point
    for i in range(n):
        # Use range peaks[i + 1, i + FAN_VALUE] as points in target zone of the anchor point
        # Use space (10x) for matching speed (10000x)
        for j in range(1, FAN_VALUE):
            if (i + j) < n:
                t1 = peaks[i][TIME_INDEX]
                t2 = peaks[i + j][TIME_INDEX]
                t_delta = t2 - t1
                if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:  
                    f1 = peaks[i][FREQ_INDEX]
                    f2 = peaks[i + j][FREQ_INDEX]
                    h = hashlib.sha1(f"{f1}|{f2}|{t_delta}".encode('utf-8'))
                    fp.append((h.hexdigest()[0:FINGERPRINT_REDUCTION], t1))
    return fp
