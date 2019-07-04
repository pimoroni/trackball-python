# Examples

## evdev-mouse.py

Use the trackball as a virtual uinput mouse. Must be run as root.

Requirements:

```
sudo apt install python-evdev
sudo modprobe uinput
sudo cp 10-trackball.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules
```

## mouse.py

Use the trackball as a mouse via xautomation.

Requirements:

```
sudo apt install xautomation
```

## rainbow.py

Light up the trackball, cycling through rainbow colours (around the HSV colour space).

## colour-control.py

Light up the trackball. Scroll up/down to control brightness, left/right to change hue and click to turn on/off.

## read-all.py

Read and return the values of all directions and the switch.
