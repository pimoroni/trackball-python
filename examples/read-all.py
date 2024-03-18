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
    print(f"r: {right:02d} u: {up:02d} d: {down:02d} l: {left:02d} switch: {switch:03d} state: {state}")
    time.sleep(0.05)
