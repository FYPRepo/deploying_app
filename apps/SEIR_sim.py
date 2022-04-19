from datetime import datetime as dt

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from scipy import interpolate
from scipy.integrate import odeint
import warnings

warnings.filterwarnings("ignore")

from app import app


# =========================================== THE SEIR MODEL =========================================

def derivatives(y, t, r_interpolate_y, gamma, sigma, population, inf_to_icu, icu_to_death, icu_beds):
    S, E, I, C, R, D = y

    def beta_A(t):
        return I / (I + C) * (12 * inf_to_icu + 1 / gamma * (1 - inf_to_icu)) + C / (I + C) * (
                min(icu_beds(t), C) / (min(icu_beds(t), C) + max(0, C - icu_beds(t))) * (
                icu_to_death * 7.5 + (1 - icu_to_death) * 6.5) +
                max(0, C - icu_beds(t)) / (min(icu_beds(t), C) + max(0, C - icu_beds(t))) * 1 * 1
        )

    def beta(t):
        try:
            return r_interpolate_y[int(t)] / beta_A(t) if not np.isnan(beta_A(t)) else 0
        except:
            return r_interpolate_y[-1] / beta_A(t)

    d_sdt = -beta(t) * I * S / population

    d_edt = beta(t) * I * S / population - sigma * E

    d_idt = sigma * E - 1 / 12.0 * inf_to_icu * I - gamma * (1 - inf_to_icu) * I

    d_cdt = 1 / 12.0 * inf_to_icu * I - 1 / 7.5 * icu_to_death * \
            min(icu_beds(t), C) - max(0, C - icu_beds(t)) - \
            (1 - icu_to_death) * 1 / 6.5 * min(icu_beds(t), C)

    d_rdt = gamma * (1 - inf_to_icu) * I + (1 - icu_to_death) * \
            1 / 6.5 * min(icu_beds(t), C)

    d_ddt = 1 / 7.5 * icu_to_death * min(icu_beds(t), C) + max(0, C - icu_beds(t))
    return d_sdt, d_edt, d_idt, d_cdt, d_rdt, d_ddt


gamma = 1.0 / 9.0
sigma = 1.0 / 3.0


def rep_R(t, R_start, k, x, R_end):
    return (R_start - R_end) / (1 + np.exp(-k * (-t + x))) + R_end


def seir_model(initial_cases, initial_date, population, icu_beds, R_start, k, x, R_end, inf_to_icu, icu_to_death, s,
               r_interpolate_y=None):
    days = 360

    def beta(t):
        return rep_R(t, R_start, k, x, R_end) * gamma

    def Beds(t):
        beds = icu_beds / 100_000 * population
        return beds + s * beds * t

    date_diff = int((np.datetime64("2022-01-01") - np.datetime64(initial_date)) / np.timedelta64(1, "D"))

    if date_diff > 0:
        r_interpolate_y = [r_interpolate_y[0] for _ in range(date_diff - 1)] + r_interpolate_y
    elif date_diff < 0:
        r_interpolate_y = r_interpolate_y[(-date_diff):]

    last_date = np.datetime64(initial_date) + np.timedelta64(days - 1, "D")
    missing_days = int((last_date - np.datetime64("2022-09-01")) / np.timedelta64(1, "D"))
    r_interpolate_y += [r_interpolate_y[-1] for _ in range(missing_days + 1)]

    y = population - initial_cases, initial_cases, 0.0, 0.0, 0.0, 0.0
    t = np.linspace(0, days, days)
    print(t)
    ret = odeint(derivatives, y, t, args=(r_interpolate_y,
                                          gamma, sigma, population, inf_to_icu, icu_to_death, Beds))
    S, E, I, C, R, D = ret.T
    R_change = r_interpolate_y
    total_CFR = [0] + [100 * D[i] / sum(sigma * E[:i]) if sum(
        sigma * E[:i]) > 0 else 0 for i in range(1, len(t))]

    daily_CFR = [0] + [100 * ((D[i] - D[i - 1]) / ((R[i] - R[i - 1]) + (D[i] - D[i - 1]))) if max(
        (R[i] - R[i - 1]), (D[i] - D[i - 1])) > 10 else 0 for i in range(1, len(t))]

    dates = pd.date_range(start=np.datetime64(initial_date), periods=days, freq="D")

    return dates, S, E, I, C, R, D, R_change, total_CFR, daily_CFR, [Beds(i) for i in range(len(t))]


