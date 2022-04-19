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
# globe to show total COVID-19 cases per country: globe
globe = graphs.globe_cases
# choropleth to show covid-19 cases per month: choropleth_month
choropleth_month = graphs.choropleth_month_cases
# choropleth to show covid-19 cases per year: choropleth_year
choropleth_year = graphs.choropleth_year_cases
# line graph for user to compare covid-19 cases between countries along with measures taken: comparison_line
line_graph = go.Figure()

countries = gd.countries
all_data = gd.all_data
measures = ['Vaccination Policy', 'Face Covering Measures',
            'Border Control Measures', 'Stay At Home Measures']

date_today = dt.datetime.today().strftime("%Y-%m-%d")
date_today = pd.to_datetime(date_today)

date_tomorrow = dt.date.today() + dt.timedelta(days=1)
date_tomorrow = date_tomorrow.strftime("%Y-%m-%d")
date_tomorrow = pd.to_datetime(date_tomorrow)

dd_options = []
for key in countries:
    dd_options.append({
        'label': key,
        'value': key
    })

me_options = []
for key in measures:
    me_options.append({
        'label': key,
        'value': key
    })

pred_countries = ['Greece', 'Malaysia',
                  'South Africa', 'Germany',
                  'Japan', 'Afghanistan',
                  'Australia',
                  'Poland']

pred_options = []
for key in pred_countries:
    pred_options.append({
        'label': key,
        'value': key
    })

YEARS = [2020, 2021, 2022]

# ========================================= APPLICATION LAYOUT =========================================================

# app = dash.Dash(__name__)

tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold'
}

tab_selected_style = {
    'borderTop': '1px solid #d6d6d6',
    'borderBottom': '1px solid #d6d6d6',
    'backgroundColor': '#000000',
    'color': 'white',
    'padding': '6px'
}

