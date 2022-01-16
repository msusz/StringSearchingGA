import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
from dash.exceptions import PreventUpdate
import plotly.express as px

import ga

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("solar")
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])
app.title = "String Learning GA"

SELECTION_RATE = 0.1
MUTATION_RATE = 0.01
ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789. "

h_style={'text-align': 'center', 'padding': 10}


app.layout = html.Div(style={'font-family': 'Noto'}, children=[
    dbc.Row([
        dbc.Col([
            html.H1(["String Learning", html.Br(), "using", html.Br(), "Genetic Algorithm"], style=h_style),
            dbc.Row([
                html.H4("Write your target text: ", style=h_style),
                dcc.Input(id='target',
                          type='text',
                          placeholder='your text',
                          style={'text-align': 'center'},
                          maxLength=50)
            ]),
            html.Br(),
            html.H4("Choose the size of the population: ", style=h_style),
            dcc.Slider(
                id='population_size',
                min=20,
                max=500,
                step=10,
                value=250,
                tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            html.H4("Choose maximal number of iterations: ", style=h_style),
            dcc.Slider(
                id='iterations',
                min=20,
                max=500,
                step=10,
                value=250,
                tooltip={"placement": "bottom", "always_visible": True}),
            html.Br(),
            dbc.Row(html.Button('Submit', id='submit_button', n_clicks=0))
        ], width=4),

        dbc.Col([
            html.Div(dcc.Graph(id="evaluation", figure={}), style={'margin': 10}),
            html.Div(id='output_container', children=[], style={'text-align': 'center'})
        ], width=7)
    ])
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='evaluation', component_property='figure')],
    [State(component_id='target', component_property='value'),
     State(component_id="population_size", component_property="value"),
     State(component_id="iterations", component_property="value"),
     Input(component_id="submit_button", component_property="n_clicks")]
)
def update_output(target, population_size, iterations, n_clicks):
    if target is None or target is '':
        return '', {
            "layout": {
                "paper_bgcolor": "#002b36",
                "plot_bgcolor": "#002b36",
                "xaxis": {
                    "visible": False
                },
                "yaxis": {
                    "visible": False
                }
            }
        }
    else:
        wynik, ev = ga.ga(population_size, SELECTION_RATE, MUTATION_RATE, ALPHABET, target, iterations)
        container = [
            'The target text chosen by user was "{}"'.format(target),
            html.Br(),
            'Every generation has {} solutions.'.format(population_size),
            html.Br(),
            wynik
        ]
        fig = px.line(ev, x="generation", y="cost", hover_data=['generation', 'best chromosome', 'cost'],
                      template="solar")
        fig.update_layout(
            margin=dict(l=20, r=50, t=50, b=20)
        )

        return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
