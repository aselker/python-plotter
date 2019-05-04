#!/usr/bin/env python3
import serial
import csv

"""
Connect to a USB plethysmograph, download data, and save it as a CSV.
"""

with open("data.csv", 'w') as f:
  with serial.Serial('/dev/ttyACM0') as s:
    while True:
      line = s.readline()
      if line == "\0":
        break
      f.write(line + "\n")
