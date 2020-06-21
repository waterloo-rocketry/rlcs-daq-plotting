import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly import graph_objs as go
from arduino_interface import Arduino
from plots import Connection_State
import argparse
import datetime

from utils import format_x, flatten
from settings import Settings


subtle_grey = '#b2b2b2'
plotbg_grey = '#212738'

class App:
    def __init__(self, testing):
        self.settings = Settings()
        self.arduino = Arduino(testing)
        self.arduino.start()
        self.data = self.arduino.data

        self.app = dash.Dash(__name__)
        self.app.config['suppress_callback_exceptions'] = True
        self.app.layout = html.Div([
            build_title(),
            build_top_row(self.data),
            build_bot_row(self.data),
            dcc.Interval(
                id='graph-update',
                interval=(1/self.settings.dashboard_hz)*1000
            )
        ], className="main")
        
        # Update the plot data ie. x, y lists
        @self.app.callback([plot.get_fig_output() for plot in self.data.plots],
                      [Input('graph-update', 'n_intervals')])
        def update_plots(n):
            new_figs = []
            i=0
            for plot in self.data.plots:
                x,y=plot.extend_x_y()
                x=format_x(x)

                new_data = (dict(
                    x=[x],
                    y=[y]
                ), [0], self.settings.max_len)
                
                new_figs.append(new_data)
            return new_figs
        
        # Update the val field shown below each plot
        @self.app.callback(flatten([plot.get_val_output() for plot in self.data.plots]),
                      [Input('graph-update', 'n_intervals')]+
                           [Input(f'zero-{plot.id}', 'value') for plot in self.data.plots])
        def update_plot_vals(n, *zeros):
            new_vals = []
            for plot, zero in zip(self.data.plots, zeros):
                plot.update_zero(zero)
                cur_vals_dict = plot.get_cur_val()
                val = cur_vals_dict['val']
                adj = cur_vals_dict['adj']
                new_vals.append(val)
                new_vals.append(adj)
            return new_vals 

        @self.app.callback([voltage.get_mapped_output() for voltage in self.data.voltages],
                      [Input('graph-update', 'n_intervals')])
        def update_voltages(n):
            new_values = []
            for voltage_component in self.data.voltages:
                new_value = voltage_component.get_y_formatted()
                new_values.append(new_value)
            return new_values

        @self.app.callback(flatten([valve.get_mapped_output() for valve in self.data.valve_states]),
                      [Input('graph-update', 'n_intervals')])
        def update_valves(n):
            updates = []
            for valve_component in self.data.valve_states:
                if valve_component.data['Y']:
                    current_value_enum = Connection_State(valve_component.data['Y'][-1])
                    new_value = current_value_enum.label
                else:
                    new_value = Connection_State.UNKNOWN.label
                new_className = 'table-item-fixed-width table-item connectionState-'+new_value
                updates.append(new_value)
                updates.append(new_className)
            return updates

def section_header_generator(name):
    header = html.H3(name, className='section-header')
    return header

