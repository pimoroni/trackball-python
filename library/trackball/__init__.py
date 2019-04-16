from smbus2 import i2c_msg, SMBus
import time
import struct
import RPi.GPIO as GPIO


I2C_ADDRESS = 0x0A
I2C_ADDRESS_ALTERNATIVE = 0x0B

CHIP_ID = 0xBA11
VERSION = 1

REG_LED_RED = 0x00
REG_LED_GRN = 0x01
REG_LED_BLU = 0x02
REG_LED_WHT = 0x03

REG_LEFT = 0x04
REG_RIGHT = 0x05
REG_UP = 0x06
REG_DOWN = 0x07
REG_SWITCH = 0x08
MSK_SWITCH_STATE = 0b10000000

REG_USER_FLASH = 0xD0
REG_FLASH_PAGE = 0xF0
REG_INT = 0xF9
MSK_INT_TRIGGERED = 0b00000001
MSK_INT_OUT_EN = 0b00000010
REG_CHIP_ID_L = 0xFA
RED_CHIP_ID_H = 0xFB
REG_VERSION = 0xFC
REG_I2C_ADDR = 0xFD
REG_CTRL = 0xFE
MSK_CTRL_SLEEP = 0b00000001
MSK_CTRL_RESET = 0b00000010
MSK_CTRL_FREAD = 0b00000100
MSK_CTRL_FWRITE = 0b00001000


class TrackBall():
    def __init__(self, address=I2C_ADDRESS, interrupt_pin=None):
        self._i2c_address = address
        self._i2c_bus = SMBus(1)
        self._interrupt_pin = interrupt_pin

        chip_id = struct.unpack("<H", bytearray(self.i2c_rdwr([REG_CHIP_ID_L], 2)))[0]
        if chip_id != CHIP_ID:
            raise RuntimeError("Invalid chip ID: 0x{:04X}, expected 0x{:04X}".format(chip_id, CHIP_ID))

        if self._interrupt_pin is not None:
            GPIO.setwarnings(False)
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(self._interrupt_pin, GPIO.IN, pull_up_down=GPIO.PUD_OFF)

        self.enable_interrupt()

    def change_address(self, new_address):
        """Write a new I2C address into flash."""
        self.i2c_rdwr([REG_I2C_ADDR, new_address & 0xff])
        self._wait_for_flash()

    def _wait_for_flash(self):
        while self.get_interrupt():
            pass
        while not self.get_interrupt():
            time.sleep(0.001)

    def enable_interrupt(self, interrupt=True):
        """Enable/disable GPIO interrupt pin."""
        value = self.i2c_rdwr([REG_INT], 1)[0]
        value = value & ~MSK_INT_OUT_EN
        if interrupt:
            value = value | MSK_INT_OUT_EN

        self.i2c_rdwr([REG_INT, value])

    def i2c_rdwr(self, data, length=0):
        """Write and optionally read I2C data."""
        msg_w = i2c_msg.write(self._i2c_address, data)
        self._i2c_bus.i2c_rdwr(msg_w)

        if length > 0:
            time.sleep(0.02)
            msg_r = i2c_msg.read(self._i2c_address, length)
            self._i2c_bus.i2c_rdwr(msg_r)
            return list(msg_r)

        return []

    def get_interrupt(self):
        """Get the trackball interrupt status."""
        if self._interrupt_pin is not None:
            return GPIO.input(self._interrupt_pin) == 0
        else:
            value = self.i2c_rdwr([REG_INT], 1)[0]
            return value & MSK_INT_TRIGGERED

    def set_rgbw(self, r, g, b, w):
        """Set all LED brightness as RGBW."""
        self.i2c_rdwr([REG_LED_RED, r, g, b, w])

    def set_red(self, value):
        """Set brightness of trackball red LED."""
        self.i2c_rdwr([REG_LED_RED, value & 0xff])

    def set_green(self, value):
        """Set brightness of trackball green LED."""
        self.i2c_rdwr([REG_LED_GRN, value & 0xff])

    def set_blue(self, value):
        """Set brightness of trackball blue LED."""
        self.i2c_rdwr([REG_LED_BLU, value & 0xff])

    def set_white(self, value):
        """Set brightness of trackball white LED."""
        self.i2c_rdwr([REG_LED_WHT, value & 0xff])

    def read(self):
        """Read up, down, left, right and switch data from trackball."""
        left, right, up, down, switch = self.i2c_rdwr([REG_LEFT], 5)
        switch, switch_state = switch & ~MSK_SWITCH_STATE, (switch & MSK_SWITCH_STATE) > 0
        return up, down, left, right, switch, switch_state


if __name__ == "__main__":
    import os

    def exp_preserve_sign(x):
        if x < 0:
            return -(x**2)
        else:
            return x**2

    trackball = TrackBall(interrupt_pin=4)

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

    use_xte = os.system('which xte') == 0

    while True:
        while not trackball.get_interrupt():
            time.sleep(0.001)

        up, down, left, right, switch, state = trackball.read()

        print("r: {:02d} u: {:02d} d: {:02d} l: {:02d} switch: {:03d} state: {}".format(right, up, down, left, switch, state))

        if right:
            trackball.set_rgbw(255, 0, 0, 0)
        if up:
            trackball.set_rgbw(0, 255, 0, 0)
        if down:
            trackball.set_rgbw(0, 0, 255, 0)
        if left:
            trackball.set_rgbw(0, 0, 0, 255)

        if use_xte:
            if switch:
                cmd = 'xte "mouseclick 1"'
                os.system(cmd)
            elif right or up or left or down:
                cmd = 'xte "mousermove {} {}"'.format(exp_preserve_sign(right - left), exp_preserve_sign(down - up))
                os.system(cmd)

        time.sleep(0.0001)
