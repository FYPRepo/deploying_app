import datetime as dt

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import warnings

from apps import get_data as gd, graphs
from app import app

warnings.filterwarnings("ignore")

# list of graphs from graphs.py
# globe to show total COVID-19 deaths per country: globe
globe_de = graphs.globe_deaths
# choropleth to show covid-19 deaths per month: choropleth_month
choropleth_month_de = graphs.choropleth_month_deaths
# choropleth to show covid-19 deaths per year: choropleth_year
choropleth_year_de = graphs.choropleth_year_deaths
# line graph for user to compare covid-19 deaths between countries along with measures taken: comparison_line
# line_graph = go.Figure()


countries_de = gd.countries
all_data_de = gd.all_data
measures_de = ['Vaccination Policy', 'Face Covering Measures',
               'Border Control Measures', 'Stay At Home Measures']

pred_countries_d = ['Greece', 'Malaysia',
                    'South Africa', 'Germany',
                    'Japan', 'Afghanistan',
                    'Australia',
                    'Poland']

dd_options_de = []
for key in countries_de:
    dd_options_de.append({
        'label': key,
        'value': key
    })

dd_options_pred_d = []
for key in pred_countries_d:
    dd_options_pred_d.append({
        'label': key,
        'value': key
    })

YEARS_d = [2020, 2021, 2022]

date_today_d = dt.datetime.today().strftime("%Y-%m-%d")
date_today_d = pd.to_datetime(date_today_d)

date_tomorrow_d = dt.date.today() + dt.timedelta(days=1)
date_tomorrow_d = date_tomorrow_d.strftime("%Y-%m-%d")
date_tomorrow_d = pd.to_datetime(date_tomorrow_d)

# ========================================= APPLICATION LAYOUT =========================================================

# app = dash.Dash(__name__)

tabs_styles_de = {
    'height': '44px'
}
tab_style_de = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style_de = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#000000',
    'color': 'white',
    'padding': '6px'
}

