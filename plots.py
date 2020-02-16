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

pressure_mass_plots = [
    {
        'id': 'pressure1',
        'title': 'Fill Tank Pressure',
        'range':[0,999],
        'zero': None,
        'disable': False
    },
    {
        'id': 'pressure2',
        'title': 'Fill Line Pressure',
        'range':[0,999],
        'zero': None,
        'disable': False
    },
    {
        'id': 'pressure3',
        'title': 'Rocket Tank Pressure',
        'range':[0,999],
        'zero': None,
        'disable': False
    },
    {
        'id': 'rocket_mass',
        'title': 'Rocket Mass (kg)',
        'range':[0,999],
        'zero': None,
        'disable': False
    }
]

current_plots = [
    {
        'id': 'ign_pri_current',
        'title': 'Ignition Primary Current',
        'range':[0,2000],
        'zero': None,
        'disable': False
    },
    {
        'id': 'ign_sec_current',
        'title': 'Ignition Secondary Current',
        'range':[0,2000],
        'zero': None,
        'disable': False
    }
]

valve_states = [
    {
        'id': 'rfill_valve_state',
        'title': 'Remote Fill',
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'disable': False
    },
    {
        'id': 'rvent_valve_state',
        'title': 'Remote Vent',
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'disable': False
    },
    {
        'id': 'injector_valve_state',
        'title': 'Injector',
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'disable': False
    },
    {
        'id': 'linac_state',
        'title': 'Fill Disconnect', #TODO double check that this linac is actually for the fill arm
        # technically range is just integers 1-4, I just use the enum to show what it represents
        'range':[Connection_State(1).value, Connection_State(4).value],
        'disable': False
    }
]

voltages = [
    {
        'id': 'rlcs_main_batt_mv',
        'title': 'RLCS Tower Main',
        'range':[0,2000],
        'disable': False
    },
    {
        'id': 'rlcs_actuator_batt_mv',
        'title': 'RLCS Tower Actuator',
        'range':[0,2000],
        'disable': False
    },
    {
        'id': 'bus_batt_mv',
        'title': 'RocketCAN Bus',
        'range':[0,2000],
        'disable': False
    },
    {
        'id': 'vent_batt_mv',
        'title': 'RocketCAN Vent',
        'range':[0,2000],
        'disable': False
    }
]

#  misc_dash_items = {
    #  {
        #  'id': 'num_boards_connected',
        #  'title': 'Number of Boards on RocketCAN',
        #  'range':[0,5],
        #  'disable': True
    #  }
#  }
