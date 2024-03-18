import itertools

import pytest


def test_setup(GPIO, smbus2, trackball):
    device = trackball.TrackBall()
    del device


def test_setup_gpio_no_interrupt(GPIO, smbus2, trackball):
    # Interrupt pin always reads 1
    device = trackball.TrackBall(timeout=0.1, interrupt_pin=16)
    device._gpio.get_value.return_value = trackball.Value.ACTIVE
    with pytest.raises(RuntimeError):
        device.change_address(0x77)


def test_setup_gpio_interrupt(GPIO, smbus2, trackball):
    # Interrupt pin cycles between 0 and 1
    device = trackball.TrackBall(timeout=0.1, interrupt_pin=16)
    device._gpio.get_value.side_effect = itertools.cycle([trackball.Value.INACTIVE, trackball.Value.ACTIVE])
    device.change_address(0x77)


def test_setup_no_interrupt(GPIO, smbus2_nointerrupt, trackball):
    device = trackball.TrackBall(timeout=0.1)
    with pytest.raises(RuntimeError):
        device.change_address(0x77)


def test_setup_nodevice(GPIO, smbus2_devicenotpresent, trackball):
    with pytest.raises(RuntimeError):
        device = trackball.TrackBall()
        del device


def test_change_address(GPIO, smbus2, trackball):
    device = trackball.TrackBall()
    device.change_address(0x77)


def test_setup_with_interrupt(GPIO, smbus2, trackball):
    device = trackball.TrackBall(interrupt_pin=16)

    assert device._interrupt_pin is not None
    assert device._gpio is not None


def test_leds(GPIO, smbus2, trackball):
    device = trackball.TrackBall()
    device.set_rgbw(255, 255, 255, 255)
    device.set_red(255)
    device.set_green(255)
    device.set_blue(255)
    device.set_white(255)


def test_read(GPIO, smbus2, trackball):
    device = trackball.TrackBall()
    left, right, up, down, switch, switch_state = device.read()