layout = html.Div(children=[

    dbc.Container([

        html.Br(),

        html.H1(children='COVID-19 Current Deaths and Prediction',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("View the current number of COVID-19 deaths around the world, "
                "and compare deaths between different countries along with the measures"
                " each country took to battle COVID-19."),

        html.Br(),
        html.Hr(),

        html.H2(children='Current Deaths',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        dcc.Graph(id="globe_de", figure=globe_de),

        html.Br(),

        dcc.Tabs(id="tabs-graph_de", value='tab-1-graph_de', children=[
            dcc.Tab(label='Deaths Per Month', value='tab-1-graph_de', style=tab_style_de,
                    selected_style=tab_selected_style_de),
            dcc.Tab(label='Deaths Per Year', value='tab-2-graph_de', style=tab_style_de,
                    selected_style=tab_selected_style_de),
        ]),
        html.Div(id='tabs-content-graph_de'),

        html.Br(),

        html.Hr(),

        html.H3(children='COVID-19 Measures vs Deaths',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("Let's take a look at how the different countries around the world implemented the three measures of "
                "Stay at Home, Face Coverings and Border Control as well as their vaccination policies and how all of "
                "this has "
                " affected COVID-19 deaths."),

        html.H4("The strictness at which each measure and the policy have been implemented is"
                " measured in levels from 0 to 4 as follows: "),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(children=[dbc.Card(children=[
                html.H5("Stay Home Measures", style={'textAlign': 'center'}),
                html.H5("0 - No measures"),
                html.H5("1 - Recommended"),
                html.H5("2 - Required with Exceptions"),
                html.H5("3 - Required with Minimal Exceptions"),
            ], body=True, color="dark", outline=True)]),

            dbc.Col(children=[dbc.Card(children=[
                html.H5("Face Covering Measures", style={'textAlign': 'center'}),
                html.H5("0 - No measures"),
                html.H5("1 - Recommended"),
                html.H5("2- Required in some shared/public spaces"),
                html.H5("3- Required in all shared/public spaces"),
                html.H5("4- Required outside  at all times")
            ], body=True, color="dark", outline=True)]),

            dbc.Col(children=[dbc.Card(children=[
                html.H5("Border Closure Measures", style={'textAlign': 'center'}),
                html.H5("0 - No measures"),
                html.H5("1 - Screening"),
                html.H5("2 - Quarantine arrivals from high-risk regions"),
                html.H5("3 - Ban on high-risk regions"),
                html.H5("4 - Total border closure")
            ], body=True, color="dark", outline=True)]),

            dbc.Col(children=[dbc.Card(children=[
                html.H5("Vaccination Policy By Availability", style={'textAlign': 'center'}),
                html.H5("0 - No availability"),
                html.H5("1 - ONE of: key workers/ clinically vulnerable groups/ elderly "
                        "groups"),
                html.H5("2 - TWO of: key workers/ clinically vulnerable groups/ elderly "
                        "groups"),
                html.H5("3 -  ALL of: key workers/ clinically vulnerable groups/ elderly groups"),
                html.H5(
                    "4 - All three, plus select broad groups/ages"),
                html.H5("5 - Universal availability")
            ], body=True, color="dark", outline=True)])
        ]),

        html.Br(),

        dbc.Row(children=[

            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select countries to compare: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_de',
                        options=dd_options_de,
                        value=['Malaysia'],
                        multi=True
                    )
                ])
            ),

            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select measure to compare: ")),
                    dcc.Dropdown(
                        id='measures_dropdown_de',
                        options=[{'label': i, 'value': i} for i in measures_de],
                        value='Stay At Home Measures',
                        multi=False
                    )
                ])
            )
        ]),

        html.Br(),

        dcc.Graph(id='comparison-line_de', figure={}),

        html.Br(),

        html.H4("Compare the COVID-19 deaths between two countries against the strictness level of all measures and"
                " their vaccination policy."),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select first country: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_stacked_de',
                        options=dd_options_de,
                        value='Malaysia',
                        multi=False
                    ),
                    html.Br(),
                    dcc.Graph(id="stacked_bar1_de", figure={})
                ])
            ),

            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select second country: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_stacked1_de',
                        options=dd_options_de,
                        value='New Zealand',
                        multi=False
                    ),
                    html.Br(),
                    dcc.Graph(id="stacked_bar2_de", figure={})
                ])
            )

        ]),

        html.Br(),
        html.Hr(),

        html.H1(children='Prediction of COVID-19 Deaths',
                style={'textAlign': 'center'}),
        html.Hr(),

        html.H4("View the prediction of COVID-19 deaths for the next 60 days."),

        html.Br(),

        # html.H3("Assuming each country keeps the following measures:"),

        html.Div(children=[

            dbc.Row(children=[
                dbc.Col(children=[
                    html.H6(html.B("Select the type of prediction: ")),
                    dcc.RadioItems(
                        id='chart_type_d',
                        options=[{'label': i, 'value': i} for i in ['Cumulative', 'Per Day']],
                        value='Cumulative',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text']
                                    "margin-right": "20px"}
                    )
                ]),

                dbc.Col(children=[
                    html.H6(html.B("Select the type of y-axis: ")),
                    dcc.RadioItems(
                        id='yaxis_type_d',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text']
                                    "margin-right": "20px"}
                    )
                ])

            ]),

            html.H6(html.B("Select country: ")),
            dcc.Dropdown(
                id='countries_dropdown_pred_d',
                options=dd_options_pred_d,
                value=['Malaysia'],
                multi=True
            ),

            html.Br(),

            dash_table.DataTable(
                id='cases_table_de',
                columns=[
                    {"name": "Country", "id": "Country"},
                    {"name": "Today's deaths", "id": "Today's deaths"},
                    {"name": "Tomorrow's deaths", "id": "Tomorrow's deaths"},
                    {"name": "Total deaths in 2022", "id": "Total deaths in 2022"}
                ],
                style_cell_conditional=[
                    {'if': {'column_id': 'Country'},
                     'width': '5px'},
                    {'if': {'column_id': 'Today\'s deaths'},
                     'width': '5px'},
                    {'if': {'column_id': 'Tomorrow\'s deaths'},
                     'width': '5px'},
                    {'if': {'column_id': 'Total deaths in 2022'},
                     'width': '5px'}
                ],
                style_cell={'textAlign': 'left',
                            'fontSize': 16, 'font-family': 'Helvetica'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            ),

            dcc.Graph(id='pred_line_d', figure={}),

            html.Br(),

            html.H4("This prediction is assuming each country keeps the following measures:"),

            html.Br(),

            dash_table.DataTable(
                id='measures_table_de',
                columns=[
                    {"name": "Country", "id": "Country"},
                    {"name": "Face Covering Measures", "id": "Face Covering Measures"},
                    {"name": "Border Closure Measures", "id": "Border Closure Measures"},
                    {"name": "Stay At Home Measures", "id": "Stay At Home Measures"},
                    {"name": "Vaccination Policy", "id": "Vaccination Policy"},
                    {"name": "Boosters Being Given?", "id": "Boosters Being Given?"},
                ],
                style_cell_conditional=[
                    {'if': {'column_id': 'Country'},
                     'width': '5px'}
                ],
                style_cell={'textAlign': 'left',
                            'fontSize': 16, 'font-family': 'Helvetica'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            ),

            html.Br(),

            html.H4("Compare COVID-19 deaths of a country between two years."),

            html.Br(),

            html.H6(html.B("Select country: ")),
            html.Div(children=[dcc.Dropdown(
                id='countries_dropdown_d_bar',
                options=dd_options_pred_d,
                value='Malaysia',
                multi=False
            )], style=dict(width='60%')),

            html.Br(),

            dbc.Row(
                [

                    dbc.Col(width=1),

                    dbc.Col(html.Div(children=[
                        html.H6(html.B("Select first year: ")),
                        dcc.Slider(
                            id='years_slider1_d',
                            min=min(YEARS_d),
                            max=max(YEARS_d),
                            value=min(YEARS_d),
                            marks={str(year): str(year) for year in YEARS_d},
                            updatemode='drag'
                        )
                    ]), width=4),

                    dbc.Col(width=1),

                    dbc.Col(html.Div(children=[
                        html.H6(html.B("Select second year: ")),
                        dcc.Slider(
                            id='years_slider2_d',
                            min=min(YEARS_d),
                            max=max(YEARS_d),
                            value=max(YEARS_d),
                            marks={str(year): str(year) for year in YEARS_d},
                            updatemode='drag'
                        ),
                    ]), width=4)
                ]),

            html.Br(),

            dbc.Row(
                [
                    dbc.Col(children=[
                        dcc.Graph(id='comp_bar1_d', figure={})
                    ]),

                    dbc.Col(children=[
                        dcc.Graph(id='comp_bar2_d', figure={})
                    ])
                ]
            )

        ])
    ], fluid=True)
])


