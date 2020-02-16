from enum import Enum
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
import dash
from dash.dependencies import Output, Input, State

import datetime

class LabledEnum(Enum):
    def __new__(cls, value, label):
        value = value
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

def format_x(queue, settings):
    output_list = []
    for i in list(queue):
        if settings['relative_timestamps']:
            delta = i - datetime.datetime.now()
            output_list.append(delta.total_seconds())
        else:
            output_list.append(i)
    #  print(output_list)
    return output_list

def flatten(listy_boi, final=[]):
    for i in listy_boi:
        if isinstance(i,list):
            flatten(i, final)
        else:
            final.append(i)
    return final
