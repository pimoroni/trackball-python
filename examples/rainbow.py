#!/usr/bin/env python

import colorsys
import time

from trackball import TrackBall

print("""Trackball: Rainbow

Fades through all the colours of the rainbow!

Press Ctrl+C to exit!
""")

trackball = TrackBall(interrupt_pin=4)

while True:
    h = int(time.time() * 100) % 360 / 360.0

    # Calculate RGB vals
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    w = 0

    # Set LEDs
    trackball.set_rgbw(r, g, b, w)

    time.sleep(0.01)
