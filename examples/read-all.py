#!/usr/bin/env python

import time
from trackball import TrackBall

print("""Trackball: Read All

Read and return directional values and switch events.

Press Ctrl+C to exit!
""")

trackball = TrackBall(interrupt_pin=4)
trackball.set_rgbw(0, 0, 0, 0)

while True:
    up, down, left, right, switch, state = trackball.read()
    print("r: {:02d} u: {:02d} d: {:02d} l: {:02d} switch: {:03d} state: {}".format(right, up, down, left, switch, state))
    time.sleep(0.05)
