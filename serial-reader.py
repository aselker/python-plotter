#!/usr/bin/env python3

import serial

with serial.Serial('/dev/ttyACM0') as s:
  while True:
    r = int(s.readline())
    print(r)


