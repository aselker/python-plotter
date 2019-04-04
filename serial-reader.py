#!/usr/bin/env python3
import serial
import numpy as np
import matplotlib.pyplot as plt

with serial.Serial('/dev/ttyACM0') as s:
  while True:
    data = []
    for _ in range(1000):
      data += [int(s.readline())]

    fourier = np.fft.rfft(data)
    plt.plot(np.fft.rfftfreq(len(data), 0.01), abs(fourier))
    plt.pause(0.05)
    plt.cla()

plt.show()
