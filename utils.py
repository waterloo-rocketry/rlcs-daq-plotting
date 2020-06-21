from enum import Enum
from settings import Settings

class LabledEnum(Enum):
    def __new__(cls, value, label):
        value = value
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

def format_x(queue):
    output_list = []
    for i in list(queue):
        output_list.append(i)
    return output_list

def flatten(listy_boi):
    out = []
    for i in listy_boi:
        if isinstance(i, list):
            for j in i:
                out.append(j)
        else:
            out.append(i)
    return out
