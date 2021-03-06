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


drop_begin = 200
drop_end = 0
freq = 450  # Hz
smoothed_drop_begin = 200

with serial.Serial("/dev/ttyACM0", timeout=1) as s:
    s.write(b"G")
    lines = s.readlines()
    ys = [int(l) for l in lines]
    if drop_end:
        ys = ys[drop_begin:-drop_end]
    else:
        ys = ys[drop_begin:]

xs = np.arange(
    0, len(ys) / freq - 0.000001, 1 / freq
)  # Subtract a small number to avoid rounding issues

ax1 = plt.subplot(2, 1, 1)
ax2 = plt.subplot(2, 1, 2)

plt.sca(ax1)  # Set current axes
plt.plot(xs, ys, label="Raw")
smoothed = butter_lowpass_filter(ys, 10, freq)
plt.plot(xs[smoothed_drop_begin:], smoothed[smoothed_drop_begin:], label="Smoothed")
# plt.xlim(120, len(smoothed))
# plt.ylim(700, 800)

plt.title("Signal")
plt.xlabel("Time (s)")
plt.ylabel("Light (/4096)")
plt.grid(True)
ax1.legend()


plt.sca(ax2)  # Set current axes
fourier = np.fft.rfft(ys)
plt.plot(np.fft.rfftfreq(len(ys), 1 / freq), abs(fourier))
"""
fourier_smoothed = np.fft.rfft(smoothed)
plt.plot(np.fft.rfftfreq(len(smoothed), 1 / freq), abs(fourier_smoothed))
"""
plt.xlim(0, 4)
plt.ylim(0, 2e4)
plt.title("Fourier Transform")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)
ax1.legend()


plt.show()
