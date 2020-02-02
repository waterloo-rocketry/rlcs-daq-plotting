from enum import Enum

class LabledEnum(Enum):
    def __new__(cls, value, label):
        value = value
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

#  class Connection_State(LabledEnum):
    #  OPEN = (1, "Open")
    #  CLOSED = (2, "Closed")
    #  UNKNOWN = (3, "Unknown")
    #  DAQ_VALVE_ILLEGAL = (4, "Illegal")

#  print(Connection_State(1).value)