# Generates the plots in a section
def section_plots_generator(plots, className='', id=''):
    section_plots = []
    settings = Settings()
    config={'displayModeBar': settings.display_mode_bar}
    for plot in plots:
        # SUPER TEMP XRANGE WHILE FIGURING OUT HOW TO AUTORANGE WITH EXTENDDATA
        #  xrange = [datetime.datetime.now(), datetime.datetime.now()+datetime.timedelta(minutes=1)]
        #  yrange = plot.range
            
        graph_container_items = [
            html.H3(plot.title, className='plot-title'),
            dcc.Graph(id=plot.id, config=config, figure={
                'data': [{'x':[], 'y':[]}],
                'layout': go.Layout(
                    xaxis=dict(#range=xrange,
                               tickformat='%X.%f',
                               showticklabels=settings.show_timestamps,
                               nticks=3,
                               gridcolor="rgb(90, 90, 110)",
                               zerolinecolor="rgb(74, 134, 232)"
                              ),
                    yaxis=dict(#range=yrange,
                               tickfont=dict(family='Open Sans', color=f'{subtle_grey}', size=10),
                               nticks=4,
                               gridcolor="rgb(90, 90, 110)",
                               zerolinecolor="rgb(74, 134, 232)"
                               ),
                        
                    # l r b t control the gap between the edge of the plot-container and the plot itself
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
            })
        ]
        if settings.show_plot_footer:
            graph_container_items.append(generate_plot_footer(plot))
        new_plot_div = html.Div(graph_container_items, className="graph-container")
        section_plots.append(new_plot_div)
    section_plots_div = html.Div(section_plots, className=f'section-plots {className}')
    return section_plots_div

def generate_plot_footer(plot):
    val_label = html.P('Raw', className='plot-footer-label')
    val = html.P('', id=f'val-{plot.id}', className='plot-footer-value')
    val_div_items=[val_label, val]
    val_div = html.Div(val_div_items, className='plot-footer-subsection')
    
    adj_label = html.P('Adj.', className='plot-footer-label adj')
    adj = html.P('', id=f'adj-{plot.id}', className='plot-footer-value adj')
    adj_div_items=[adj_label, adj]
    adj_div = html.Div(adj_div_items, className='plot-footer-subsection adj')

    zero_label = html.P('Zero', className='plot-footer-label')
    zero_input = dcc.Input(
        id=f"zero-{plot.id}", type="number", className='plot-footer-value',
        debounce=True, placeholder="0",
    )
    zero_div_items = [zero_label, zero_input]
    zero_div = html.Div(zero_div_items, className='plot-footer-subsection')
    outer_div_items = [val_div, adj_div, zero_div]
    outer_div = html.Div(outer_div_items, className='plot-footer')
    return outer_div

def table_section_generator(name, id, plots, column_titles, column_className='table-column', column_title_className='column-title', item_className='table-item', leftmost_item_className='table-item-leftmost', table_className='table-main', table_id=''):
    # rows should be ["name", element_id_col1, element_id_col2, ...]
    
    settings = Settings()
    
    if settings.disable_table_column_titles:
        items_in_first_col = []
    else:
        items_in_first_col = [html.P(column_titles[0], className=column_title_className)]

    for plot in plots:
        items_in_first_col.append(html.P(plot.title, className=f'{item_className} {leftmost_item_className}'))
    first_col = html.Div(items_in_first_col, className=column_className)
    
    if settings.disable_table_column_titles:

        items_in_2nd_column = []
    else:
        items_in_2nd_column = [html.P(column_titles[1], className=column_title_className)]

    for plot in plots:
        items_in_2nd_column.append(html.P('', className=item_className, id=plot.id))
    
    second_col = html.Div(items_in_2nd_column, className=column_className)
    
    table_div = html.Div([first_col, second_col], className=table_className, id=table_id)
    section_header_div = section_header_generator(name)

    section_div = html.Div([section_header_div, table_div], className='section', id=id)
    return section_div

# Generates a section composed of plots
def plot_section_generator(name, id, plots, className='section', plots_className='', plots_id=''):
    elements = []
    elements.append(section_header_generator(name))
    elements.append(section_plots_generator(plots, plots_className, plots_id))
    return html.Div(elements, className=f'{className}', id=id)

def build_pressure_mass_section(data):
    return plot_section_generator('Pressure and Mass', 'pressure-mass-section', data.plots_pressure_mass)

def build_voltages_section(data):
    # I walked onto the google campus and just ooh im wet splooshin everywhere
    return table_section_generator('Battery Voltages',
                                   'voltages-section',
                                   data.voltages,
                                   ['Name', 'Value'],
                                   table_id='voltages-table')


def build_ignition_currents_section(data):
    return plot_section_generator('Ignition Currents', 'ignition-currents-section', data.plots_currents)

def build_valves_section(data):
    return table_section_generator('Valves',
                                   'valves-section',
                                   data.valve_states,
                                   ['Name', 'Value'],
                                   item_className='table-item',
                                   table_id='valves-table')

def build_top_row(data):
    row_div = html.Div([build_pressure_mass_section(data)], className='top-row')
    return row_div

def build_bot_row(data):
    sections = []
    sections.append(build_ignition_currents_section(data))
    sections.append(build_valves_section(data))
    sections.append(build_voltages_section(data))
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
    app.app.run_server(
        debug=True
    )
