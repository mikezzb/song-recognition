from pretty_midi import PrettyMIDI
import numpy as np
import librosa
from nazo.configs import SAMPLE_RATE

def convert_to_midi():
    pass


def midi_to_pitch_series(file):
    pv = None
    mid = PrettyMIDI(file)
    for instrument in mid.instruments:
        for note in instrument.notes:
            num_pvs = int(note.get_duration() * SAMPLE_RATE)
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
    for pitch, duration in pitches:
        num_pvs = int(duration * SAMPLE_RATE)
        note_pvs = np.full(num_pvs, pitch, dtype=np.float)
        series = np.concatenate([series, note_pvs]) if series is not None else note_pvs
    return series

def pv_to_time_series(file):
    ts = np.loadtxt(file)
    ts[ts == 0] = np.nan
    return ts
