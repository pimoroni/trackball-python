from smbus2 import i2c_msg, SMBus
import struct
import sys
import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

I2C_ADDRESS = 0x0A      #7 bit address
I2C_ADDRESS_ALTERNATIVE = 0x0B      #7 bit address

START_BYTE = 0x6A

CMD_RESET_READ_ADDR = 0x20

CMD_SET_RED_LED     = 0x30
CMD_SET_GREEN_LED   = 0x31
CMD_SET_BLUE_LED    = 0x32
CMD_SET_WHITE_LED   = 0x33
CMD_SET_ALL_LEDS    = 0x60

CMD_SET_INT_OUT_EN  = 0x34


class TrackBall():
    def __init__(self, address=I2C_ADDRESS):
        self._i2c_address = address
        self._i2c_bus = SMBus(1)

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        self.i2c_rdwr([START_BYTE, CMD_SET_ALL_LEDS, 0, 0, 0, 0])    

        self.enable_interrupt()

    def enable_interrupt(self, interrupt=True):
        self.i2c_rdwr([START_BYTE, CMD_SET_INT_OUT_EN, 1 if interrupt else 0])

    def i2c_rdwr(self, data, length=0):
        for d in data:
            self._i2c_bus.write_byte(self._i2c_address, d)

        return [self._i2c_bus.read_byte(self._i2c_address) for _ in range(length)]

        # msg_w = i2c_msg.write(self._i2c_address, data)
        # msg_r = i2c_msg.read(self._i2c_address, length)
        # self._i2c_bus.i2c_rdwr(msg_w, msg_r)
        # return [ord(c) for c in msg_r.buf]

    def get_interrupt(self):
        return GPIO.input(4) == 0

    def set_rgbw(self, r, g, b, w):
        self.i2c_rdwr([START_BYTE, CMD_SET_ALL_LEDS, r, g, b, w])  

    def set_red(self, value):
        """Set brightness of trackball red LED."""
        self.i2c_rdwr([START_BYTE, CMD_SET_RED_LED, value & 0xff])

    def set_green(self, value):
        """Set brightness of trackball green LED."""
        self.i2c_rdwr([START_BYTE, CMD_SET_GREEN_LED, value & 0xff])

    def set_blue(self, value):
        """Set brightness of trackball blue LED."""
        self.i2c_rdwr([START_BYTE, CMD_SET_BLUE_LED, value & 0xff])

    def set_white(self, value):
        """Set brightness of trackball white LED."""
        self.i2c_rdwr([START_BYTE, CMD_SET_WHITE_LED, value & 0xff])

    def read(self):
        """Read up, down, left, right and switch data from trackball."""
        data = self.i2c_rdwr([START_BYTE, CMD_RESET_READ_ADDR], 10) 
        right, up, down, left, switch = struct.unpack(">HHHHH", bytearray(data))
        return up, down, left, right, switch


if __name__ == "__main__":
    def exp_preserve_sign(x):
        if x < 0:
            return -(x**2)
        else:
            return x**2

    trackball = TrackBall()

    trackball.set_red(255)
    time.sleep(0.2)
    trackball.set_red(0)

    trackball.set_green(255)
    time.sleep(0.2)
    trackball.set_green(0)

    trackball.set_blue(255)
    time.sleep(0.2)
    trackball.set_blue(0)

    trackball.set_white(255)
    time.sleep(0.2)
    trackball.set_white(0)

    while True:
        while not trackball.get_interrupt(): # Wait for interrupt from breakout
            time.sleep(0.001)

        up, down, left, right, switch = trackball.read()

        print("right: {} up: {} down: {} left: {} switch: {}".format(right, up, down, left, switch))

        if right:
            trackball.set_rgbw(255, 0, 0, 0)
        if up:
            trackball.set_rgbw(0, 255, 0, 0)
        if down:
            trackball.set_rgbw(0, 0, 255, 0)
        if left:
            trackball.set_rgbw(0, 0, 0, 255)

        if switch:
            cmd = 'xte "mouseclick 1"'
            os.system(cmd)
        elif right or up or left or down:
            cmd = 'xte "mousermove %d %d"'% ( exp_preserve_sign(right-left), exp_preserve_sign(down-up) )
            os.system(cmd)