layout = html.Div(children=[

    dbc.Container([

        html.Br(),

        html.H1(children='COVID-19 Current Cases and Prediction',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("View the current number of COVID-19 cases around the world, "
                "and compare cases between different countries along with the measures"
                " each country took to battle COVID-19."),

        html.Br(),

        html.Hr(),

        html.H2(children='Current Cases',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        dcc.Graph(id="globe", figure=globe),

        html.Br(),

        dcc.Tabs(id="tabs-graph", value='tab-1-graph', children=[
            dcc.Tab(label='Cases Per Month', value='tab-1-graph', style=tab_style, selected_style=tab_selected_style),
            dcc.Tab(label='Cases Per Year', value='tab-2-graph', style=tab_style, selected_style=tab_selected_style),
        ]),
        html.Div(id='tabs-content-graph'),

        html.Br(),

        html.Hr(),

        html.H3(children='COVID-19 Measures vs Cases',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("Let's take a look at how the different countries around the world implemented the three measures of "
                "Stay at Home, Face Coverings and Border Control as well as their vaccination policies and how all of "
                "this has "
                " affected COVID-19 cases."),

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

            dbc.Col(children=[
                html.Div(children=[
                    html.H6(html.B("Select countries to compare: ")),
                    dcc.Dropdown(
                        id='countries_dropdown',
                        options=dd_options,
                        value=['Malaysia'],
                        multi=True
                    )
                ])
            ]),

            dbc.Col(children=[
                html.Div(children=[
                    html.H6(html.B("Select measure to compare: ")),
                    dcc.Dropdown(
                        id='measures_dropdown',
                        # options=[{'label': i, 'value': i} for i in measures],
                        options=me_options,
                        value='Stay At Home Measures',
                        multi=False
                    )
                ])
            ])

        ]),

        html.Br(),

        dcc.Graph(id='comparison-line', figure={}),

        html.Br(),

        html.H4("Compare the COVID-19 cases between two countries against the strictness level of all measures and"
                " their vaccination policy."),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select first country: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_stacked',
                        options=dd_options,
                        value='Malaysia',
                        multi=False
                    ),
                    html.Br(),
                    dcc.Graph(id="stacked_bar1", figure={})
                ])
            ),

            dbc.Col(
                html.Div(children=[
                    html.H6(html.B("Select second country: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_stacked1',
                        options=dd_options,
                        value='New Zealand',
                        multi=False
                    ),
                    html.Br(),
                    dcc.Graph(id="stacked_bar2", figure={})
                ])
            )

        ]),

        html.Br(),

        html.Hr(),

        html.H1(children='Prediction of COVID-19 Cases',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("View the prediction of COVID-19 cases for the next 60 days."),

        html.Br(),

        html.Div(children=[

            dbc.Row(children=[
                dbc.Col(children=[
                    html.H6(html.B("Select the type of prediction: ")),
                    dcc.RadioItems(
                        id='chart_type',
                        options=[{'label': i, 'value': i} for i in ['Cumulative', 'Per Day']],
                        value='Cumulative',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text']
                                    "margin-right": "20px"}
                    ),
                ]),

                dbc.Col(children=[
                    html.H6(html.B("Select the type of y-axis: ")),
                    dcc.RadioItems(
                        id='yaxis_type',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text']
                                    "margin-right": "20px"}
                    ),
                ])
            ]),

            html.H6(html.B("Select country: ")),
            dcc.Dropdown(
                id='countries_dropdown_pred',
                options=pred_options,
                value=['Malaysia'],
                multi=True
            ),

            html.Br(),

            dash_table.DataTable(
                id='cases_table',
                columns=[
                    {"name": "Country", "id": "Country"},
                    {"name": "Today's cases", "id": "Today's cases"},
                    {"name": "Tomorrow's cases", "id": "Tomorrow's cases"},
                    {"name": "Total cases in 2022", "id": "Total cases in 2022"}
                ],
                style_cell_conditional=[
                    {'if': {'column_id': 'Country'},
                     'width': '5px'},
                    {'if': {'column_id': 'Today\'s cases'},
                     'width': '5px'},
                    {'if': {'column_id': 'Tomorrow\'s cases'},
                     'width': '5px'},
                    {'if': {'column_id': 'Total cases in 2022'},
                     'width': '5px'}
                ],
                style_cell={'textAlign': 'left',
                            'fontSize': 16, 'font-family': 'Helvetica'},
                style_header={
                    'backgroundColor': 'white',
                    'fontWeight': 'bold'
                }
            ),

            dcc.Graph(id='pred_line', figure={}),

            html.Br(),

            html.H4("This prediction is assuming each country keeps the following measures:"),

            html.Br(),

            dash_table.DataTable(
                id='measures_table',
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

            html.H4("Compare COVID-19 cases of a country between two years."),

            html.Br(),

            html.H6(html.B("Select country: ")),
            html.Div(children=[dcc.Dropdown(
                id='countries_dropdown_bar',
                options=pred_options,
                value='Malaysia',
                multi=False
            )], style=dict(width='60%')),

            html.Br(),

            dbc.Row(children=[

                dbc.Col(width=1),

                dbc.Col(children=[
                    html.H6(html.B("Select first year: ")),
                    dcc.Slider(
                        id='years_slider1',
                        min=min(YEARS),
                        max=max(YEARS),
                        value=min(YEARS),
                        marks={str(year): str(year) for year in YEARS},
                        updatemode='drag'
                    )
                ], width=4),

                dbc.Col(width=1),

                dbc.Col(children=[

                    html.H6(html.B("Select second year: ")),
                    dcc.Slider(
                        id='years_slider2',
                        min=min(YEARS),
                        max=max(YEARS),
                        value=max(YEARS),
                        marks={str(year): str(year) for year in YEARS},
                        updatemode='drag'
                    )
                ], width=4),
            ]),

            html.Br(),

            dbc.Row(
                [
                    dbc.Col(children=[
                        dcc.Graph(id='comp_bar1', figure={})
                    ]),

                    dbc.Col(children=[
                        dcc.Graph(id='comp_bar2', figure={})
                    ])
                ]
            )

        ])
    ], fluid=True)

]
)


