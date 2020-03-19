import pytest
import itertools


def test_setup(GPIO, smbus2, trackball):
    device = trackball.TrackBall()
    del device


def test_setup_gpio_no_interrupt(GPIO, smbus2, trackball):
    # Interrupt pin always reads 1
    GPIO.input.return_value = 1
    device = trackball.TrackBall(timeout=0.1, interrupt_pin=16)
    with pytest.raises(RuntimeError):
        device.change_address(0x77)


def test_setup_gpio_interrupt(GPIO, smbus2, trackball):
    # Interrupt pin cycles between 0 and 1
    GPIO.input.side_effect = itertools.cycle([0, 1])
    device = trackball.TrackBall(timeout=0.1, interrupt_pin=16)
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

    GPIO.setwarnings.assert_called_once_with(False)
    GPIO.setmode.assert_called_once_with(GPIO.BCM)
    GPIO.setup.assert_called_once_with(16, GPIO.IN, pull_up_down=GPIO.PUD_OFF)
    del device


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
