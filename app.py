import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly

from graphs import graphs
from arduino_interface import Arduino
import argparse

class App:
    def __init__(self, testing):
        self.arduino = Arduino(testing)
        self.arduino.start()

        self.app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = html.Div([
             #html.Div([
            for graph in graphs:
                html.Div([
                    html.H3(graph.title),
                    dcc.Graph(id=graph.name),
                ], className="graph-container"),

            dcc.Interval(
                id='graph-update',
                interval=0.5*1000
            )],className="main-container"
        )


        @self.app.callback([Output(graph.name, 'figure') for graph in graphs],
                      [Input('graph-update', 'n_intervals')])
        def update_graph_scatter(n):
            new_figs = []
            for graph in graphs:
                new_data = graph['graph_type'](
                    x=list(graph['data']['X']),
                    y=list(graph['data']['Y']),
                    name='Scatter',
                    mode='lines+markers'
                )
                new_layout = plotly.graph_objs.Layout(
                    xaxis=dict(range=[min(graph['data']['X']), max(graph['data']['X'])]),
                    yaxis=dict(range=[min(graph['data']['Y']), max(graph['data']['Y'])])
                )

                new_figs.append({'data': new_data, 'layout': new_layout})

            return new_figs
            #  trace1 = plotly.graph_objs.Scatter(
                #  x=list(self.pressure1['X']),
                #  y=list(self.pressure1['Y']),
                #  name='Scatter',
                #  mode='lines+markers'
            #  )
            #  trace2 = plotly.graph_objs.Scatter(
                #  x=list(self.pressure2['X']),
                #  y=list(self.pressure2['Y']),
                #  name='Scatter',
                #  mode='lines+markers'
            #  )

            #  return [{'data': [trace1],
                    #  'layout': go.Layout(
                        #  xaxis=dict(range=[min(self.pressure1['X']), max(self.pressure1['X'])]),
                        #  yaxis=dict(range=[min(self.pressure1['Y']), max(self.pressure1['Y'])]))#30]))
                    #  },
                    #  {'data': [trace2],
                    #  'layout': go.Layout(
                        #  xaxis=dict(range=[min(self.pressure2['X']), max(self.pressure2['X'])]),
                        #  yaxis=dict(range=[min(self.pressure2['Y']), max(self.pressure2['Y'])]))#30]))
                    #  }
                    #  ]

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true')
    args = parser.parse_args()
    app = App(args.testing)
    app.app.run_server(debug=True)
