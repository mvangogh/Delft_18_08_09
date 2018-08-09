import serial
from time import sleep, time
from general_functions import current_time as time


class Device:
    DEFAULTS = {
        'read_termination': '\n',
        'write_termination': '\n',
        'encoding': 'ascii',
        'timeout': 1,
        'write_timeout': 1,
    }

    def __init__(self, port):
        self.port = port
        self.rsc = None

    def initialize(self):
        self.rsc = serial.Serial(self.port, timeout=self.DEFAULTS['timeout'])

    def idn(self):
        if self.rsc is None:
            raise Exception('First initialize the device with initialize()')

        return self.query('IDN')

    def get_analog_value(self, channel):
        message = 'IN:CH{}'.format(channel)
        message = 'IN:CH6'
        return int(self.query(message))

    def set_analog_value(self, channel, value):
        value = int(value / 3.3 * 4095)
        write_string = 'OUT:CH{}:{}'.format(channel, value)
        self.write(write_string)
        sleep(1)

    def write(self, message):
        message += self.DEFAULTS['write_termination']
        message = message.encode(self.DEFAULTS['encoding'])
        self.rsc.write(message)

    def read(self):
        line = "".encode(self.DEFAULTS['encoding'])
        line_termination = self.DEFAULTS['read_termination'].encode(self.DEFAULTS['encoding'])

        start_time = time()
        while True:
            new_char = self.rsc.read(size=1)
            line += new_char
            if new_char == line_termination:
                break
            if time()-start_time > 1000*self.DEFAULTS['timeout']: # Time gives time in milliseconds
                raise Exception('Device timed out')

        return line.decode(self.DEFAULTS['encoding'])

    def query(self, message):
        self.write(message)
        return self.read()

    def finalize(self):
        self.rsc.close()


if __name__ == '__main__':
    dev = Device('/dev/ttyACM0')
    dev.initialize()
    sleep(1)
    print(dev.idn())
    dev.finalize()