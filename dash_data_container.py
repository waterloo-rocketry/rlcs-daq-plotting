from plots import pressure_mass_plots, current_plots, voltages, valve_states
import random
import dash
import dash_html_components as html
from plotly import graph_objs as go
from dash.dependencies import Output
from collections import deque
import math
from settings import settings
import numpy as np

# Calculate how many items to keep per plot using the plot domain and arduino refresh rate
MAX_LEN = int((settings['range'][1]-settings['range'][0])*settings['arduino_hz'])

class DashData:
    def __init__(self):
        self.plots_currents = self.generate_component_objects(IgnitionCurrentPlot, current_plots)
        self.plots_pressure_mass = self.generate_component_objects(PressureMassPlot, pressure_mass_plots)
        self.plots = self.plots_pressure_mass + self.plots_currents
        self.voltages = self.generate_component_objects(Voltage, voltages)
        self.valve_states = self.generate_component_objects(ValveState, valve_states)
        self.generate_mappings()

    def generate_mappings(self):
        self.mappings = {}
        for i in self.plots + self.voltages + self.valve_states:
            self.mappings[i.id]=i

    def generate_component_objects(self, new_type, dict_form_list):
        dash_objs = []
        for i in dict_form_list:
            #  print(i)
            if not i['disable']:
                dash_objs.append(new_type(i))
        return dash_objs

    def update(self,component_id, val, timestamp):
        component_obj = self.mappings[component_id]
        component_obj.update(val, timestamp)

class DashComponent:
    def __init__(self, data_dict):
        #  print(data_dict)
        self.id = data_dict['id']
        self.title = data_dict['title']
        self.range = data_dict['range']
        self.data = {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)}

    # Entirely for testing, this just generates values in interesting patterns
    def generate_next_test_value(self):
        if not self.data['Y']:
            # If no data exists, just get a random number in the interval
            return random.randint(self.range[0], self.range[1])

        range_breadth = int((self.range[1] - self.range[0]) ** (1/4))
        delta = random.randint(-range_breadth, range_breadth)
        new = self.data['Y'][-1] + delta
        out = np.clip(new, self.range[0], self.range[1])
        #  print(out)
        return out


class Voltage(DashComponent):
    def __init__(self, data_dict):
        super().__init__(data_dict)
        self.dash_object_type = html.P

    def update(self, val, timestamp):
        self.data['Y'].append(int(val))
        self.data['X'].append(timestamp)

    def get_mapped_output(self):
        return Output(self.id, 'children')

    def get_y_formatted(self):
        def format(float_val):
            return f'{float_val:.2f}'
        if self.data['Y']:
            return format(self.data['Y'][-1]/1000.0)
        else:
            return format(-999.0)

class ValveState(DashComponent):
    def __init__(self, data_dict):
        super().__init__(data_dict)
        self.dash_object_type = html.P

    def update(self, val, timestamp):
        # TODO: Print error if val is outside the range of ValveState
        self.data['Y'].append(int(val))
        self.data['X'].append(timestamp)

    def get_mapped_output(self):
        #  return Output(self.id, 'children')
        return [Output(self.id, 'children'), Output(self.id, 'className')]

class Plot(DashComponent):
    def __init__(self, plot_dict):
        super().__init__(plot_dict)
        self.dash_object_type = go.Scatter

    def update(self, val, timestamp):
        self.data['Y'].append(int(val))
        self.data['X'].append(timestamp)
        #  print(f'data: {self.data}')

    def get_mapped_output(self):
        return Output(self.id, 'figure')

class PressureMassPlot(Plot):
    def __init__(self, plot_dict):
        super().__init__(plot_dict)
        # Todo also use this to set axis titles and shit
    
    def get_y_list(self):
        y_list = []
        for i in self.data['Y']:
            y_list.append(i)
        return y_list


class IgnitionCurrentPlot(Plot):
    def __init__(self, plot_dict):
        super().__init__(plot_dict)
        # Todo also use this to set axis titles and shit
    
    def get_y_list(self):
        y_list = []
        mA_per_A = 1000.0
        for i in self.data['Y']:
            y_list.append(i/mA_per_A)
        #  print(y_list)
        return y_list

