import dash_html_components as html
import dash_bootstrap_components as dbc
import warnings

warnings.filterwarnings("ignore")

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the COVID-19 Dashboard", className="text-center")
                    , className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='A dashboard for comparing COVID-19 data between different countries and the '
                                     'prediction of COVID-19 data. '
                            )
                    , className="mb-4")
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H5(
                children='This dashboard consists of four pages: Cases, Deaths, Cases & Deaths and SEIR simulation.'
                         ' The Cases and Deaths pages give an insight of the current state of COVID-19 cases and '
                         'deaths around the world and '
                         'let you compare data between countries of your choice with the measures each country took during the pandemic. '
                         ' The Cases & Deaths page focuses on comparing deaths and cases with measures taken in individual countries. '
                         'In addition, each of these pages provide a prediction of cases and deaths for a select few '
                         'countries. '
                         'The SEIR simulation gives you a chance to simulate the pandemic '
                         'and find how different '
                         'parameters can affect the results of the virus.')
            ], body=True, color="dark", outline=True), width=12, className="mb-5")
        ]),

        dbc.Row([
            dbc.Col(html.H5(
                children='Click on any of the tabs above to access the page of your choice.')
                , className="mb-5")
        ]),

        # dbc.Row([
        #     dbc.Col(dbc.Card(children=[html.H3(children='View COVID-19 Cases and Deaths',
        #                                        className="text-center"),
        #                                dbc.Row([dbc.Col(dbc.Button("Cases",
        #                                                            href="/apps/cases",
        #                                                            color="primary"),
        #                                                 className="mt-3"),
        #                                         dbc.Col(dbc.Button("Deaths",
        #                                                            href="/apps/deaths",
        #                                                            color="primary"),
        #                                                 className="mt-3"),
        #                                         dbc.Col(dbc.Button("Cases & Deaths",
        #                                                            href="/apps/cases_deaths",
        #                                                            color="primary"),
        #                                                 className="mt-3")
        #                                         ], justify="center"),
        #
        #                                ],
        #                      body=True, color="dark", outline=True)
        #             , width=4, className="mb-4"),
        #
        #     # dbc.Col(dbc.Card(children=[html.H3(children='View Predictions for COVID-19 Cases and Deaths',
        #     #                                    className="text-center"),
        #     #                            dbc.Row([dbc.Col(dbc.Button("Cases",
        #     #                                                        href="/apps/pred_cases",
        #     #                                                        color="primary"),
        #     #                                             className="mt-3"),
        #     #                                     dbc.Col(dbc.Button("Deaths",
        #     #                                                        href="/apps/pred_deaths",
        #     #                                                        color="primary"),
        #     #                                             className="mt-3"),
        #     #                                     dbc.Col(dbc.Button("Deaths",
        #     #                                                        href="/apps/pred_deaths",
        #     #                                                        color="primary"),
        #     #                                             className="mt-3")], justify="center")
        #     #                            ],
        #     #                  body=True, color="dark", outline=True)
        #     #         , width=4, className="mb-4"),
        #
        #     dbc.Col(dbc.Card(children=[html.H3(children='Simulate the effect of COVID-19',
        #                                        className="text-center"),
        #                                dbc.Button("SEIR Simulation",
        #                                           href="/apps/SEIR_sim",
        #                                           color="primary",
        #                                           className="mt-3"),
        #
        #                                ],
        #                      body=True, color="dark", outline=True)
        #             , width=4, className="mb-4")
        # ], className="mb-5"),

        html.H6("Data for this dashboard was obtained from Our World in Data and the Center for Systems Science and "
                "Engineering (CSSE) at Johns Hopkins University")

        # html.A("Data for this dashboard was obtained from Our World in Data and the Center for Systems Science and "
        #        "Engineering (CSSE) at Johns Hopkins University",
        #        href="")

    ])

])
