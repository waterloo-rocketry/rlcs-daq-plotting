import serial
import io
import logging
from enum import Enum
import threading
import time
import datetime
from collections import deque

AXIS_MAX_LEN = 150

DATATYPES = {
    'pressure1': int,
    'pressure2': int,
}

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

        self.data = {'pressure1': {'X': deque(maxlen=AXIS_MAX_LEN),'Y': deque(maxlen=AXIS_MAX_LEN)},
                     'pressure2': {'X': deque(maxlen=AXIS_MAX_LEN),'Y': deque(maxlen=AXIS_MAX_LEN)}}

        self.data_test = {'pressure1': {'range': [0, 999]},\
                          'pressure2': {'range': [0, 999]}\
                          }

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

    def read_without_wrapper_temp(self):
        if not testing:
            value = self.device.readline(3).decode().rstrip('\n')
        print(value)
        return value

    def decode_assign(self, string):
        print(string.split('='))
        name, val = string.split('=')
        self.data[name]['Y'].append(DATATYPES[name](val))

        timestamp = datetime.datetime.now()#.strftime('%X%f')
        self.data[name]['X'].append(timestamp)

    def run(self):
        if not self.testing:
            while(True):
                if (self.device.in_waiting):
                    line = self.device.readline().decode().rstrip('\r\n')
                    self.decode_assign(line)
                    print(line)
        else: # testing
            test_data_list = [(k,v) for k, v in self.data_test.items()]
        
            while(True):
                for item in test_data_list:
                    name = item[0]
                    minval = item[1]['range'][0]
                    maxval = item[1]['range'][1]
                    try:
                        last_val = self.data[name]['Y'][-1]
                    except IndexError:
                        last_val = self.data_test[name]['range'][0]
                    
                    if last_val + 1 > maxval:
                        next_val = minval
                    else:
                        next_val = last_val + 1
                    #  next_val = minval if last_val+1>maxval else last_val+1
                    self.decode_assign(f'{name}={next_val}')
                    time.sleep(0.1)

            #  self.decode_assign(f'num={self.data["num"][-1]}')
            #  print(line)

        #  print(self.data)

    
    def serial_out(self, string):
        string += "\n"
        #  logger.log("Serial Out: " + string, print_line=logger.debug_mode)
        self.device.write(string_.encode())

class ResponseType(Enum):
    PART_RESPONSE = "+"
    RESPONSE = ">"
    LOG = "#"
    ERROR = "!"

def determine_message_type(char):
    for in_state in ResponseType:
        if char in in_state.value:
            return in_state
    return None

def sanitised_input(prompt, type_=None, min_=None, max_=None, range_=None):
    if min_ is not None and max_ is not None and max_ < min_:
        raise ValueError("min_ must be less than or equal to max_.")
    while True:
        ui = input(prompt + '\n>')
        if type_ is not None:
            try:
                if type_ == "alphanumeric_int":
                    if len(ui) != 4:
                        raise ValueError
                    else:
                        ui = int(ui)
                        type_ = int
                else:
                    ui = type_(ui)
            except ValueError:
                if type_ == "alphanumeric_int":
                    print("Input must be int in range <0000 - 9999>")
                else:
                    print("Input type must be {0}.".format(type_.__name__))
                continue
        if max_ is not None and ui > max_:
            print("Input must be less than or equal to {0}.".format(max_))
        elif min_ is not None and ui < min_:
            print("Input must be greater than or equal to {0}.".format(min_))
        elif range_ is not None and ui not in range_:
            if isinstance(range_, range):
                template = "Input must be between {0.start} and {0.stop}."
                print(template.format(range_))
            else:
                template = "Input must be {0}."
                if len(range_) == 1:
                    print(template.format(*range_))
                else:
                    print(template.format(" or ".join((", ".join(map(str, range_[:-1])), str(range_[-1])))))
        else:
            return ui

if __name__ == "__main__":
    arduino = Arduino(True)
    arduino.start()
    #  print(arduino.is_alive())
    arduino.join()
    #  print(arduino.is_alive())
