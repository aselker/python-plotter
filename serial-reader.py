#!/usr/bin/env python3
import serial
import numpy as np
import matplotlib.pyplot as plt

with serial.Serial('/dev/ttyACM0') as s:
  data = []
  while True:
    for _ in range(200):
      data += [int(s.readline())]
    data = data[-2000:]

    """
    fourier = np.fft.rfft(data)
    plt.plot(np.fft.rfftfreq(len(data), 0.01), abs(fourier))
    """
    plt.plot(np.arange(0, len(data)/500, 1/500), data)
    plt.ylim(-200, 1500)
    plt.pause(0.0001)
    plt.cla()

plt.show()
