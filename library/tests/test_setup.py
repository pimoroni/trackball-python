import sys
import mock


class MockSMBus2():
    def __init__(self, bus):
        self.reg = None

    def i2c_rdwr(self, *args):
        msg = args[0]

        if type(msg) == I2CMsgWrite:
            self.reg = msg.data

        if type(msg) == I2CMsgRead:
            if self.reg == [0xFA]:
                msg.set([0x11, 0xba])  # Return CHIP ID
            else:
                msg.set([0 for _ in range(msg.length)])


class MockI2CMsg():
    read = None
    write = None


class I2CMsgWrite(list):
    def __init__(self, addr, data):
        self.addr = addr
        self.data = data
        list.__init__(self)


class I2CMsgRead(list):
    def __init__(self, addr, length):
        self.length = length
        self.addr = addr
        list.__init__(self)

    def set(self, data):
        for x in data:
            self.append(x)


MockI2CMsg.read = I2CMsgRead
MockI2CMsg.write = I2CMsgWrite


def _mock():
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi.GPIO'] = mock.Mock()
    sys.modules['smbus2'] = mock.Mock()
    sys.modules['smbus2'].SMBus = MockSMBus2
    sys.modules['smbus2'].i2c_msg = MockI2CMsg


def test_setup():
    _mock()
    import trackball
    device = trackball.TrackBall()
    del device
