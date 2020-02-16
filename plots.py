from collections import deque
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from utils import LabledEnum

# Decoding the enum from the arduino side which is defined by
#  typedef enum {
    #  DAQ_VALVE_OPEN,
    #  DAQ_VALVE_CLOSED,
    #  DAQ_VALVE_UNK,
    #  DAQ_VALVE_ILLEGAL
#  } valve_state_t;

class Connection_State(LabledEnum):
    OPEN = (1, "Open")
    CLOSED = (2, "Closed")
    UNKNOWN = (3, "Unknown")
    DAQ_VALVE_ILLEGAL = (4, "Illegal")

MAX_LEN = 200 # max number of data points stored and displayed


'''
GRAPH CATEGORIES

??
Number of Boards on RocketCAN (num_boards_connected)

Pressure and Mass
- should def be big graphs
    Fill Tank Pressure (pressure1)
    Fill Line Pressure (pressure2)
    Rocket Tank Pressure (pressure3)
    Rocket Mass (rocket_mass)
    
Voltages
    RLCS Tower Main Battery Voltage (rlcs_main_batt_mv)
    RLCS Tower Actuator Voltage (rlcs_actuator_batt_mv)
    RocketCAN Bus Battery Voltage (bus_batt_mv)
    RocketCAN Vent Battery Voltage (vent_batt_mv)
    -no point of these being graphs

Ignition Currents
    Ignition Primary Current (ign_pri_current)
    Ignition Secondary Current (ign_sec_current)

Valves
    Remote Vent Valve State (rvent_valve_state)
    Injector Valve State (injector_valve_state)
    Remote Fill Valve State (rfill_valve_state)
    Fill Arm Linear Actuator State (linac_state)

Colors: UW Black and Gold

Settings ideas:
-Zero pressure and mass
-Click a button and store that
-Do time as 0, t-n (seconds)
-calculate max_len using a variable for time to store
'''

plots = {
    'pressure1': {
        'title': 'Fill Tank Pressure',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[500,505],
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'pressure2': {
        'title': 'Fill Line Pressure',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[35,52], # usually 0, 999
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'pressure3': { # used as rocket tank pressure for currents_line
        'title': 'Rocket Tank Pressure',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,3], # 999 usually
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'rocket_mass': {
        'title': 'Rocket Mass (kg)',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,18], # 180 usually
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'num_boards_connected': {
        'title': 'Number of Boards on RocketCAN',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,5],
        'type': int,
        'graph_type': go.Scatter,
        'disable': True
    },
    # should be small plots for ign current
    'ign_pri_current': {
        'title': 'Ignition Primary Current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'ign_sec_current': {
        'title': 'Ignition Secondary Current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': go.Scatter,
        'disable': False
    },
    'rlcs_main_batt_mv': {
        'title': 'RLCS Tower Main Battery Voltage',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2], #TODO: Update range
        'type': int,
        'graph_type': html.P,
        'disable': False
    },
    'rlcs_actuator_batt_mv': {
        'title': 'RLCS Tower Actuator Voltage',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2], #TODO: Update range
        'type': int,
        'graph_type': html.P,
        'disable': False
    },
    'bus_batt_mv': {
        'title': 'RocketCAN Bus Battery Voltage',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2], #TODO: Update range
        'type': int,
        'graph_type': html.P,
        'disable': False
    },
    'vent_batt_mv': {
        'title': 'RocketCAN Vent Battery Voltage',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2], #TODO: Update range
        'type': int,
        'graph_type': html.P,
        'disable': False
    },
    'rfill_valve_state': {
        'title': 'Remote Fill Valve State',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': html.P, # dcc.Textarea,
        'disable': False
    },
    'rvent_valve_state': {
        'title': 'Remote Vent Valve State',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': html.P, # dcc.Textarea,
        'disable': False
    },
    'injector_valve_state': {
        'title': 'Injector Valve State',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': html.P, # dcc.Textarea,
        'disable': False
    },
    'linac_state': {
        'title': 'Fill Arm Linear Actuator State', #TODO double check that this linac is actually for the fill arm
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': html.P, # dcc.Textarea,
        'disable': False
    }
}
