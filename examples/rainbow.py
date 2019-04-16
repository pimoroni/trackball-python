#!/usr/bin/env python

import time
import colorsys
from trackball import TrackBall

print("""Trackball: Rainbow

Fades through all the colours of the rainbow!

Press Ctrl+C to exit!
""")

trackball = TrackBall(interrupt_pin=4)

while True:
    h = int(time.time() * 100) % 360 / 360.0

    # Calculate RGB vals and mix in white
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, 1.0)]
    minimum = min(r,g,b)
    w = minimum
    r,g,b = r-minimum, g-minimum, b-minimum

    # Set LEDs
    trackball.set_rgbw(r, g, b, w)

    time.sleep(0.01)