# ======================================= APPLICATION CALLBACKS ========================

@app.callback(

    Output('comparison-line_de', 'figure'),

    [
        Input('countries_dropdown_de', 'value'),
        Input('measures_dropdown_de', 'value'),
    ]

)
def update_graph(
        countries_choice_de,
        measures_choice_de
):
    fig_de = go.Figure()
    traces_de = []
    for i in countries_choice_de:
        data_country_de = all_data_de[all_data_de['location'] == i]
        data_monthly_strictness_de = gd.get_df_all_measures_month(data_country_de)

        traces_de.append(go.Scatter(x=data_monthly_strictness_de['date'],
                                    y=data_monthly_strictness_de['Total Deaths'],
                                    mode='lines',
                                    # line=dict(color='rgba(0,0,200,0.7)'),
                                    name=str(i)))

        fig_de.add_traces(px.scatter(data_monthly_strictness_de,
                                     x=data_monthly_strictness_de['date'],
                                     y=data_monthly_strictness_de['Total Deaths'],
                                     color=measures_choice_de,
                                     hover_data=['date', 'Total Deaths', 'location'],
                                     labels={
                                         'date': 'Date',
                                         'deaths_new': 'Confirmed Deaths',
                                         'location': 'Country'
                                     }).data)

    fig_de.add_traces(traces_de)
    fig_de.update_layout(coloraxis_colorbar_x=-0.15,
                         coloraxis_colorbar=dict(
                             title="Strictness of <br> Measures"
                         ),
                         plot_bgcolor='rgba(234,234,242,255)',
                         template="seaborn"
                         )

    title_de = ', '.join(countries_choice_de)
    title_de = 'COVID-19 Deaths: ' + title_de
    fig_de.update_layout(title=title_de)
    fig_de.update_layout(hovermode="x unified")

    # if tab_de == 'tab-1-graph_de':
    #     return html.Div([
    #         html.H3('COVID-19 Deaths Per Month'),
    #         dcc.Graph(
    #             id='graph-1-tabs-dcc_de',
    #             figure=choropleth_month_de
    #         )
    #     ]), fig_de, stacked_bar1_de, stacked_bar2_de
    # elif tab_de == 'tab-2-graph_de':
    #     return html.Div([
    #         html.H3('COVID-19 Deaths Per Year'),
    #         dcc.Graph(
    #             id='graph-2-tabs-dcc',
    #             figure=choropleth_year_de
    #         )
    #     ])
    return fig_de


