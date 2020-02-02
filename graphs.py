from collections import deque
import plotly.graph_objs as go
import dash_core_components as dcc
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

MAX_LEN = 15

graphs = {
    'pressure1': {
        'title': 'pressure1',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'pressure2': {
        'title': 'pressure2',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'pressure3': { # used as rocket tank pressure for currents_line
        'title': 'pressure3',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'rocket_mass': {
        'title': 'rocket_mass',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,180],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'ign_pri_current': {
        'title': 'ignition primary current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'ign_sec_current': {
        'title': 'ignition secondary current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': go.Scatter,
        'update_type': 'figure' #"figure" for graphs, "value" for text
    },
    'rfill_valve_state': {
        'title': 'remote fill valve state',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': dcc.Textarea,
        'update_type': 'value' #"figure" for graphs, "value" for text
    },
    'rvent_valve_state': {
        'title': 'remote vent valve state',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': dcc.Textarea,
        'update_type': 'value' #"figure" for graphs, "value" for text
    },
    'linac_state': {
        'title': 'linear actuator state',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'type': int,
        'graph_type': dcc.Textarea,
        'update_type': 'value' #"figure" for graphs, "value" for text
    }
}
