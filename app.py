import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import ga

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

load_figure_template("solar")

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

SELECTION_RATE = 0.1
MUTATION_RATE = 0.01
ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789.,;:?!_+-*/ " + 16 * "a"

app.layout = html.Div([
    html.H1("String Learning using Genetic Algorithm"),
    html.Div([
        html.H4("Write your target string: "),
        dcc.Input(id='target', type='text', value='marcelina')
              ]),
    html.Div([
        html.H4("Choose the size of the population: "),
        dcc.Slider(
            id='population_size',
            min=20,
            max=500,
            step=10,
            value=250,
            tooltip={"placement": "bottom", "always_visible": True})
    ]),
    html.Div([
        html.H4("Choose maximal number of iterations: "),
        dcc.Slider(
                id='iterations',
                min=20,
                max=500,
                step=10,
                value=250,
                tooltip={"placement": "bottom", "always_visible": True}
            )
    ]),
    html.Button('Submit', id='submit_button', n_clicks=0),
    html.Div(id='output_container', children=[]),
    dcc.Graph(id="evaluation", figure={})
])


@app.callback(
    [Output(component_id='output_container', component_property='children'),
     Output(component_id='evaluation', component_property='figure')],
    [Input(component_id='target', component_property='value'),
     Input(component_id="population_size", component_property="value"),
     Input(component_id="iterations", component_property="value"),
     Input(component_id="submit_button", component_property="n_clicks")]
)

def upgrade_graph(target, population_size, iterations, n_clicks):
    if n_clicks>0:
        wynik, ev = ga.ga(population_size, SELECTION_RATE, MUTATION_RATE, ALPHABET, target, iterations)
        container = "The target chosen by user was: {}".format(target)
        fig = px.line(ev, x="generation", y="cost", hover_data=['generation', 'best chromosome', 'cost'], template="solar")
    else:
        container = ''
        fig = px.line()
    return container, fig


if __name__ == '__main__':
    app.run_server(debug=True)
