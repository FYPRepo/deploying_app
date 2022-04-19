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

countries = gd.countries
all_data = gd.all_data
measures = ['Vaccination Policy', 'Face Covering Measures',
            'Border Control Measures', 'Stay At Home Measures']

me_options_cd = []
for key in measures:
    me_options_cd.append({
        'label': key,
        'value': key
    })

pred_countries_cd = ['Greece', 'Malaysia',
                     'South Africa', 'Germany',
                     'Japan', 'Afghanistan',
                     'Australia',
                     'Poland']

date_today_cd = dt.datetime.today().strftime("%Y-%m-%d")
date_today_cd = pd.to_datetime(date_today_cd)

date_tomorrow_cd = dt.date.today() + dt.timedelta(days=1)
date_tomorrow_cd = date_tomorrow_cd.strftime("%Y-%m-%d")
date_tomorrow_cd = pd.to_datetime(date_tomorrow_cd)

dd_options_cd = []
for key in countries:
    dd_options_cd.append({
        'label': key,
        'value': key
    })

pred_options = []
for key in pred_countries_cd:
    pred_options.append({
        'label': key,
        'value': key
    })

YEARS_cd = [2020, 2021, 2022]

# choropleths

choropleth_year_cd = px.choropleth(graphs.covid_data_year,
                                   locations="location",
                                   locationmode='country names',
                                   scope='world',
                                   color='new_cases',
                                   hover_data=['location', 'new_cases', 'new_deaths'],
                                   animation_frame='year',
                                   labels={
                                       'location': 'Country',
                                       'new_cases': 'Total Cases',
                                       'new_deaths': 'Total Deaths'
                                   },
                                   color_continuous_scale='Plasma',
                                   height=600
                                   )

choropleth_year_cd.update_layout(
    title_text='COVID-19 Cases and Deaths Yearly around the World',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)

# choropleth_year_cd.update_layout(template='plotly_dark')

choropleth_month_cd = px.choropleth(graphs.covid_data_month,
                                    locations="location",
                                    locationmode='country names',
                                    scope='world',
                                    color='new_cases',
                                    hover_data=['location', 'new_cases', 'new_deaths'],
                                    animation_frame='date',
                                    labels={
                                        'location': 'Country',
                                        'new_cases': 'Total Cases',
                                        'new_deaths': 'Total Deaths'
                                    },
                                    color_continuous_scale='Plasma',
                                    height=600
                                    )

choropleth_month_cd.update_layout(
    title_text='COVID-19 Cases and Deaths Monthly around the World',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='equirectangular'
    )
)

# choropleth_month_cd.update_layout(template='plotly_dark')

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

# ========================================= APPLICATION LAYOUT =========================================================

# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# app.layout = \
layout = html.Div(children=[

    dbc.Container([

        html.Br(),

        html.H1(children='COVID-19 Current Cases, Deaths and Prediction',
                style={'textAlign': 'center'}),
        html.Hr(),

        html.Br(),

        html.H4("View the current number of COVID-19 cases and deaths for the country of your choice, "
                "and compare them against the different measures"
                " the country took to battle COVID-19."),

        html.Br(),

        html.Hr(),

        html.H2(children='Current Cases and Deaths',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        # dcc.Graph(id="globe", figure=globe),

        html.Br(),

        dcc.Tabs(id="tabs-graph_cd", value='tab-1-graph_cd', children=[
            dcc.Tab(label='Cases & Deaths Per Month', value='tab-1-graph_cd', style=tab_style,
                    selected_style=tab_selected_style),
            dcc.Tab(label='Cases & Deaths Per Year', value='tab-2-graph_cd', style=tab_style,
                    selected_style=tab_selected_style),
        ]),
        html.Div(id='tabs-content-graph_cd'),

        html.Br(),

        html.Hr(),

        html.H3(children='COVID-19 Measures vs Cases & Deaths',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.Br(),

        html.H4("Let's take a look at how countries around the world implemented the three measures of "
                "Stay at Home, Face Coverings and Border Control as well as their vaccination policies and how all of "
                "this has "
                " affected COVID-19 cases and deaths."),

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
                    html.H6(html.B("Select country to compare: ")),
                    dcc.Dropdown(
                        id='countries_dropdown_cd',
                        options=dd_options_cd,
                        value='Malaysia',
                        multi=False
                    )
                ])
            ]),

            dbc.Col(children=[
                html.Div(children=[
                    html.H6(html.B("Select measure to compare: ")),
                    dcc.Dropdown(
                        id='measures_dropdown_cd',
                        # options=[{'label': i, 'value': i} for i in measures],
                        options=me_options_cd,
                        value='Stay At Home Measures',
                        multi=False
                    )
                ])
            ])

        ]),

        html.Br(),

        dcc.Graph(id='comparison-line_cd', figure={}),

        html.Br(),

        html.H4("Compare the COVID-19 cases and deaths against the strictness level of all measures and"
                " the vaccination policy."),

        html.Br(),

        dbc.Row(children=[
            dbc.Col(
                html.Div(children=[
                    # html.H6("Select first country: "),
                    # dcc.Dropdown(
                    #     id='countries_dropdown_stacked',
                    #     options=dd_options,
                    #     value='Malaysia',
                    #     multi=False
                    # ),
                    # html.Br(),
                    dcc.Graph(id="stacked_bar1_cd", figure={})
                ])
            ),

            dbc.Col(
                html.Div(children=[
                    # html.H6("Select second country: "),
                    # dcc.Dropdown(
                    #     id='countries_dropdown_stacked1',
                    #     options=dd_options,
                    #     value='New Zealand',
                    #     multi=False
                    # ),
                    # html.Br(),
                    dcc.Graph(id="stacked_bar2_cd", figure={})
                ])
            )

        ]),

        html.Br(),

        # html.H1("Prediction of COVID-19 Cases and Deaths for 8 Countries Around the Globe"),
        # html.H3("This page provides predictions for the COVID-19 Cases and Deaths for 8 select countries.\n"
        #         "The countries were selected based on their average level of strictness wherein 4 of them are strict and "
        #         "4 are not srict."),

        html.Hr(),

        html.H1(children='Prediction of COVID-19 Cases and Deaths',
                style={'textAlign': 'center'}),

        html.Hr(),

        html.H4("View the prediction of COVID-19 cases and deaths for the next 60 days."),

        html.Br(),

        html.Div(children=[

            dbc.Row(children=[
                dbc.Col(children=[
                    html.H6(html.B("Select the type of prediction: ")),
                    dcc.RadioItems(
                        id='chart_type_cd',
                        options=[{'label': i, 'value': i} for i in ['Cumulative', 'Per Day']],
                        value='Cumulative',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text'],
                                    "margin-right": "20px"}
                    ),
                ]),

                dbc.Col(children=[
                    html.H6(html.B("Select the type of y-axis: ")),
                    dcc.RadioItems(
                        id='yaxis_type_cd',
                        options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                        value='Linear',
                        labelStyle={'display': 'inline-block',
                                    # 'color': colors['text']
                                    "margin-right": "20px"}
                    ),
                ])
            ]),

            # html.H6("Select the type of prediction: "),
            # dcc.RadioItems(
            #     id='chart_type_cd',
            #     options=[{'label': i, 'value': i} for i in ['Cumulative', 'Per Day']],
            #     value='Linear'
            #     # labelStyle={'display': 'inline-block',
            #     #             'color': colors['text']}
            # ),
            #
            # html.H6("Select the type of y-axis: "),
            # dcc.RadioItems(
            #     id='yaxis_type_cd',
            #     options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
            #     value='Linear'
            #     # labelStyle={'display': 'inline-block',
            #     #             'color': colors['text']}
            # ),

            html.H6(html.B("Select country: ")),
            dcc.Dropdown(
                id='countries_dropdown_pred_cd',
                options=pred_options,
                value='Malaysia',
                multi=False
            ),

            html.Br(),

            dbc.Row(children=[
                dbc.Col(
                    html.Div(children=[
                        html.H5("Today's cases: "),
                        html.H5("Today's deaths: ")
                    ])
                ),

                dbc.Col(
                    html.Div(children=[
                        html.Div(id='today_cases_cd', children=[]),
                        html.Div(id='today_deaths_cd', children=[])
                    ])
                ),

                dbc.Col(
                    html.Div(children=[
                        html.H5("Tomorrow's prediction: "),
                        html.H5("Tomorrow's prediction: ")
                    ])
                ),

                dbc.Col(
                    html.Div(children=[
                        html.Div(id='tomorrow_cases_cd', children=[]),
                        html.Div(id='tomorrow_deaths_cd', children=[])
                    ])
                ),

                dbc.Col(
                    html.Div(children=[
                        html.H5("Total Cases in 2022: "),
                        html.H5("Total Deaths in 2022: ")
                    ])
                ),

                dbc.Col(
                    html.Div(children=[
                        html.Div(id='total_2022_cd_c', children=[]),
                        html.Div(id='total_2022_cd_d', children=[])
                    ])
                )

            ])

        ]),

        dcc.Graph(id='pred_line_cd', figure={}),

        html.Br(),

        html.H4("This prediction is assuming the country keeps the following measures:"),

        html.Br(),

        dash_table.DataTable(
            id='measures_table_cd',
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

        html.H4("Compare COVID-19 cases and deaths between two years."),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(width=1),

                dbc.Col(html.Div(children=[
                    html.H6(html.B("Select first year: ")),
                    dcc.Slider(
                        id='years_slider1_cd',
                        min=min(YEARS_cd),
                        max=max(YEARS_cd),
                        value=min(YEARS_cd),
                        marks={str(year): str(year) for year in YEARS_cd},
                        updatemode='drag'
                    )
                ]), width=4),

                dbc.Col(width=1),

                dbc.Col(html.Div(children=[
                    html.H6(html.B("Select second year: ")),
                    dcc.Slider(
                        id='years_slider2_cd',
                        min=min(YEARS_cd),
                        max=max(YEARS_cd),
                        value=max(YEARS_cd),
                        marks={str(year): str(year) for year in YEARS_cd},
                        updatemode='drag'
                    )
                ]), width=4)
            ]),

        html.Br(),

        dbc.Row(
            [
                dbc.Col(children=[
                    dcc.Graph(id='comp_pie1_cd', figure={})
                ]),

                dbc.Col(children=[
                    dcc.Graph(id='comp_pie2_cd', figure={})
                ])
            ]
        )
    ], fluid=True)

])