# ======================================= APPLICATION CALLBACKS ========================

@app.callback(

    Output('tabs-content-graph', 'children'),
    Input('tabs-graph', 'value')

)
def update_graph(tab
                 ):
    if tab == 'tab-1-graph':
        return html.Div([
            # html.H3('COVID-19 Cases Per Month'),
            dcc.Graph(
                id='graph-1-tabs-dcc',
                figure=choropleth_month
            )
        ])
    elif tab == 'tab-2-graph':
        return html.Div([
            # html.H3('COVID-19 Cases Per Year'),
            dcc.Graph(
                id='graph-2-tabs-dcc',
                figure=choropleth_year
            )
        ])


@app.callback(
    Output('comparison-line', 'figure'),

    [Input('countries_dropdown', 'value'),
     Input('measures_dropdown', 'value')]
)
def update_graph(countries_choice,
                 measures_choice):
    fig = go.Figure()
    traces = []
    for i in countries_choice:
        data_country = all_data[all_data['location'] == i]
        data_monthly_strictness = gd.get_df_all_measures_month(data_country)

        traces.append(go.Scatter(x=data_monthly_strictness['date'],
                                 y=data_monthly_strictness['Total Cases'],
                                 mode='lines',
                                 # line=dict(color='rgba(0,0,200,0.7)'),
                                 name=str(i)))

        fig.add_traces(px.scatter(data_monthly_strictness,
                                  x=data_monthly_strictness['date'],
                                  y=data_monthly_strictness['Total Cases'],
                                  color=measures_choice,
                                  hover_data=['date', 'Total Cases', 'location'],
                                  labels={
                                      'date': 'Date',
                                      'cases_new': 'Confirmed Cases',
                                      'location': 'Country'
                                  }).data)

    fig.add_traces(traces)
    fig.update_layout(coloraxis_colorbar_x=-0.15,
                      coloraxis_colorbar=dict(
                          title="Strictness of <br> Measures"
                      ),
                      plot_bgcolor='rgba(234,234,242,255)',
                      template="seaborn"
                      )

    title = ', '.join(countries_choice)
    title = 'COVID-19 Cases: ' + title
    fig.update_layout(title=title)
    fig.update_layout(hovermode="x unified")
    # fig.update_layout(template='plotly_dark')

    return fig


@app.callback(
    [Output('stacked_bar1', 'figure'),
     Output('stacked_bar2', 'figure')],

    [Input('countries_dropdown_stacked', 'value'),
     Input('countries_dropdown_stacked1', 'value')]
)
def update_graph(countries_stacked1,
                 countries_stacked2):
    stacked_bar1 = graphs.get_stacked_bar_line(countries_stacked1, 'Total Cases', 'Confirmed Cases', 'Confirmed Cases')
    # stacked_bar1.update_layout(template='plotly_dark')

    stacked_bar1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    stacked_bar2 = graphs.get_stacked_bar_line(countries_stacked2, 'Total Cases', 'Confirmed Cases', 'Confirmed Cases')
    # stacked_bar2.update_layout(template='plotly_dark')

    stacked_bar2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return stacked_bar1, stacked_bar2


