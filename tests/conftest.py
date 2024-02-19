import sys
import mock
import pytest


CHIP_ID_PRESENT = [0x11, 0xba]
CHIP_ID_INVALID = [0, 0]
chip_id = [0x11, 0xba]
toggle_interrupt = True
interrupt_state = 1


class MockSMBus2():
    def __init__(self, bus):
        self.reg = None
        self.int = False

    def i2c_rdwr(self, *args):
        msg = args[0]

        if type(msg) == I2CMsgWrite:
            self.reg = msg.data

        if type(msg) == I2CMsgRead:
            if self.reg == [0xFA]:  # REG_CHIP_ID_L
                msg.set(chip_id)  # Return CHIP ID
            elif self.reg == [0xF9]:  # REG_INT
                # Toggle the interrupt pin
                # since the code waits for it to be unset and then set again
                if toggle_interrupt:
                    if self.int:
                        msg.set([0b00000001])
                    else:
                        msg.set([0b00000000])
                    self.int = not self.int
                else:
                    msg.set([interrupt_state])
            elif self.reg == [0x04]:  # REG_LEFT
                # Left, Right, Up, Down, Switch/Switch State
                msg.set([1, 0, 1, 0, 0b10000000])
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


@pytest.fixture(scope='function', autouse=False)
def smbus2():
    """Mock SMBUS module with fake device."""
    global chip_id
    global toggle_interrupt
    toggle_interrupt = True
    chip_id = CHIP_ID_PRESENT
    smbus2 = mock.Mock()
    sys.modules['smbus2'] = smbus2
    sys.modules['smbus2'].SMBus = MockSMBus2
    sys.modules['smbus2'].i2c_msg = MockI2CMsg
    yield smbus2
    del sys.modules['smbus2']


@pytest.fixture(scope='function', autouse=False, params=[0, 1], ids=["int_low", "int_high"])
def smbus2_nointerrupt(request):
    """Mock SMBUS module with fake device but non-working interrupt."""
    global chip_id
    global toggle_interrupt
    global interrupt_state
    interrupt_state = request.param
    toggle_interrupt = False
    chip_id = CHIP_ID_PRESENT
    smbus2 = mock.Mock()
    sys.modules['smbus2'] = smbus2
    sys.modules['smbus2'].SMBus = MockSMBus2
    sys.modules['smbus2'].i2c_msg = MockI2CMsg
    yield smbus2
    del sys.modules['smbus2']


@pytest.fixture(scope='function', autouse=False)
def smbus2_devicenotpresent():
    """Mock SMBUS module without fake device."""
    global chip_id
    chip_id = CHIP_ID_INVALID
    smbus2 = mock.MagicMock()
    sys.modules['smbus2'] = smbus2
    sys.modules['smbus2'].SMBus = MockSMBus2
    sys.modules['smbus2'].i2c_msg = MockI2CMsg
    yield smbus2
    del sys.modules['smbus2']


@pytest.fixture(scope='function', autouse=False)
def GPIO():
    """Mock RPi.GPIO module."""
    GPIO = mock.MagicMock()
    # Fudge for Python < 37 (possibly earlier)
    sys.modules['RPi'] = mock.Mock()
    sys.modules['RPi'].GPIO = GPIO
    sys.modules['RPi.GPIO'] = GPIO
    yield GPIO
    del sys.modules['RPi']
    del sys.modules['RPi.GPIO']


@pytest.fixture(scope='function', autouse=False)
def trackball():
    """Import and remove trackball module."""
    import trackball
    yield trackball
    del sys.modules['trackball']
