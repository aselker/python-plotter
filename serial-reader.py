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


chunk_size = 60
num_chunks = 20
chunks_to_drop = 1
freq = 450  # Hz

with serial.Serial("/dev/ttyACM0") as s:
    for _ in range(chunks_to_drop * chunk_size):
        s.readline()

    data = []
    while True:
        for _ in range(chunk_size):
            data += [int(s.readline())]
        dataToShow = data[-(chunk_size * num_chunks) :]

        ax1 = plt.subplot(2, 1, 1)
        ax2 = plt.subplot(2, 1, 2)

        plt.sca(ax2)  # Set current axes
        smoothed = butter_lowpass_filter(dataToShow, 10, freq)
        # plt.plot(smoothed[200:])
        plt.plot(dataToShow)
        # plt.xlim(120, len(smoothed))
        # plt.ylim(700, 800)

        plt.sca(ax1)  # Set current axes
        fourier = np.fft.rfft(dataToShow)
        # fourier = np.fft.rfft(smoothed)
        plt.plot(np.fft.rfftfreq(len(dataToShow), 1 / freq), abs(fourier))
        plt.xlim(0, 5)
        plt.ylim(0, 10000)

        plt.pause(0.01)
        plt.clf()

plt.show()
