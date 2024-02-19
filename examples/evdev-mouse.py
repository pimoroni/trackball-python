#!/usr/bin/env python
import math
import os
import time

from evdev import UInput
from evdev import ecodes as e

from trackball import TrackBall

print("""evdev-mouse.py - Use the Trackball as a system mouse.

You *must*:

    sudo modprobe uinput
    sudo cp 10-trackball.rules /etc/udev/rules.d/
    sudo udevadm control --reload-rules

And run this script as root with:

    sudo ./evdev-mouse.py

For this to work.

Press Ctrl+C to exit!

""")

os.system('modprobe uinput')

trackball = TrackBall(interrupt_pin=4)

MAX_X = 255
MAX_Y = 255

cap = {
    e.EV_KEY: [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL: [
        e.REL_X,
        e.REL_Y
    ]
}

ui = UInput(cap, name='Pimoroni Trackball', bustype=e.BUS_USB)

x = 0
y = 0

try:
    while True:
        while not trackball.get_interrupt():
            time.sleep(0.001)

        up, down, left, right, switch, state = trackball.read()

        x = right - left
        y = down - up

        x = math.copysign(x**2, x)
        y = math.copysign(y**2, y)

        x = int(x)
        y = int(y)

        # print("s: {} x: {:+03x}, y: {:+03x}".format(state, x, y))

        ui.write(e.EV_KEY, e.BTN_LEFT, state)
        ui.write(e.EV_REL, e.REL_X, x)
        ui.write(e.EV_REL, e.REL_Y, y)
        ui.syn()

except KeyboardInterrupt:
    pass