# ========================================= APPLICATION LAYOUT =========================================================

# app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

SIDEBAR_STYLE = {
    'position': 'relative',
    'top': 25,
    'left': 0,
    'bottom': 0,
    'width': '20%',
    'padding': '20px 10px',
    'background-color': '#e3e3e3',
    # 'height': '100vh',
    'overflow-y': 'auto',
    'overflow-x': 'hidden'
}

# the style arguments for the main content page.
CONTENT_STYLE = {
    'margin-left': '25%',
    'margin-right': '5%',
    'top': 125,
    'padding': '20px 10px',
    'position': 'absolute'
}

TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#191970'
}

CARD_TEXT_STYLE = {
    'textAlign': 'center',
    'color': '#0074D9'
}

controls = dbc.FormGroup(
    [
        html.P('First Infection Date', style={
            'textAlign': 'center'
        }),
        dcc.DatePickerSingle(
            day_size=39,  # how big the date picker appears
            display_format="DD.MM.YYYY",
            date='2022-01-01',
            id='initial_date',
            min_date_allowed=dt(2022, 1, 1),
            max_date_allowed=dt(2022, 5, 31),
            initial_visible_month=dt(2022, 1, 1),
            placeholder="date"
        ),

        html.Br(),

        html.P('Initial Number of Cases', style={
            'textAlign': 'center'
        }),
        dbc.Input(
            id="initial_cases",
            type="number",
            placeholder="Initial cases",
            min=1,
            max=1_000_000,
            step=1,
            value=15
        ),

        html.Br(),

        html.P('Population of Country', style={
            'textAlign': 'center'
        }),
        dbc.Input(
            id="population",
            type="number",
            placeholder="population",
            min=10_000,
            max=1_000_000_000,
            step=10_000,
            value=10_000_000
        ),

        html.Br(),

        html.P('ICU beds available per 100K people', style={
            'textAlign': 'center'
        }),
        dbc.Input(
            id="icu_beds",
            type="number",
            placeholder="ICU beds available",
            min=0.0,
            max=100.0,
            step=0.1,
            value=34.0,
        ),

        html.Br(),
        html.P('% Probability of going to the ICU after infection ', style={
            'textAlign': 'center'
        }),
        dcc.Slider(
            id='inf_to_icu',
            min=0.01,
            max=100.0,
            step=0.01,
            value=5.0,
            tooltip={'always_visible': False, "placement": "bottom"}
        ),

        html.Br(),
        html.P('% Probability of dying in the ICU after admission ', style={
            'textAlign': 'center'
        }),
        dcc.Slider(
            id='icu_to_death',
            min=0.01,
            max=100.0,
            step=0.01,
            value=50.0,
            tooltip={'always_visible': False, "placement": "bottom"}
        ),

        html.Br(),
        html.P('Reproduction rate of the virus ', style={
            'textAlign': 'center'
        }),

        dash_table.DataTable(
            id='r_table',
            columns=[
                {"name": "Date", "id": "Date"},
                {"name": "R value", "id": "R value",
                 "editable": True, "type": "numeric"},
            ],
            data=[
                {
                    "Date": i[0],
                    "R value": i[1],
                }
                for i in [("2022-01-01", 3.2), ("2022-02-01", 2.9), ("2022-03-01", 2.5), ("2022-04-01", 0.8),
                          ("2022-05-01", 1.1), ("2022-06-01", 2.0), ("2022-07-01", 2.1), ("2022-08-01", 2.2),
                          ("2022-09-01", 2.3)]
            ],
            style_cell_conditional=[
                {'if': {'column_id': 'Date'},
                 'width': '5px'},
                {'if': {'column_id': 'R value'},
                 'width': '10px'},
            ],
            style_cell={'textAlign': 'left',
                        'fontSize': 16, 'font-family': 'Helvetica'},
            style_header={
                'backgroundColor': 'white',
                'fontWeight': 'bold'
            }
        ),

        html.Br(),

        dbc.Button("Apply to Graphs",
                   id="submit-button-state",
                   color="primary")

    ]
)

sidebar = html.Div(
    [
        html.H2('SEIR Simulation Parameters'),
        html.Hr(),
        controls
    ], style=SIDEBAR_STYLE,
)

