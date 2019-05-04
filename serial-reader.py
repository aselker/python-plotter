#!/usr/bin/env python3
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv


def moving_average(a, n=3):
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


chunk_size = 60
num_chunks = 12
chunks_to_drop = 1

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

        plt.sca(ax1)  # Set current axes
        fourier = np.fft.rfft(dataToShow)
        plt.plot(np.fft.rfftfreq(len(dataToShow), 0.001), abs(fourier))
        plt.xlim(0, 3)
        plt.ylim(0, 400000)

        plt.sca(ax2)  # Set current axes
        smoothed = moving_average(dataToShow, 1)
        # plt.plot(np.arange(0, len(smoothed)/500, 1/500), smoothed)
        plt.plot(smoothed)
        # plt.ylim(-200, 4096)

        plt.pause(0.01)
        plt.clf()

plt.show()
