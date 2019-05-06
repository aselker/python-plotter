#!/usr/bin/env python3
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.signal import butter, lfilter, freqz


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


# Credit: https://stackoverflow.com/questions/25191620/creating-lowpass-filter-in-scipy-understanding-methods-and-units
def butter_lowpass(cutoff, fs, order=5):
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


"""
chunk_size = 60
num_chunks = 20
chunks_to_drop = 1
"""
chunk_size = 1
num_chunks = None
chunks_to_drop = 0
freq = 450  # Hz

with serial.Serial("/dev/ttyACM0", timeout=1) as s:
    s.write(b"G")
    lines = s.readlines()
    data = [int(l) for l in lines]

ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1, 2)

plt.sca(ax2)  # Set current axes
smoothed = butter_lowpass_filter(data, 10, freq)
# plt.plot(smoothed[200:])
plt.plot(np.arange(0, len(data) / freq, 1 / freq), data)
# plt.xlim(120, len(smoothed))
# plt.ylim(700, 800)

plt.sca(ax1)  # Set current axes
fourier = np.fft.rfft(data)
# fourier = np.fft.rfft(smoothed)
plt.plot(np.fft.rfftfreq(len(data), 1 / freq), abs(fourier))
plt.xlim(0, 5)
plt.ylim(0, 10000)


plt.show()