@app.callback(
    [Output('measures_table', 'data'),
     Output('cases_table', 'data')],

    Input('countries_dropdown_pred', 'value')
)
def update_graph(countries_dropdown):
    global measures_table, cases_table
    # today_cases = 0
    # tomorrow_cases = 0
    # total_cases = 0

    country_measures = {}
    country_measures = pd.DataFrame(country_measures)

    cases_countries_df = {}
    cases_countries_df = pd.DataFrame(cases_countries_df)

    # countries = countries_dropdown if len(countries_dropdown) > 0 else ['Malaysia']

    for countries in countries_dropdown:
        df_country = graphs.combine_pred_avaible_cases(countries)

        df_today = df_country[df_country['ds'] == date_today]
        df_today = round(df_today['yhat'], 0).astype(int)
        today_cases = df_today.iloc[-1].tolist()
        today_cases = str(today_cases)
        today_cases = '{:,}'.format(int(today_cases))

        df_tomorrow = df_country[df_country['ds'] == date_tomorrow]
        df_tomorrow = round(df_tomorrow['yhat'], 0).astype(int)
        tomorrow_cases = df_tomorrow.iloc[-1].tolist()
        tomorrow_cases = str(tomorrow_cases)
        tomorrow_cases = '{:,}'.format(int(tomorrow_cases))

        # df_today = df_country[df_country['ds'] == date_today]
        # today_last_row = df_today.tail(1)
        # print("============== today last row cases ================")
        # print(today_last_row)
        # print("=====================================================")
        # today_cases = today_last_row['yhat']
        # print("============== today cases ================")
        # print(today_cases)
        # print("============================================")
        # today_cases = today_cases.astype(int)
        # # today_cases = '{:,}'.format(int(today_cases))
        #
        # df_tomorrow = df_country[df_country['ds'] == date_tomorrow]
        # tomorrow_last_row = df_tomorrow.tail(1)
        # print("============== tomorrow last row cases ================")
        # print(tomorrow_last_row)
        # print("============================================")
        # tomorrow_cases = tomorrow_last_row['yhat']
        # print("============== tomorrow deaths ================")
        # print(tomorrow_cases)
        # print("============================================")
        # tomorrow_cases = tomorrow_cases.astype(int)
        # tomorrow_cases = '{:,}'.format(int(tomorrow_cases))

        # tomorrow_cases = FRGC.forest_reg(countries, 2)
        # tomorrow_cases = '{:,}'.format(int(tomorrow_cases))

        total_cases = graphs.get_total_cases_2022(countries)
        total_cases = '{:,}'.format(int(total_cases))

        cases = {'Country': [countries],
                 'Today\'s cases': [today_cases],
                 'Tomorrow\'s cases': [tomorrow_cases],
                 'Total cases in 2022': [total_cases]}

        cases_df = pd.DataFrame(cases)
        cases_countries_df = pd.concat([cases_countries_df, cases_df],
                                       ignore_index=True, sort=False)

        measures_table = graphs.current_measures
        country_measure = measures_table[measures_table['Country'] == countries]
        country_measures = pd.concat([country_measures, country_measure],
                                     ignore_index=True, sort=False)

        measures_table = country_measures
        cases_table = cases_countries_df

    return measures_table.to_dict(orient='records'), cases_table.to_dict(orient='records'),


@app.callback(
    Output('pred_line', 'figure'),

    [Input('chart_type', 'value'),
     Input('yaxis_type', 'value'),
     Input('countries_dropdown_pred', 'value')
     ]
)
def update_graph(chart_type, yaxis_type, countries_dropdown):
    if chart_type == 'Cumulative':
        pred_line = graphs.get_pred_line_cumm_cases(countries_dropdown, yaxis_type)
    else:
        pred_line = graphs.get_pred_line_day_cases(countries_dropdown, yaxis_type)

    return pred_line


@app.callback(
    [Output('comp_bar1', 'figure'),
     Output('comp_bar2', 'figure')],

    [Input('countries_dropdown_bar', 'value'),
     Input('years_slider1', 'value'),
     Input('years_slider2', 'value')]
)
def update_graph(countries_dropdown_bar, years_slider1, years_slider2):
    bar_chart1 = graphs.get_bar_current(countries_dropdown_bar, years_slider1, 'new_cases')
    bar_chart2 = graphs.get_bar_current(countries_dropdown_bar, years_slider2, 'new_cases')

    # bar_chart1.update_layout(template='plotly_dark')
    # bar_chart2.update_layout(template='plotly_dark')

    return bar_chart1, bar_chart2

# if __name__ == '__main__':
#     app.run_server(debug=True)
