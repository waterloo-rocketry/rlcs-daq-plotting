from collections import deque
import plotly.graph_objs as graph_objs

MAX_LEN = 150

graphs = {
    'pressure1': {
        'title': 'pressure1',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'pressure2': {
        'title': 'pressure2',
        'data':{'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': graph_objs.Scatter
    }}
''',
    'pressure3': { # used as rocket tank pressure for currents_line
        'title': 'pressure3',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,999],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'rocket_mass': {
        'title': 'rocket_mass',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,180],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'ign_pri_current': {
        'title': 'ignition primary current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'ign_sec_current': {
        'title': 'ignition secondary current',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,2],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'rfill_lsw_open': {
        'title': 'rfill_lsw_open',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'rfill_lsw_closed': {
        'title': 'rfill_lsw_closed',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'rvent_lsw_open': {
        'title': 'rvent_lsw_open',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'rvent_lsw_closed': {
        'title': 'rvent_lsw_open',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'linac_lsw_extend': {
        'title': 'rvent_lsw_open',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    },
    'linac_lsw_retract': {
        'title': 'rvent_lsw_retract',
        'data': {'X': deque(maxlen=MAX_LEN),'Y': deque(maxlen=MAX_LEN)},
        'range':[0,1],
        'type': int,
        'graph_type': graph_objs.Scatter
    }
}'''
