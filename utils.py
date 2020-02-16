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

def plot_output_mappings(plots):
    outputs = []
    for name, plot in plots.items():
        if plot['disable']:
            continue
        if plot['graph_type'] == go.Scatter:
            outputs.append(Output(name, 'figure'))

        elif plot['graph_type'] == html.P:
            if 'state' in name: #TODO janky janky janky please no
                outputs += [Output(name, 'children'), Output(name, 'className')]
            else:
                outputs.append(Output(name, 'children'))
    return outputs


def format_x(queue, settings):
    output_list = []
    for i in list(queue):
        if settings['relative_timestamps']:
            delta = i - datetime.datetime.now()
            #  print(delta)
            #  print(delta.total_seconds())

            output_list.append(delta.total_seconds())
        else:
            output_list.append(i)
    return output_list
