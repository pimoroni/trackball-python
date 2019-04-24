#!/usr/bin/env python

import time
import colorsys
from trackball import TrackBall
import atexit

print("""Trackball: Colour Control

Use the trackball and switch to control the hue and
brightness of the trackball's RGBW LEDs.

Scroll up to increase brightness and left/right
to change hue. Click to turn on/off.

Press Ctrl+C to exit!
""")

trackball = TrackBall(interrupt_pin=4)


@atexit.register
def clear_trackball():
    trackball.set_rgbw(0, 0, 0, 0)


x = 0
y = 0

toggled = False

while True:
    up, down, left, right, switch, state = trackball.read()

    # Update x and y vals based on movement
    y += up
    y -= down
    x += right
    x -= left

    # Clamp to min of 0 and max of 100
    x = max(0, min(x, 100))
    y = max(0, min(y, 100))

    # Calculate hue and brightness
    h = x / 100.0
    v = y / 100.0

    # Prevents button from retriggering
    debounce = 0.5

    # Change toggled state if switch is pressed
    if state and not toggled:
        toggled = True
        time.sleep(debounce)
    elif state and toggled:
        toggled = False
        time.sleep(debounce)

    # Set brightness to zero if switch toggled
    if toggled:
        v = 0

    # Calculate RGB vals
    w = 0
    r, g, b = [int(c * 255) for c in colorsys.hsv_to_rgb(h, 1.0, v)]

    # Set LEDs
    trackball.set_rgbw(r, g, b, w)

    time.sleep(0.01)