content = html.Div([
    html.H1('SEIR Simulation For the Spread of COVID-19',
            className="display-3"),
    html.Hr(className="my-2"),
    html.P("Simulate the spread of COVID-19 with a few parameters.",
           className="lead"),
    dcc.Markdown('''
                            The SEIR model is used to simulate and predict the spread of COVID-19. The model divides the
                            population into 4 groups: Susceptible, Exposed, Infected and Recovered. The Susceptible group is the number of 
                            the population susceptible to being infected by the virus. The Exposed group is the number of the 
                            population that has been exposed to the virus but has not yet been infected by it. The Infected group
                            is the number of the population that has been infected by the virus. The Recovered group is the number of the population
                            that has fully recovered from the virus after being infected by it.
                            
                            In this simulation, you can freely tune the date at which the first infected occurred, the total number of the population,
                            the number of ICU beds per 100 thousand of the population, the probability of going to the ICU after infection
                            and the probability of dying in the ICU. These parameters will then work together to simulate the spread of the virus
                            and how much of the population is in each of the SEIR groups. 
                            
                            The reproduction rate (R) of the virus, i.e. how fast it spreads between the population,
                            can also be changed to simulate lockdowns, social distancing, a second wave of the virus
                            etc. 
                            
                            Tune the parameters on the side bar and click the Apply button to get started!
                            '''
                 ),

    dcc.Graph(id='main_graph'),
    html.Br(),
    dbc.Row(
        [
            dbc.Col(dcc.Graph(id='seir_bar'), md=6),
            dbc.Col(dcc.Graph(id='seir_pie'), md=6)

        ]
    ),
    # dcc.Graph(id='r0_graph'),
    html.Br(),
    html.H2("What about the fatality of the virus?"),
    dcc.Graph(id='cfr_graph'),
    html.Br(),
    dcc.Graph(id='deaths_critical'),
    html.Br(),
    dcc.Graph(id="deaths_icu"),
    # dbc.Row(
    #     [
    #         # the graph for the fatality rate over time.
    #         dbc.Col(dcc.Graph(id='deaths_critical'), md=6),
    #         dbc.Col(dcc.Graph(id="deaths_icu"), md=6)
    #
    #     ]
    # ),
    html.Br()

], style=CONTENT_STYLE
)

layout = html.Div([sidebar, content])

# ======================================= APPLICATION CALLBACKS ========================


