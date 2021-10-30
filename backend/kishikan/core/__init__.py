import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from skimage.feature import peak_local_max

from kishikan.configs import FFT_OVERLAP_RATIO, FFT_WSIZE, LOCAL_MAX_EPSILON, SAMPLE_RATE

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

    print(f'local_maxima: {len(local_max)} of frequency & time pairs')

    # Return fingerprint hash
    return None

def _get_img_peaks(im):
    peaks = peak_local_max(im, min_distance=LOCAL_MAX_EPSILON)
    print(f'Detected peaks {peaks.shape}')
    peak_freqs, peak_times = peaks[:, 0], peaks[:, 1]
    # plt the peaks
    fig, ax = plt.subplots()
    ax.imshow(im)
    plt.plot(peak_times, peak_freqs, 'r.')
    ax.set_xlabel('Time')
    ax.set_ylabel('Frequency')
    ax.set_title("Spectrogram")
    plt.gca().invert_yaxis()
    plt.show()
    return list(zip(peak_freqs, peak_times))
