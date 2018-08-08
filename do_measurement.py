from time import sleep

import numpy as np
from simple_daq import Device


dev = Device('/dev/ttyACM0')
dev.initialize()
sleep(1)
out_port = 0  # Output Port
in_port = 0  # Input Port

voltages = np.linspace(0,4025,100)  # Voltages to sweep
data = np.zeros((100))  # Where to store data

for i in range(len(voltages)):
    dev.set_analog_value(out_port, voltages[i])
    sleep(0.1)
    data[i] = dev.get_analog_value(in_port)

print(data)