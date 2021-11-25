from pretty_midi import PrettyMIDI
import numpy as np
import librosa
from nazo.configs import F_MAX, F_MIN, FRAME_LENGTH, PITCHES_PER_SECOND

from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

def convert_to_midi():
    pass

def midi_to_pitch_series(file):
    pv = None
    mid = PrettyMIDI(file)
    for instrument in mid.instruments:
        for note in instrument.notes:
            num_pvs = int(note.get_duration() * PITCHES_PER_SECOND)
            note_pvs = np.full(num_pvs, note.pitch, dtype=np.float)
            pv = np.concatenate([pv, note_pvs]) if pv is not None else note_pvs
    return pv

def midi_to_pitches(file):
    melody_sequence = []
    mid = PrettyMIDI(file)
    for instrument in mid.instruments:
        for note in instrument.notes:
            melody_sequence.append([note.pitch, round(note.get_duration(), 4)])
    return melody_sequence

def pitches_to_series(pitches: np.ndarray):
    series = None
    carry = 0
    for pitch, duration in pitches:
        carry += duration * PITCHES_PER_SECOND
        num_pvs = duration * PITCHES_PER_SECOND
        mod = num_pvs % 1
        num_pvs = int(num_pvs)
        carry += mod
        if carry > 1:
            num_pvs += 1
            carry -= 1
        # print(f"{duration}: {num_pvs}")
        note_pvs = np.full(num_pvs, pitch, dtype=np.float)
        series = np.concatenate([series, note_pvs]) if series is not None else note_pvs
    return series

def pv_to_time_series(file):
    ts = np.loadtxt(file)
    ts[ts == 0] = np.nan
    return ts

def audio_to_pitches(y, sr):
    # num_pitches = int(librosa.get_duration(y, sr=sr) * PITCHES_PER_SECOND)
    # print(num_pitches)
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=F_MIN, fmax=F_MAX, fill_na=np.nan, frame_length=FRAME_LENGTH)
    # print(len(f0))
    return librosa.hz_to_midi(f0[~np.isnan(f0)])


A = 0.8
B = 0.6

def score(x: np.ndarray, y: np.ndarray):
    n = x.shape[0]
    m = y.shape[0]
    new_len = min(n, m)
    x, y = x[:new_len], y[:new_len]
    d_mean = np.mean(x) - np.mean(y)
    x -= d_mean
    e, _ = fastdtw(x, y, radius=2, dist=euclidean)
    score = A * B ** (e / n) + (1 - A) * (m / n)
    return e
