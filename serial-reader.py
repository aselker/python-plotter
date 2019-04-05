#!/usr/bin/env python3
import serial
import numpy as np
import matplotlib.pyplot as plt
import csv

def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

with serial.Serial('/dev/ttyACM0') as s:
  data = []
  while True:
    try:
      for _ in range(200):
        data += [int(s.readline())]
      # data = data[-5000:]

      """
      fourier = np.fft.rfft(data)
      plt.plot(np.fft.rfftfreq(len(data), 0.002), abs(fourier))
      plt.xlim(0, 3)
      plt.ylim(0, 800000)
      """
      smoothed = moving_average(data, 40)
      # plt.plot(np.arange(0, len(smoothed)/500, 1/500), smoothed)
      plt.plot(smoothed)
      plt.ylim(-200, 4096)
      plt.pause(0.0001)
      plt.cla()

    except KeyboardInterrupt:
      with open('data.csv', 'w') as f:
        for x in data:
          f.write(str(x) + "\n")
      break

plt.show()
