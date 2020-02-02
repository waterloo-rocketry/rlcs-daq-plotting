import dash
from dash.dependencies import Output, Input, State
import dash_core_components as dcc
import dash_html_components as html
import plotly
from plotly import graph_objs as go

from graphs import graphs
from arduino_interface import Arduino
from graphs import Connection_State
import argparse

class App:
    def __init__(self, testing):
        self.arduino = Arduino(testing)
        self.arduino.start()

        self.app = dash.Dash(__name__)
        self.app.layout = html.Div(
            build_plots()
            +[
            dcc.Interval(
                id='graph-update',
                interval=1*1000
            )],className="main-container"
        )


        @self.app.callback([Output(name, graph['update_type']) for name, graph in graphs.items()],
                      [Input('graph-update', 'n_intervals')])
        def update_graphs(n):
            new_figs = []
            for name, graph in graphs.items():
                if graph['graph_type'] == go.Scatter:
                    new_data = go.Scatter(
                        x=list(graph['data']['X']),
                        y=list(graph['data']['Y']),
                        name='Scatter',
                        mode='lines+markers'
                    )
                    new_layout = plotly.graph_objs.Layout(
                        xaxis=dict(range=[min(graph['data']['X']), max(graph['data']['X'])]),
                        yaxis=dict(range=[min(graph['data']['Y']), max(graph['data']['Y'])]),
                        autosize=True,
                        height=200,
                        width=400,
                        margin=dict(t=0)
                    )

                    new_figs.append({'data': [new_data], 'layout': new_layout})
                
                elif graph['graph_type'] == dcc.Textarea:
                    new_value = Connection_State(graph['data']['Y'][-1]).label
                    new_figs.append(new_value)

            #  print(new_figs)

            return new_figs

def build_plots():
    plot_list = []
    
    for name, graph in graphs.items():
        new_plot_div = html.Div([
            html.H3(graph['title']),
            dcc.Graph(id=name) if graph['graph_type'] == go.Scatter else graph['graph_type'](id=name)
        ], className="graph-container")
        plot_list.append(new_plot_div)

    return plot_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--testing', action='store_true')
    args = parser.parse_args()
    app = App(args.testing)
    app.app.run_server(debug=True)