@app.callback(
    [Output('main_graph', 'figure'),
     Output('seir_bar', 'figure'),
     Output('seir_pie', 'figure'),
     Output('cfr_graph', 'figure'),
     # Output('r0_graph', 'figure'),
     Output('deaths_icu', 'figure'),
     Output('deaths_critical', 'figure')
     ],

    [Input('submit-button-state', 'n_clicks')],

    [State('initial_cases', 'value'),
     State('initial_date', 'date'),
     State('population', 'value'),
     State('icu_beds', 'value'),
     State('inf_to_icu', 'value'),
     State('icu_to_death', 'value'),
     State('r_table', 'data'),
     State('r_table', 'columns')
     ]

)
def update_graphs(_, initial_cases, initial_date, population, icu_beds, inf_to_icu, icu_to_death, r_table_data,
                  r_table_columns):
    placeholder_initial_date = "2022-01-15"
    placeholder_population = 1_000_000
    placeholder_icu_beds = 5.0
    placeholder_inf_to_icu = 5.0
    placeholder_icu_to_death = 50.0

    if not (initial_date and population and icu_beds and inf_to_icu and icu_to_death):
        initial_date, population, icu_beds, \
        inf_to_icu, icu_to_death = placeholder_initial_date, placeholder_population, placeholder_icu_beds, \
                                   placeholder_inf_to_icu, placeholder_icu_to_death

    r_table_data_x = [datapoint["Date"] for datapoint in r_table_data]
    r_table_data_y = [
        datapoint["R value"] if ((not np.isnan(datapoint["R value"])) and (datapoint["R value"] >= 0)) else 0
        for datapoint in r_table_data]

    f = interpolate.interp1d([0, 1, 2, 3, 4, 5, 6, 7, 8], r_table_data_y, kind='linear')

    r_dates_x = pd.date_range(start=np.datetime64("2022-01-01"), end=np.datetime64("2022-09-01"), freq="D")
    r_interpolate_y = f(np.linspace(0, 8, num=len(r_dates_x))).tolist()

    dates, S, E, I, C, R, D, r_change, total_CFR, daily_CFR, B = seir_model(initial_cases, initial_date,
                                                                            population,
                                                                            icu_beds, 3.0, 0.01, 50, 2.3,
                                                                            float(inf_to_icu) / 100,
                                                                            float(icu_to_death) / 100, 0.001,
                                                                            r_interpolate_y)

    seir_graph = go.Figure()
    seir_graph.add_trace(go.Scatter(
        x=dates,
        y=S.astype(int),
        mode='lines',
        name='Susceptible'
    ))

    seir_graph.add_trace(go.Scatter(
        x=dates,
        y=E.astype(int),
        mode='lines',
        name='Exposed'
    ))

    seir_graph.add_trace(go.Scatter(
        x=dates,
        y=I.astype(int),
        mode='lines',
        name='Infected'
    ))

    seir_graph.add_trace(go.Scatter(
        x=dates,
        y=R.astype(int),
        mode='lines',
        name='Recovered'
    ))

    seir_graph.update_layout(title='Compartments over time', template="seaborn")
    seir_graph.update_yaxes(title_text='Population')
    seir_graph.update_xaxes(title_text='Date')
    seir_graph.update_layout(hovermode="x unified")

    sus_sum = sum(S)
    exp_sum = sum(E)
    inf_sum = sum(I)
    rec_sum = sum(R)

    seir_pie = px.pie(values=[sus_sum, exp_sum, inf_sum, rec_sum],
                      names=['susceptible', 'exposed', 'infected', 'recovered'],
                      hole=.3)
    seir_pie.update_layout(template="seaborn")

    seir_bar = go.Figure([go.Bar(
        y=[sus_sum, exp_sum, inf_sum, rec_sum],
        x=['susceptible', 'exposed', 'infected', 'recovered']
    )])
    seir_bar.update_layout(template="seaborn")

    fatality_graph = go.Figure()
    fatality_graph.add_trace(go.Scatter(
        x=dates,
        y=daily_CFR,
        mode='lines',
        name='Daily Fatality'
    ))

    fatality_graph.add_trace(go.Scatter(
        x=dates,
        y=total_CFR,
        mode='lines',
        name='Total Fatality'
    ))

    fatality_graph.update_layout(title='Fatality Rate from the Virus', template="seaborn")
    fatality_graph.update_yaxes(title_text='Rate')
    fatality_graph.update_xaxes(title_text='Date')
    fatality_graph.update_layout(hovermode="x unified")

    # reproduction_graph = go.Figure()
    # reproduction_graph.add_trace(go.Scatter(
    #     x=dates,
    #     y=R_0_over_time,
    #     mode='lines',
    #     name='susceptible'
    # ))
    #
    # reproduction_graph.update_layout(title='Reproduction Rate of the Virus')
    # reproduction_graph.update_yaxes(title_text='Rate')
    # reproduction_graph.update_xaxes(title_text='Date')

    deaths_graph = go.Figure()
    # deaths_graph.add_trace(go.Scatter(
    #     x=dates,
    #     y=[0] + [D[i] - D[i - 1] for i in range(1, len(dates))],
    #     mode='lines',
    #     name='Total Deaths'
    # ))

    deaths_graph.add_trace(
        go.Scatter(
            x=dates,
            y=[0] + [max(0, C[i - 1] - B[i - 1]) for i in range(1, len(dates))],
            mode='lines',
            name='Deaths due to Overcapacity of the ICU'
        )
    )

    deaths_graph.update_layout(title='Deaths due to Overcapacity of the ICU',
                               template="seaborn")
    deaths_graph.update_yaxes(title_text='Deaths')
    deaths_graph.update_xaxes(title_text='Date')

    critical_deaths = go.Figure()
    critical_deaths.add_trace(go.Scatter(
        x=dates,
        y=D.astype(int),
        mode='lines',
        name='Dead'
    ))

    critical_deaths.add_trace(go.Scatter(
        x=dates,
        y=C.astype(int),
        mode='lines',
        name='Critical Condition'
    ))

    critical_deaths.update_layout(title='Critical Cases and Deaths of COVID-19',
                                  template="seaborn")
    critical_deaths.update_yaxes(title_text='Deaths')
    critical_deaths.update_xaxes(title_text='Date')
    critical_deaths.update_layout(hovermode="x unified")

    # return seir_graph, seir_bar, seir_pie, fatality_graph, reproduction_graph, deaths_graph, critical_deaths
    return seir_graph, seir_bar, seir_pie, fatality_graph, deaths_graph, critical_deaths

# if __name__ == '__main__':
#     app.run_server(debug=True)