@app.callback(
    Output('tabs-content-graph_de', 'children'),
    Input('tabs-graph_de', 'value')
)
def update_graph(tab_de):
    if tab_de == 'tab-1-graph_de':
        return html.Div([
            # html.H3('COVID-19 Deaths Per Month'),
            dcc.Graph(
                id='graph-1-tabs-dcc_de',
                figure=choropleth_month_de
            )
        ])
    elif tab_de == 'tab-2-graph_de':
        return html.Div([
            # html.H3('COVID-19 Deaths Per Year'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure=choropleth_year_de
            )
        ])


@app.callback(
    [Output('stacked_bar1_de', 'figure'),
     Output('stacked_bar2_de', 'figure')],

    [Input('countries_dropdown_stacked_de', 'value'),
     Input('countries_dropdown_stacked1_de', 'value')]

)
def update_graph(countries_stacked1_de, countries_stacked2_de):
    stacked_bar1_de = graphs.get_stacked_bar_line(countries_stacked1_de, 'Total Deaths', 'Confirmed Deaths',
                                                  'Confirmed Deaths')

    stacked_bar1_de.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    stacked_bar2_de = graphs.get_stacked_bar_line(countries_stacked2_de, 'Total Deaths', 'Confirmed Deaths',
                                                  'Confirmed Deaths')

    stacked_bar2_de.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return stacked_bar1_de, stacked_bar2_de


@app.callback(
    [Output('measures_table_de', 'data'),
     Output('cases_table_de', 'data')],

    Input('countries_dropdown_pred_d', 'value')
)
def update_graph(countries_dropdown_de):
    global measures_table_d, deaths_table

    country_measures_d = {}
    country_measures_d = pd.DataFrame(country_measures_d)

    deaths_countries_df = {}
    deaths_countries_df = pd.DataFrame(deaths_countries_df)

    for countries in countries_dropdown_de:
        df_country = graphs.combine_pred_avaible_deaths(countries)

        df_today = df_country[df_country['ds'] == date_today_d]
        df_today = round(df_today['yhat'], 0).astype(int)
        today_deaths = df_today.iloc[-1].tolist()
        today_deaths = str(today_deaths)
        today_deaths = '{:,}'.format(int(today_deaths))
        # print("============== today last row deaths ================")
        # print(today_last_row)
        # print("============================================")
        # today_deaths = today_last_row['yhat']
        # print("============== today deaths ================")
        # print(today_deaths)
        # print("============================================")
        # today_deaths = today_deaths.astype(int)
        # today_deaths = '{:,}'.format(int(today_deaths))

        df_tomorrow = df_country[df_country['ds'] == date_tomorrow_d]
        df_tomorrow = round(df_tomorrow['yhat'], 0).astype(int)
        tomorrow_deaths = df_tomorrow.iloc[-1].tolist()
        tomorrow_deaths = str(tomorrow_deaths)
        tomorrow_deaths = '{:,}'.format(int(tomorrow_deaths))


        # tomorrow_last_row = df_tomorrow.tail(1)
        # print("============== tomorrow last row deaths ================")
        # print(tomorrow_last_row)
        # print("============================================")
        # tomorrow_deaths = tomorrow_last_row['yhat']
        # print("============== tomorrow deaths ================")
        # print(tomorrow_deaths)
        # print("============================================")
        # tomorrow_deaths = tomorrow_deaths.astype(int)
        # tomorrow_deaths = '{:,}'.format(int(tomorrow_deaths))

        # tomorrow_deaths = FRGD.forest_reg(countries, 2)
        # tomorrow_deaths = '{:,}'.format(int(tomorrow_deaths))

        total_deaths = graphs.get_total_deaths_2022(countries)
        total_deaths = '{:,}'.format(int(total_deaths))

        deaths = {'Country': [countries],
                  'Today\'s deaths': [today_deaths],
                  'Tomorrow\'s deaths': [tomorrow_deaths],
                  'Total deaths in 2022': [total_deaths]}

        deaths_df = pd.DataFrame(deaths)
        deaths_countries_df = pd.concat([deaths_countries_df, deaths_df],
                                        ignore_index=True, sort=False)

        measures_table_d = graphs.current_measures
        country_measure_d = measures_table_d[measures_table_d['Country'] == countries]
        country_measures_d = pd.concat([country_measures_d, country_measure_d],
                                       ignore_index=True, sort=False)

        measures_table_d = country_measures_d
        deaths_table = deaths_countries_df

    return measures_table_d.to_dict(orient='records'), deaths_table.to_dict(orient='records')