# ======================================= APPLICATION CALLBACKS ========================

@app.callback(

    Output('tabs-content-graph_cd', 'children'),
    Input('tabs-graph_cd', 'value')

)
def update_graph(tab
                 ):
    if tab == 'tab-1-graph_cd':
        return html.Div([
            # html.H3('COVID-19 Cases Per Month'),
            dcc.Graph(
                id='graph-1-tabs-dcc_cd',
                figure=choropleth_month_cd
            )
        ])
    elif tab == 'tab-2-graph_cd':
        return html.Div([
            # html.H3('COVID-19 Cases Per Year'),
            dcc.Graph(
                id='graph-2-tabs-dcc_cd',
                figure=choropleth_year_cd
            )
        ])


@app.callback(
    Output('comparison-line_cd', 'figure'),

    [Input('countries_dropdown_cd', 'value'),
     Input('measures_dropdown_cd', 'value')]
)
def update_graph(countries_choice,
                 measures_choice):
    fig = go.Figure()
    traces = []
    # for i in countries_choice:
    data_country = all_data[all_data['location'] == countries_choice]
    data_monthly_strictness = gd.get_df_all_measures_month(data_country)

    traces.append(go.Scatter(x=data_monthly_strictness['date'],
                             y=data_monthly_strictness['Total Cases'],
                             mode='lines',
                             # line=dict(color='rgba(0,0,200,0.7)'),
                             name='Cases'))

    traces.append(go.Scatter(x=data_monthly_strictness['date'],
                             y=data_monthly_strictness['Total Deaths'],
                             mode='lines',
                             # line=dict(color='rgba(0,0,200,0.7)'),
                             name='Deaths'))

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

    fig.add_traces(px.scatter(data_monthly_strictness,
                              x=data_monthly_strictness['date'],
                              y=data_monthly_strictness['Total Deaths'],
                              color=measures_choice,
                              hover_data=['date', 'Total Deaths', 'location'],
                              labels={
                                  'date': 'Date',
                                  'cases_new': 'Confirmed Deaths',
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

    # title = ', '.join(countries_choice)
    title = 'COVID-19 Cases & Deaths: ' + countries_choice
    fig.update_layout(title=title)
    fig.update_layout(hovermode="x unified")
    # fig.update_layout(template='plotly_dark')

    return fig


@app.callback(
    [Output('stacked_bar1_cd', 'figure'),
     Output('stacked_bar2_cd', 'figure')],

    Input('countries_dropdown_cd', 'value')
)
def update_graph(countries_dropdown_cd):
    stacked_bar1 = graphs.get_stacked_bar_line(countries_dropdown_cd, 'Total Cases', 'Confirmed Cases', 'Confirmed '
                                                                                                        'Cases')

    stacked_bar1.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # stacked_bar1.update_layout(template='plotly_dark')

    stacked_bar2 = graphs.get_stacked_bar_line(countries_dropdown_cd, 'Total Deaths', 'Confirmed Deaths',
                                               'Confirmed Deaths')

    stacked_bar2.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    # stacked_bar2.update_layout(template='plotly_dark')

    return stacked_bar1, stacked_bar2


@app.callback(
    [Output('measures_table_cd', 'data'),
     Output('today_cases_cd', 'children'),
     Output('tomorrow_cases_cd', 'children'),
     Output('today_deaths_cd', 'children'),
     Output('tomorrow_deaths_cd', 'children'),
     Output('total_2022_cd_c', 'children'),
     Output('total_2022_cd_d', 'children')],

    Input('countries_dropdown_pred_cd', 'value')
)
def update_graph(countries_dropdown_pred_cd):
    df_country_cases = graphs.combine_pred_avaible_cases(countries_dropdown_pred_cd)

    df_today_cases = df_country_cases[df_country_cases['ds'] == date_today_cd]
    df_today = round(df_today_cases['yhat'], 0).astype(int)
    today_cases = df_today.iloc[-1].tolist()
    today_cases = str(today_cases)
    today_cases = '{:,}'.format(int(today_cases))

    # today_last_row_cases = df_today_cases.tail(1)
    # print("============== today last row cases ================")
    # print(today_last_row_cases)
    # print("=====================================================")
    # today_cases = today_last_row_cases['yhat']
    # print("============== today cases ================")
    # print(today_cases)
    # print("============================================")
    # today_cases = today_cases.astype(int)
    # # today_cases = '{:,}'.format(int(today_cases))

    df_tomorrow_cases = df_country_cases[df_country_cases['ds'] == date_tomorrow_cd]
    df_tomorrow = round(df_tomorrow_cases['yhat'], 0).astype(int)
    tomorrow_cases = df_tomorrow.iloc[-1].tolist()
    tomorrow_cases = str(tomorrow_cases)
    tomorrow_cases = '{:,}'.format(int(tomorrow_cases))

    # tomorrow_last_row_cases = df_tomorrow_cases.tail(1)
    # print("============== tomorrow last row cases ================")
    # print(tomorrow_last_row_cases)
    # print("============================================")
    # tomorrow_cases = tomorrow_last_row_cases['yhat']
    # print("============== tomorrow deaths ================")
    # print(tomorrow_cases)
    # print("============================================")
    # tomorrow_cases = tomorrow_cases.astype(int)

    total_cases_cd = graphs.get_total_cases_2022(countries_dropdown_pred_cd)
    total_cases_cd = '{:,}'.format(int(total_cases_cd))

    # df_country_cd_d = graphs.combine_pred_avaible_deaths(countries_dropdown_cd)
    #
    # df_today_cd_d = df_country_cd_d[df_country_cd_d['ds'] == date_today_cd]
    # today_deaths_cd = df_today_cd_d['yhat'].astype(int)
    #
    # tomorrow_deaths_cd = FRGD.forest_reg(countries, 2)
    # tomorrow_deaths_cd = '{:,}'.format(int(tomorrow_deaths_cd))

    # df_tomorrow_cd_d = df_country_cd_d[df_country_cd_d['ds'] == date_tomorrow_cd]
    # tomorrow_deaths_cd = df_tomorrow_cd_d['yhat'].astype(int)

    df_country_deaths = graphs.combine_pred_avaible_deaths(countries_dropdown_pred_cd)

    df_today_deaths = df_country_deaths[df_country_deaths['ds'] == date_today_cd]
    df_today_d = round(df_today_deaths['yhat'], 0).astype(int)
    today_deaths = df_today_d.iloc[-1].tolist()
    today_deaths = str(today_deaths)
    today_deaths = '{:,}'.format(int(today_deaths))


    # today_last_row_deaths = df_today_deaths.tail(1)
    # print("============== today last row deaths ================")
    # print(today_last_row_deaths)
    # print("============================================")
    # today_deaths = today_last_row_deaths['yhat']
    # print("============== today deaths ================")
    # print(today_deaths)
    # print("============================================")
    # today_deaths = today_deaths.astype(int)
    # today_deaths = '{:,}'.format(int(today_deaths))

    df_tomorrow_deaths = df_country_deaths[df_country_deaths['ds'] == date_tomorrow_cd]
    df_tomorrow_d = round(df_tomorrow_deaths['yhat'], 0).astype(int)
    tomorrow_deaths = df_tomorrow_d.iloc[-1].tolist()
    tomorrow_deaths = str(tomorrow_deaths)
    tomorrow_deaths = '{:,}'.format(int(tomorrow_deaths))


    # tomorrow_last_row_deaths = df_tomorrow_deaths.tail(1)
    # print("============== tomorrow last row deaths ================")
    # print(tomorrow_last_row_deaths)
    # print("============================================")
    # tomorrow_deaths = tomorrow_last_row_deaths['yhat']
    # print("============== tomorrow deaths ================")
    # print(tomorrow_deaths)
    # print("============================================")
    # tomorrow_deaths = tomorrow_deaths.astype(int)

    total_deaths_cd = graphs.get_total_deaths_2022(countries_dropdown_pred_cd)
    total_deaths_cd = '{:,}'.format(int(total_deaths_cd))

    measures_table = graphs.current_measures
    country_measure = measures_table[measures_table['Country'] == countries_dropdown_pred_cd]

    measures_table = country_measure

    return measures_table.to_dict(orient='records'), today_cases, tomorrow_cases, today_deaths, \
           tomorrow_deaths, total_cases_cd, total_deaths_cd


@app.callback(
    Output('pred_line_cd', 'figure'),

    [Input('chart_type_cd', 'value'),
     Input('yaxis_type_cd', 'value'),
     Input('countries_dropdown_pred_cd', 'value')
     ]
)
def update_graph(chart_type_cd, yaxis_type_cd, countries_dropdown_cd):
    if chart_type_cd == 'Cumulative':
        pred_line_cd = graphs.cases_deaths_line_cumm(countries_dropdown_cd, yaxis_type_cd)
    else:
        pred_line_cd = graphs.cases_deaths_line(countries_dropdown_cd, yaxis_type_cd)

    pred_line_cd.update_layout(hovermode="x unified")

    return pred_line_cd


@app.callback(
    [Output('comp_pie1_cd', 'figure'),
     Output('comp_pie2_cd', 'figure')],

    [Input('countries_dropdown_pred_cd', 'value'),
     Input('years_slider1_cd', 'value'),
     Input('years_slider2_cd', 'value')]
)
def update_graph(countries_dropdown_cd, years_slider1_cd, years_slider2_cd):
    pie_chart1_cd = graphs.pie_deaths_cases(countries_dropdown_cd, years_slider1_cd)
    pie_chart2_cd = graphs.pie_deaths_cases(countries_dropdown_cd, years_slider2_cd)

    return pie_chart1_cd, pie_chart2_cd

#
# if __name__ == '__main__':
#     app.run_server(debug=True)
