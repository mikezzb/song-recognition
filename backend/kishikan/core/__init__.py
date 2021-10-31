import hashlib
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max

from kishikan.configs import FAN_VALUE, FFT_OVERLAP_RATIO, FFT_WSIZE, LOCAL_MAX_EPSILON, SAMPLE_RATE, MIN_HASH_TIME_DELTA, MAX_HASH_TIME_DELTA, FINGERPRINT_REDUCTION

FREQ_INDEX = 0
TIME_INDEX = 1

# Generate audio fingerprint from audio timeseries
def fingerprint(y, sr=SAMPLE_RATE):
    # Spectrogram
    sgram = mlab.specgram(
        y,
        NFFT=FFT_WSIZE,
        Fs=sr,
        window=mlab.window_hanning,
        noverlap=int(FFT_WSIZE * FFT_OVERLAP_RATIO)
    )[0]
    """ scipy way
    f, t, sgram = spectrogram(y, sr, 'hamming', FFT_WSIZE, int(FFT_WSIZE * FFT_OVERLAP_RATIO))  
    """
    # Convert to db and ignore warning
    with np.errstate(divide='ignore'):
        sgram = np.ma.log10(sgram) * 10
        sgram[np.isneginf(sgram)] = 0

    local_max = _get_img_peaks(sgram)

    # Return fingerprint hash
    return _fingerprint_hashes(local_max)

def _get_img_peaks(im: np.ndarray):
    peaks = peak_local_max(im, min_distance=LOCAL_MAX_EPSILON)
    print(f'Detected peaks {peaks.shape}')
    # plt the peaks
    plt.imshow(im)
    plt.scatter(peaks[:, TIME_INDEX], peaks[:, FREQ_INDEX], c='#DC143C', s=1)
    plt.gca().invert_yaxis()
    plt.show()
    return peaks

def _fingerprint_hashes(peaks: np.ndarray):
    n = peaks.shape[0]
    fp = []
    # Sort peaks with respect to time
    peaks = peaks[peaks[:, TIME_INDEX].argsort()]
    for i in range(n):
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
