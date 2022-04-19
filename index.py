import base64

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import warnings

# must add this line in order for the app to be deployed successfully on Heroku
from app import app
from app import server
# import all pages in the app
from apps import cases, deaths, cases_deaths, SEIR_sim, homepage

warnings.filterwarnings("ignore")

# image source
# PATH = pathlib.Path(__file__).parent
# DATA_PATH = PATH.joinpath("./assets").resolve()
# image_path = DATA_PATH.joinpath("coronavirus.png")

image_filename = 'assets/coronavirus.png'
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        # dbc.Col(html.Img(src='assets/coronavirus.png', height="30px")),
                        dbc.Col(html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), height="30px")),
                        dbc.Col(dbc.NavbarBrand("COVID-19 DASHBOARD", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/homepage"
            )
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

tabs_links = html.Div([

    # html.Div([], className='col-2', style={'background-color': '#e3e3e3'}),

    dbc.Row(children=[

        dbc.Col(width=1, style={'background-color': '#e3e3e3'}),
        dbc.Col(width=1, style={'background-color': '#e3e3e3'}),

        dbc.Col(children=[
            dcc.Link(
                html.H4(children='Cases'),
                href='/apps/cases'
            )
        ], style={'background-color': '#e3e3e3'},
            width=2),

        dbc.Col(children=[
            dcc.Link(
                html.H4(children='Deaths'),
                href='/apps/deaths'
            )
        ], style={'background-color': '#e3e3e3'},
            width=2),

        dbc.Col(children=[dcc.Link(
            html.H4(children='Cases & Deaths'),
            href='/apps/cases_deaths'
        )
        ], style={'background-color': '#e3e3e3'},
            width=2),

        dbc.Col(width=1, style={'background-color': '#e3e3e3'}),

        dbc.Col(children=[dcc.Link(
            html.H4(children='SEIR Simulation'),
            href='/apps/SEIR_sim'
        )
        ], style={'background-color': '#e3e3e3'},
            width=2),

        dbc.Col(width=1, style={'background-color': '#e3e3e3'}),
        dbc.Col(width=0.65, style={'background-color': '#e3e3e3'})
    ])
])


# embedding the navigation bar

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    tabs_links,
    html.Div(id='page-content', children=[])
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/cases':
        return cases.layout
    elif pathname == '/apps/deaths':
        return deaths.layout
    elif pathname == '/apps/cases_deaths':
        return cases_deaths.layout
    elif pathname == '/apps/SEIR_sim':
        return SEIR_sim.layout
    else:
        return homepage.layout


if __name__ == '__main__':
    app.run_server(debug=True)
