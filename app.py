import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque

from arduino_interface import Arduino
import argparse

class App:
    def __init__(self, testing):
        self.arduino = Arduino(testing)
        self.arduino.start()

        self.pressure1 = {'X': self.arduino.data['pressure1']['X'], 'Y': self.arduino.data['pressure1']['Y']}

        #  initial_trace = plotly.graph_objs.Scatter(
            #  x=list(self.pressure1['X']),
            #  y=list(self.pressure1['Y']),
            #  name='Scatter',
            #  mode='lines+markers'
        #  )
        
        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(
            [
                dcc.Graph(id='live-graph'
                          #  animate=True
                          #  figure={'data': [],#[initial_trace],
                                  #  'layout': go.Layout(
                                      #  xaxis=dict(range=[min(self.pressure1['X']), max(self.pressure1['X'])]),
                                      #  yaxis=dict(range=[min(self.pressure1['Y']), max(self.pressure1['Y'])]))
                                  #}
                          ),
                dcc.Interval(
                    id='graph-update',
                    interval=0.5*1000
                ),
            ]
        )


        @self.app.callback(Output('live-graph', 'figure'),
                      [Input('graph-update', 'n_intervals')],
                    [State('live-graph', 'figure')])
        def update_graph_scatter(n, figure):
            trace = plotly.graph_objs.Scatter(
                x=list(self.pressure1['X']),
                y=list(self.pressure1['Y']),
                name='Scatter',
                mode='lines+markers'
            )

            return {'data': [trace],
                    'layout': go.Layout(
                        xaxis=dict(range=[min(self.pressure1['X']), max(self.pressure1['X'])]),
                        yaxis=dict(range=[min(self.pressure1['Y']), max(self.pressure1['Y'])]))#30]))
                    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true')
    args = parser.parse_args()
    app = App(args.testing)
    app.app.run_server(debug=True)