@app.callback(
    # [
    Output('pred_line_d', 'figure'),
    # Output('today_deaths_d', 'children'),
    # Output('tomorrow_deaths_d', 'children'),
    # Output('total_2022_d', 'children')
    # ],

    [Input('chart_type_d', 'value'),
     Input('yaxis_type_d', 'value'),
     Input('countries_dropdown_pred_d', 'value')
     ]
)
def update_graph(chart_type_d, yaxis_type_d, countries_dropdown_d):
    # today_deaths_d = 0
    # tomorrow_deaths_d = 0
    # total_deaths_d = 0

    # for countries in countries_dropdown_d:
    #     df_country_d = graphs.combine_pred_avaible_deaths(countries)
    #
    #     df_today_d = df_country_d[df_country_d['ds'] == date_today_d]
    #     today_deaths_d = df_today_d['yhat'].astype(int)
    #     today_deaths_d = '{:,}'.format(int(today_deaths_d))
    #
    #     df_tomorrow_d = df_country_d[df_country_d['ds'] == date_tomorrow_d]
    #     tomorrow_deaths_d = df_tomorrow_d['yhat'].astype(int)
    #     tomorrow_deaths_d = '{:,}'.format(int(tomorrow_deaths_d))
    #
    #     total_deaths_d = graphs.get_total_deaths_2022(countries)
    #     total_deaths_d = '{:,}'.format(int(total_deaths_d))

    if chart_type_d == 'Cumulative':
        pred_line_deaths = graphs.get_pred_line_cumm_deaths(countries_dropdown_d, yaxis_type_d)
    else:
        pred_line_deaths = graphs.get_pred_line_day_deaths(countries_dropdown_d, yaxis_type_d)

    return pred_line_deaths
    # return today_deaths_d, tomorrow_deaths_d, total_deaths_d


@app.callback(
    [Output('comp_bar1_d', 'figure'),
     Output('comp_bar2_d', 'figure')],

    [Input('countries_dropdown_d_bar', 'value'),
     Input('years_slider1_d', 'value'),
     Input('years_slider2_d', 'value')]
)
def update_graph(countries_dropdown_d_bar, years_slider1_d, years_slider2_d):
    bar_chart_deaths1 = graphs.get_bar_current(countries_dropdown_d_bar, years_slider1_d, 'new_deaths')
    bar_chart_deaths2 = graphs.get_bar_current(countries_dropdown_d_bar, years_slider2_d, 'new_deaths')

    return bar_chart_deaths1, bar_chart_deaths2

#
# if __name__ == '__main__':
#     app.run_server(debug=True)
