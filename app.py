import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly import graph_objs as go
from plots import plots
from arduino_interface import Arduino
from plots import Connection_State
import argparse

from utils import plot_output_mappings, format_x
from settings import settings


subtle_grey = '#b2b2b2'
plotbg_grey = '#212738'

class App:
    def __init__(self, testing):
        self.settings = settings
        self.arduino = Arduino(testing)
        self.arduino.start()

        self.app = dash.Dash(__name__)
        self.app.config['suppress_callback_exceptions'] = True
        self.app.layout = html.Div([
            build_title(),
            build_top_row(),
            build_bot_row(),
            dcc.Interval(
                id='graph-update',
                interval=1*1000
            )
        ], className="main")


        @self.app.callback(plot_output_mappings(plots),
                      [Input('graph-update', 'n_intervals')])
        def update_graphs(n):
            new_figs = []
            for name, plot in plots.items():
                if plot['disable']:
                    continue
                if plot['graph_type'] == go.Scatter:
                    new_data = go.Scatter(
                        x=format_x(plot['data']['X'], self.settings),
                        y=list(plot['data']['Y']),
                        name='Scatter',
                        mode='lines+markers'
                    )
                    if self.settings['autorange'] and plot['data']['X']:
                        xrange = [min(plot['data']['X']), max(plot['data']['X'])]
                    else:
                        xrange = self.settings['range']

                    new_layout = plotly.graph_objs.Layout(
                        xaxis=dict(range=xrange,
                                    #  tickformat='%X' if not self.settings['relative_timestamps'] else '-',
                                   showticklabels=self.settings['show_timestamps'],
                                   #  domain=(-5,0)
                                  ),
                        yaxis=dict(range=[min(plot['data']['Y']), max(plot['data']['Y'])],
                                   tickfont=dict(family='Open Sans', color=f'{subtle_grey}', size=10),
                                   nticks=4
                                   ),
                            
                        #  autosize=True,
                        #  height=200,
                        #  width=400,
                        # l r b t control the gap between the edge of the plot-container and the plot itself
                        # margin, padding
                        margin={
                            'l': 40,
                            'r': 30,
                            'b': 30,
                            't': 5,
                            'pad': 0
                        },
                        plot_bgcolor = plotbg_grey,
                        paper_bgcolor = plotbg_grey
                    )

                    new_figs.append({'data': [new_data], 'layout': new_layout})
                
                elif plot['graph_type'] == html.P:
                    if 'state' in name:
                        if plot['data']['Y']:
                            current_value_enum = Connection_State(plot['data']['Y'][-1])
                            new_value = current_value_enum.label
                        else:
                            new_value = Connection_State.UNKNOWN.label
                        new_className = 'connectionState '+new_value
                        new_figs.append(new_value)
                        new_figs.append(new_className)
                    else: # super janky TODO lil refactor
                        print(name)
                        try:
                            new_value = plot['data']['Y'][-1]
                        except IndexError:
                            new_value = None

                        new_figs.append(new_value)
            return new_figs

def section_header_generator(name):
    header = html.H3(name, className='section-header')
    return header

def section_plots_generator(plots, className='', id=''):
    section_plots = []
    config={'displayModeBar': False}
    for name, plot in plots.items():
        if not plot['disable']:
            new_plot_div = html.Div([
                html.H3(plot['title'], className='plot-title'),
                dcc.Graph(id=name, config=config) if plot['graph_type'] == go.Scatter else plot['graph_type'](id=name)
            ], className="graph-container")
            section_plots.append(new_plot_div)
    section_plots_div = html.Div(section_plots, className=f'section-plots {className}')
    return section_plots_div

def table_section_generator(name, id, plots, column_titles, column_className='table-column', column_title_className='column-title', item_className='table-item', leftmost_item_className='table-item', table_className='table-main', table_id=''):
    # rows should be ["name", element_id_col1, element_id_col2, ...]
        
    items_in_first_col = [html.P(column_titles[0], className=column_title_className)]

    for plot in plots.values():
        items_in_first_col.append(html.P(plot['title'], className=leftmost_item_className))
    first_col = html.Div(items_in_first_col, className=column_className)
    
    items_in_2nd_column = [html.P(column_titles[1], className=column_title_className)]

    for plot_id in plots.keys():
        items_in_2nd_column.append(html.P('', className=item_className, id=plot_id))
    
    second_col = html.Div(items_in_2nd_column, className=column_className)
    
    table_div = html.Div([first_col, second_col], className=table_className, id=table_id)
    section_header_div = section_header_generator(name)

    section_div = html.Div([section_header_div, table_div], className='section', id=id)
    return section_div

def plot_section_generator(name, id, plots, className='section', plots_className='', plots_id=''):
    elements = []
    elements.append(section_header_generator(name))
    elements.append(section_plots_generator(plots, plots_className, plots_id))
    return html.Div(elements, className=f'{className}', id=id)

def plots_subset_helper(keys):
    return dict((k, plots[k]) for k in keys if k in plots)

def build_pressure_mass_section():
    section_plots = plots_subset_helper(['pressure1', 'pressure2', 'pressure3', 'rocket_mass'])
    return plot_section_generator('Pressure and Mass', 'pressure-mass-section', section_plots)

def build_voltages_section():
    # I walked onto the google campus and just ooh im wet splooshin everywhere
    section_plots = plots_subset_helper(['rlcs_main_batt_mv', 'rlcs_actuator_batt_mv', 'bus_batt_mv', 'vent_batt_mv'])
    return table_section_generator('Voltages',
                                   'voltages-section',
                                   section_plots,
                                   ['Name', 'Value'])


def build_ignition_currents_section():
    section_plots = plots_subset_helper(['ign_pri_current','ign_sec_current'])
    return plot_section_generator('Ignition Currents', 'ignition-currents-section', section_plots)

def build_valves_section():
    section_plots = plots_subset_helper(['rvent_valve_state', 'injector_valve_state', 'rfill_valve_state', 'linac_state'])
    return table_section_generator('Valves',
                                   'valves-section',
                                   section_plots,
                                   ['Name', 'Value'],
                                   item_className='table-item table-item-fixed-width')

def build_top_row():
    row_div = html.Div([build_pressure_mass_section()], className='top-row')
    #  return row_div
    return row_div
    #  return build_pressure_mass_section()

def build_bot_row():
    sections = []
    sections.append(build_ignition_currents_section())
    sections.append(build_valves_section())
    sections.append(build_voltages_section())
    row_div = html.Div(sections, className='bot-row')
    return row_div

def build_title():
    title = html.H1('RLCS DAQ Plotting', id='main-title')
    header_div = html.Div([title], id='header-div')
    return header_div

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true')
    args = parser.parse_args()
    app = App(args.testing)
    app.app.run_server(debug=True)
