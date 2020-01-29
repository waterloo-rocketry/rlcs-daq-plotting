import serial
import io
import logging
from enum import Enum
import threading
import time
import datetime
from graphs import graphs
from collections import deque

AXIS_MAX_LEN = 150

# notes: 
# super broken (from old project) but useful starting point
# listing ports: python -m serial.tools.list_ports will print a list of available ports. It is also possible to add a regexp as first argument and the list will only include entries that matched.

# see documentation https://pythonhosted.org/pyserial/pyserial_api.html#classes
# screw with ports, id, parity, stopbits, rtscts
# device.in_waiting and .out_waiting gives num bytes in input and output buffers

class Arduino(threading.Thread):
    def __init__(self, testing, port='/dev/ttyACM0'):
        super().__init__()
        self.testing = testing
        if not testing:
            self.device = serial.Serial(port, baudrate=9600, timeout=5, write_timeout=3)
            self.connect()
        self.logger = logging.Logger('logger')
        #  self.val = 1

        #  pressure1 = deque(maxlen=20)
        self.graphs = graphs

        #  self.data = {'pressure1': {'X': deque(maxlen=AXIS_MAX_LEN),'Y': deque(maxlen=AXIS_MAX_LEN)},
                     #  'pressure2': {'X': deque(maxlen=AXIS_MAX_LEN),'Y': deque(maxlen=AXIS_MAX_LEN)}}

        #  self.data_test = {'pressure1': {'range': [0, 999]},\
                          #  'pressure2': {'range': [0, 30]}\
                          #  }

    def connect(self):
        try:
            self.device.open()
        except serial.SerialException:
            #  self.logger.log("Error: Failed to open serial port.", print_line=True)
            return False
        return True

    def disconnect(self):
        if self.device.is_open:
            self.device.close()

    #  def read(self):
        #  if not testing:
            #  value = self.device.readline(3).decode().rstrip('\n')
        #  print(value)
        #  return value

    def decode_assign(self, string):
        print(string.split('='))
        name, val = string.split('=')
        self.graphs[name]['data']['Y'].append(graphs[name]['type'](val))

        timestamp = datetime.datetime.now()#.strftime('%X%f')
        self.graphs[name]['data']['X'].append(timestamp)

    def run(self):
        if not self.testing:
            while(True):
                if (self.device.in_waiting):
                    line = self.device.readline().decode().rstrip('\r\n')
                    self.decode_assign(line)
                    print(line)
        else: # testing
            while(True):
                for name, graph in self.graphs.items():
                    minval = graph['range'][0]
                    maxval = graph['range'][1]
                    try:
                        last_val = graph['data']['Y'][-1]
                    except IndexError:
                        last_val = graph['range'][0]
                    
                    if last_val + 1 > maxval:
                        next_val = minval
                    else:
                        next_val = last_val + 1
                    #  next_val = minval if last_val+1>maxval else last_val+1
                    self.decode_assign(f'{name}={next_val}')
                    time.sleep(0.1)
    
    def serial_out(self, string):
        string += "\n"
        self.device.write(string_.encode())

if __name__ == "__main__":
    arduino = Arduino(True)
    arduino.start()
    #  print(arduino.is_alive())
    arduino.join()
    #  print(arduino.is_alive())
