from enum import Enum
import dash_core_components as dcc
import dash_html_components as html
from plotly import graph_objs as go
import dash
from dash.dependencies import Output, Input, State
from settings import Settings

import datetime

class LabledEnum(Enum):
    def __new__(cls, value, label):
        value = value
        obj = object.__new__(cls)
        obj._value_ = value
        obj.label = label
        return obj

def format_x(queue):
    output_list = []
    settings = Settings()
    for i in list(queue):
        if settings.relative_timestamps:
            delta = i - datetime.datetime.now()
            output_list.append(delta.total_seconds())
        else:
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
