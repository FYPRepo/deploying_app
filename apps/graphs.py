import datetime
import datetime as dt
import warnings

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import signal

from apps import get_data as gd
from Prediction import forest_reg_cases as FRGC
from Prediction import forest_reg_deaths as FRGD

warnings.filterwarnings("ignore")

covid_data_month = gd.covid_data_month
covid_data_year = gd.covid_data_year
covid_data_total = gd.covid_data_total


# ------------------------------------------------------------- CHOROPLETHS FOR MONTHLY AND YEARLY NUMBER OF CASES & DEATHS ------------------------------------------------------------

def get_choropleth(df, color, title, frame, color_label):
    choropleth = px.choropleth(df,
                               locations="location",
                               locationmode='country names',
                               scope='world',
                               color=color,
                               hover_data=['location', color],
                               animation_frame=frame,
                               labels={
                                   'location': 'Country',
                                   color: color_label
                               },
                               color_continuous_scale='Plasma',
                               height=600
                               )

    choropleth.update_layout(
        title_text=title,
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type='equirectangular'
        )
    )

    return choropleth


choropleth_month_cases = get_choropleth(covid_data_month, 'new_cases',
                                        'COVID-19 Cases Monthly around the World', 'date',
                                        'Total Cases')

# choropleth_month_cases.update_layout(template='plotly_dark')
# choropleth_month_cases.show()

choropleth_year_cases = get_choropleth(covid_data_year, 'new_cases',
                                       'COVID-19 Cases Yearly around the World', 'year',
                                       'Total Cases')

# choropleth_year_cases.update_layout(template='plotly_dark')
# choropleth_year_cases.show()

choropleth_month_deaths = get_choropleth(covid_data_month, 'new_deaths',
                                         'COVID-19 Deaths Monthly around the World', 'date',
                                         'Total Deaths')

# choropleth_month_deaths.update_layout(template='plotly_dark')
# choropleth_month_deaths.show()

choropleth_year_deaths = get_choropleth(covid_data_year, 'new_deaths',
                                        'COVID-19 Deaths Yearly around the World', 'year',
                                        'Total Deaths')

# choropleth_year_deaths.update_layout(template='plotly_dark')
# choropleth_year_deaths.show()

# -------------------------------------------------------------------- GLOBE FOR TOTAL NUMBER OF CASES -----------------------------------------------------------

countries = np.unique(covid_data_total['location'])


def get_globe(df, column, col_label, bar_title, fig_title):
    data = [dict(
        type='choropleth',
        locations=countries,
        z=df[column],
        locationmode='country names',
        text=countries,
        marker=dict(
            line=dict(color='rgb(0,0,0)', width=1)),
        colorbar=dict(tickprefix='',
                      title=bar_title),
        colorscale='Plasma'
    )
    ]

    layout = dict(
        title=fig_title,
        geo=dict(
            showframe=False,
            showocean=True,
            oceancolor='rgb(12,74,173)',
            projection=dict(
                type='orthographic',
                rotation=dict(
                    lon=60,
                    lat=10),
            ),
            lonaxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)'
            ),
            lataxis=dict(
                showgrid=True,
                gridcolor='rgb(102, 102, 102)'
            )
        ),
    )

    globe = go.Figure(data=data, layout=layout)

    return globe


globe_cases = get_globe(covid_data_total, 'new_cases', 'Total Cases', 'Total COVID-19\nCases',
                        'Total COVID-19 Cases Around the World')
globe_deaths = get_globe(covid_data_total, 'new_deaths', 'Total Deaths', 'Total COVID-19\nDeaths',
                         'Total COVID-19 Deaths Around the World')

# globe_cases.update_layout(template='plotly_dark')
# globe_deaths.update_layout(template='plotly_dark')

# globe = go.Figure(data=data, layout=layout)
# globe.update_layout(template='plotly_dark')
# globe.show()

# --------------------------------------------------------- SCATTER PLOT FOR CORRELATION BETWEEN MEASURES AND CASES -----------------------------------------------------------
# NOT A GOOD MEASURE

all_data = gd.all_data
all_data = all_data[all_data['location'] != 'Asia']
all_data = all_data[all_data['location'] != 'Africa']
all_data = all_data[all_data['location'] != 'Oceania']
all_data = all_data[all_data['location'] != 'South America']
all_data = all_data[all_data['location'] != 'North America']
all_data = all_data[all_data['location'] != 'Europe']


# scatter_plot = px.scatter()


def add_trace_scatter(measure, country):
    all_data_monthly = gd.get_df_measures_cases(all_data, measure)
    all_data_monthly = all_data_monthly[all_data_monthly['location'] == country]
    # print("all_data_monthly: (data for scatter plot)")
    # print("---------------------------------------------------------------------")
    # print(all_data_monthly.head())
    # print("---------------------------------------------------------------------")

    scatter_plot = px.scatter(all_data_monthly,
                              x=measure,
                              y='Total Cases',
                              trendline="ols")

    # scatter_plot.update_layout(template='plotly_dark')

    return scatter_plot


scatter = add_trace_scatter('Total Strictness', 'Afghanistan')


# scatter.show()


# -------------------------------------------------------------- HEATMAP TO SHOW CORRELATION ---------------------------------------------------------
# NOT A GOOD MEASURE

def get_heatmap(country):
    all_data_country = all_data[all_data['location'] == country]

    correlation = all_data_country.corr()
    # print("correlation data:")
    # print("---------------------------------------------------------------------")
    # print(correlation.head())
    # print("---------------------------------------------------------------------")

    # correlation_temp = correlation.drop(['population', 'year_x', 'month_x',
    #                                      'new_cases_smoothed', 'new_deaths',
    #                                      'new_deaths_smoothed', 'year_y',
    #                                      'month_y', 'year', 'month'])

    heatmap = px.imshow(correlation,
                        text_auto=True,
                        aspect="auto")

    heatmap.update_xaxes(side="top")
    # heatmap.update_layout(template='plotly_dark')

    return heatmap


heatmap_corr = get_heatmap('Malaysia')
# heatmap_corr.show()

# ---------------------------------------------------- GANTT CHART OF MEASURES ---------------------------------------------------------------------

measures = ['Total Strictness', 'Vaccination Policy', 'Face Covering Measures',
            'Border Control Measures', 'Stay At Home Measures']


def get_gantt(measure, country):
    data_country = all_data[all_data['location'] == country]

    data_country['date'] = pd.to_datetime(data_country['date'], dayfirst=True)
    g = data_country.groupby(measure)['date'].diff().dt.days.ne(1).cumsum()  # STEP A
    m = data_country.groupby([measure, g])[measure].transform('max').eq(
        data_country[measure])  # STEP B

    df = data_country.assign(high_hats=data_country[measure].mask(~m),
                             high_date=data_country[measure].mask(~m))  # STEP C

    dct = {'Start Date': ('date', 'first'), 'End Date': ('date', 'last')}
    df1 = df.groupby([measure, g]).agg(**dct).reset_index().drop('date', 1)  # STEP D

    gantt = px.timeline(df1, x_start="Start Date", x_end="End Date", y=measure)
    gantt.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
    # gantt.update_layout(template='plotly_dark')

    return gantt


gantt = get_gantt('Vaccination Policy', 'Malaysia')


# gantt.show()

# ---------------------------------------------- STACKED BAR + LINE CHART  ----------------------------------------------------

def get_stacked_bar_line(country, cases_or_deaths, ytitle, line_name):
    data_country = all_data[all_data['location'] == country]
    data_monthly_strictness = gd.get_df_all_measures_month(data_country)

    stacked_bar = make_subplots(specs=[[{"secondary_y": True}]])

    measures_ = ['Vaccination Policy', 'Face Covering Measures',
                 'Border Control Measures', 'Stay At Home Measures']

    color_list = [px.colors.sequential.Sunset[3], px.colors.sequential.Sunset[4],
                  px.colors.sequential.Sunset[5], px.colors.sequential.Sunset[6]]

    # for measure in measures_ and color in color_list:

    for i in [0, 1, 2, 3]:
        stacked_bar.add_trace(go.Bar(name=measures_[i],
                                     x=data_monthly_strictness.date,
                                     y=data_monthly_strictness[measures_[i]],
                                     marker_color=color_list[i]),
                              secondary_y=False)

    stacked_bar.add_trace(go.Scatter(x=data_monthly_strictness.date,
                                     y=data_monthly_strictness[cases_or_deaths],
                                     mode='lines',
                                     name=line_name,
                                     line=dict(color='rgb(0,0,0)', width=3)),
                          secondary_y=True)

    stacked_bar.update_layout(barmode='stack', template="seaborn")
    # stacked_bar.update_layout(template='plotly_dark')
    stacked_bar.update_xaxes(title='Year', showgrid=False)
    stacked_bar.update_yaxes(title_text="Measure Level", secondary_y=False)
    stacked_bar.update_yaxes(title_text=ytitle, secondary_y=True)

    return stacked_bar


cases_measures_bar_cases = get_stacked_bar_line('Malaysia', 'Total Cases', 'Confirmed Cases', 'Confirmed Cases')
cases_measures_bar_deaths = get_stacked_bar_line('Malaysia', 'Total Deaths', 'Confirmed Deaths', 'Confirmed Deaths')


# cases_measures_bar_cases.show()
# cases_measures_bar_deaths.show()


# ---------------------------------------------------------------- PREDICTION DATA LINE GRAPHS ----------------------------------------------------


def get_pred_cases_day(country):
    pred_link = 'https://raw.githubusercontent.com/FYPRepo/Prediction-Files/main/cases_prophet_csv_per_day_' + country + '.csv'
    pred_link = pred_link.replace(" ", "%20")
    prediction_data_df = pd.read_csv(pred_link)

    return prediction_data_df


def get_pred_deaths_day(country):
    pred_link = 'https://raw.githubusercontent.com/FYPRepo/Prediction-Files/main/deaths_prophet_csv_per_day_' + country + '.csv'
    pred_link = pred_link.replace(" ", "%20")
    prediction_data_df = pd.read_csv(pred_link)

    return prediction_data_df


def get_pred_cases_cumm(country):
    pred_link = 'https://raw.githubusercontent.com/FYPRepo/Prediction-Files/main/cases_prophet_csv_cummulative_' + country + '.csv'
    pred_link = pred_link.replace(" ", "%20")
    prediction_data_df = pd.read_csv(pred_link)

    return prediction_data_df


def get_pred_deaths_cumm(country):
    pred_link = 'https://raw.githubusercontent.com/FYPRepo/Prediction-Files/main/deaths_prophet_csv_cummulative_' + country + '.csv'
    pred_link = pred_link.replace(" ", "%20")
    prediction_data_df = pd.read_csv(pred_link)

    return prediction_data_df


date_today = dt.datetime.today().strftime("%Y-%m-%d")
date_tomorrow = dt.date.today() + dt.timedelta(days=1)
date_tomorrow = date_tomorrow.strftime("%Y-%m-%d")


# COMBINING THE PRED DF WITH AVAILABLE DATA
def combine_pred_avaible_cases(country):
    df_pred = get_pred_cases_day(country)
    df_pred = df_pred[['ds', 'yhat']]
    df_pred['location'] = ""

    available_data = gd.covid_data
    available_data['date'] = pd.to_datetime(available_data['date'])
    available_data['date'] = available_data['date'].dt.date

    available_data = available_data[available_data['location'] == country]
    available_data = available_data[['date', 'location', 'new_cases']]
    available_data.rename(columns={'date': 'ds', 'new_cases': 'yhat'}, inplace=True)

    df_concat = pd.concat([available_data, df_pred],
                          ignore_index=True, sort=False)
    df_concat.loc[df_concat['location'] == "", 'location'] = country
    df_concat = df_concat.fillna(0)
    df_concat['yhat'] = df_concat['yhat'].astype(int)

    next_day_pred = FRGC.forest_reg(country, 2).astype(int)
    df_forest = {'ds': [date_tomorrow], 'location': country, 'yhat': [next_day_pred]}
    df_forest = pd.DataFrame(df_forest)
    # print("=========== df_forest =========")
    # print(df_forest)
    # print("================================")

    i = df_concat[(df_concat.ds == date_tomorrow)].index
    df_concat = df_concat.drop(i)

    # df_concat.combine_first(df_forest)

    df_concat = pd.concat([df_concat, df_forest],
                          ignore_index=True, sort=True)

    df_concat['ds'] = pd.to_datetime(df_concat['ds'])
    df_concat['ds'] = df_concat['ds'].dt.date

    df_concat = df_concat.sort_values(by=['ds'], ascending=True)

    # print("combining cases prediction data with available data:")
    # print("---------------------------------------------------------------------")
    # print(df_concat)
    # # df_concat.to_csv("df_concat.csv")
    # print("---------------------------------------------------------------------")

    return df_concat


def combine_pred_avaible_deaths(country):
    df_pred = get_pred_deaths_day(country)
    df_pred = df_pred[['ds', 'yhat']]
    df_pred['location'] = ""

    available_data = gd.covid_data
    available_data['date'] = pd.to_datetime(available_data['date'])
    available_data['date'] = available_data['date'].dt.date

    available_data = available_data[available_data['location'] == country]
    available_data = available_data[['date', 'location', 'new_deaths']]
    available_data.rename(columns={'date': 'ds', 'new_deaths': 'yhat'}, inplace=True)

    df_concat = pd.concat([available_data, df_pred],
                          ignore_index=True, sort=False)
    df_concat.loc[df_concat['location'] == "", 'location'] = country
    df_concat = df_concat.fillna(0)
    df_concat['yhat'] = df_concat['yhat'].astype(int)

    next_day_pred = FRGD.forest_reg(country, 2).astype(int)
    df_forest = {'ds': [date_tomorrow], 'location': country, 'yhat': [next_day_pred]}
    df_forest = pd.DataFrame(df_forest)

    # df_concat = pd.merge(df_concat, df_forest, on='ds', how='left')

    # df_concat.update(df_forest)
    # df_concat.combine_first(df_forest)

    # df_concat = df_concat.append(df_forest, ignore_index=True).drop_duplicates(subset='ds')

    i = df_concat[(df_concat.ds == date_tomorrow)].index
    df_concat = df_concat.drop(i)

    # df_concat.combine_first(df_forest)

    df_concat = pd.concat([df_concat, df_forest],
                          ignore_index=True, sort=True)

    df_concat['ds'] = pd.to_datetime(df_concat['ds'])
    df_concat['ds'] = df_concat['ds'].dt.date

    df_concat = df_concat.sort_values(by=['ds'], ascending=True)

    # print("combining deaths prediction data with available data:")
    # print("---------------------------------------------------------------------")
    # print(df_concat)
    # print("---------------------------------------------------------------------")

    return df_concat


# combine_pred_avaible_cases('Malaysia')


pred_countries = ['Greece', 'Malaysia',
                  'South Africa', 'Germany',
                  'Japan', 'Afghanistan',
                  'Australia',
                  'Poland']


def get_pred_line_cumm_cases(country, axis_type):
    countries = country if len(country) > 0 else ['Malaysia']

    data_value = []
    for country_pred in country:
        df = get_pred_cases_cumm(country_pred)
        df['ds'] = pd.to_datetime(df['ds'])
        df['ds'] = df['ds'].dt.date

        date = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d').date()

        df_2022 = df[(df['ds'] > date)]

        data_value.append(dict(
            x=df_2022['ds'],
            # y=signal.savgol_filter(df_2022.yhat, 35, 3).astype(int),
            y=df_2022.yhat.astype(int),
            type='lines',
            name=str(country_pred)
        ))

    title = ', '.join(countries)
    title = 'Prediction of the Cummulative COVID-19 Cases for the next 60 days in: ' + title

    return {
        'data': data_value,
        'layout': dict(
            yaxis={
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            plot_bgcolor='rgba(234,234,242,255)',
            template="seaborn",
            # template='plotly_dark',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            hovermode='x unified',
            title=title
        )
    }


def get_pred_line_cumm_deaths(country, axis_type):
    countries = country if len(country) > 0 else ['Malaysia']

    data_value = []
    for country_pred in country:
        df = get_pred_deaths_cumm(country_pred)
        df['ds'] = pd.to_datetime(df['ds'])
        df['ds'] = df['ds'].dt.date

        date = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d').date()

        df_2022 = df[(df['ds'] > date)]

        data_value.append(dict(
            x=df_2022['ds'],
            # y=signal.savgol_filter(df_2022.yhat, 35, 3).astype(int),
            y=df_2022.yhat.astype(int),
            type='lines',
            name=str(country_pred)
        ))

    title = ', '.join(countries)
    title = 'Prediction of the Cummulative COVID-19 Deaths for the next 60 days in: ' + title

    return {
        'data': data_value,
        'layout': dict(
            yaxis={
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            plot_bgcolor='rgba(234,234,242,255)',
            template='seaborn',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            hovermode='x unified',
            title=title
        )
    }


def get_pred_line_day_cases(country, axis_type):
    countries = country if len(country) > 0 else ['Malaysia']

    data_value = []
    for country_pred in country:
        df = combine_pred_avaible_cases(country_pred)
        df['ds'] = pd.to_datetime(df['ds'])
        df['ds'] = df['ds'].dt.date

        date = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d').date()

        df_2022 = df[(df['ds'] > date)]

        data_value.append(dict(
            x=df_2022['ds'],
            # y=signal.savgol_filter(df_2022.yhat, 35, 3).astype(int),
            y=df_2022.yhat.astype(int),
            type='lines',
            name=str(country_pred)
        ))

    title = ', '.join(countries)
    title = 'Prediction of the COVID-19 Cases Per Day for the next 60 days in: ' + title

    return {
        'data': data_value,
        'layout': dict(
            yaxis={
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            plot_bgcolor='rgba(234,234,242,255)',
            template='seaborn',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            hovermode='x unified',
            title=title
        )
    }


def get_pred_line_day_deaths(country, axis_type):
    countries = country if len(country) > 0 else ['Malaysia']

    data_value = []
    for country_pred in country:
        df = combine_pred_avaible_deaths(country_pred)
        df['ds'] = pd.to_datetime(df['ds'])
        df['ds'] = df['ds'].dt.date

        date = datetime.datetime.strptime('2020-12-31', '%Y-%m-%d').date()

        df_2022 = df[(df['ds'] > date)]

        data_value.append(dict(
            x=df_2022['ds'],
            # y=signal.savgol_filter(df_2022.yhat, 35, 3).astype(int),
            y=df_2022.yhat.astype(int),
            type='lines',
            name=str(country_pred)
        ))

    title = ', '.join(countries)
    title = 'Prediction of the Cummulative COVID-19 Deaths for the next 60 days in: ' + title

    return {
        'data': data_value,
        'layout': dict(
            yaxis={
                'type': 'linear' if axis_type == 'Linear' else 'log'
            },
            plot_bgcolor='rgba(234,234,242,255)',
            template='seaborn',
            xaxis=dict(
                rangeselector=dict(
                    buttons=list([
                        dict(count=1,
                             label="1m",
                             step="month",
                             stepmode="backward"),
                        dict(count=6,
                             label="6m",
                             step="month",
                             stepmode="backward"),
                        dict(count=1,
                             label="YTD",
                             step="year",
                             stepmode="todate"),
                        dict(count=1,
                             label="1y",
                             step="year",
                             stepmode="backward"),
                        dict(step="all")
                    ])
                ),
                rangeslider=dict(
                    visible=True
                ),
                type="date"
            ),
            hovermode='x unified',
            title=title
        )
    }


# pred_line = get_pred_line_day_cases('Malaysia', 'Linear')
# pred_line2 = get_pred_line_day_deaths('Malaysia', 'Linear')
# pred_line3 = get_pred_line_cumm_cases('Malaysia', 'Linear')
# pred_line4 = get_pred_line_cumm_deaths('Malaysia', 'Linear')

# pred_line.show()
# pred_line2.show()
# pred_line3.show()
# pred_line4.show()


# -------------------------------------------------------------------------- CASES + DEATHS PREDICTION IN ONE --------------------------------------------------
# get the combined df for cases and deaths
# change the name of yhat in each of them to cases and deaths
# merge both of those dataframes on date and location

# create a stacked bar chart of deaths and cases
# create a line chart with two lines

# pass the per day prediction df here to find the total number of cases
# in the year 2022 till may


def pred_df_total(df, country, year):
    df['location'] = country

    df['ds'] = pd.to_datetime(df['ds'])
    df['year'] = df['ds'].dt.year
    df = df[df['year'] == year]

    df = df.groupby(['location', 'year'])[['yhat']].sum()
    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    # print("total for each year:")
    # print("---------------------------------------------------------------------")
    # print(df)
    # print("---------------------------------------------------------------------")

    return df


def df_for_cases_deaths_pred(country):
    cases_combine = combine_pred_avaible_cases(country)
    deaths_combine = combine_pred_avaible_deaths(country)

    cases_combine.rename(columns={'yhat': 'cases'}, inplace=True)
    deaths_combine.rename(columns={'yhat': 'deaths'}, inplace=True)

    deaths_cases_df = pd.merge(cases_combine, deaths_combine,
                               how='left', on=['ds', 'location'])

    deaths_cases_df['ds'] = pd.to_datetime(deaths_cases_df['ds'])
    deaths_cases_df['year'] = deaths_cases_df['ds'].dt.year
    deaths_cases_df['month'] = deaths_cases_df['ds'].dt.month

    return deaths_cases_df


def df_for_cases_deaths_pred_year(country, year):
    cases_combine = combine_pred_avaible_cases(country)
    deaths_combine = combine_pred_avaible_deaths(country)

    cases_combine.rename(columns={'yhat': 'cases'}, inplace=True)
    deaths_combine.rename(columns={'yhat': 'deaths'}, inplace=True)

    deaths_cases_df = pd.merge(cases_combine, deaths_combine, how='left', on=['ds', 'location'])

    deaths_cases_df['ds'] = pd.to_datetime(deaths_cases_df['ds'])
    deaths_cases_df['year'] = deaths_cases_df['ds'].dt.year
    deaths_cases_df['month'] = deaths_cases_df['ds'].dt.month

    pd.DatetimeIndex(deaths_cases_df.ds).to_period("M")

    per = deaths_cases_df.ds.dt.to_period("M")
    df = deaths_cases_df.groupby([per])[['cases', 'deaths']].sum()

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    df['ds'] = df.ds.astype(str)
    # df = gd.covid_data_month
    # df = df[df['location'] == country]

    year = str(year)
    df = df[df['ds'].str.contains(year)]

    return df


def pie_deaths_cases(country, year):
    df_c = combine_pred_avaible_cases(country)
    df_d = combine_pred_avaible_deaths(country)

    df_ct = pred_df_total(df_c, country, year)

    df_total_ct = round(df_ct['yhat'], 0).astype(int)
    df_total_ct = df_total_ct.iloc[-1].tolist()
    df_total_ct = str(df_total_ct)

    df_dt = pred_df_total(df_d, country, year)

    df_total_dt = round(df_dt['yhat'], 0).astype(int)
    df_total_dt = df_total_dt.iloc[-1].tolist()
    df_total_dt = str(df_total_dt)

    labels = ['Cases', 'Deaths']
    values = [df_total_ct, df_total_dt]

    pie_chart = go.Figure(data=[go.Pie(labels=labels,
                                       values=values)])
    pie_chart.update_layout(template="seaborn")

    return pie_chart


def cases_deaths_line(country, axis_type):
    # df = df_for_cases_deaths_pred(country)
    # df = df_for_cases_deaths_pred_year(country, 2022)

    df_cases = combine_pred_avaible_cases(country)
    df_cases['ds'] = pd.to_datetime(df_cases['ds'])
    df_cases['ds'] = df_cases['ds'].dt.date

    date = datetime.datetime.strptime('2021-12-31', '%Y-%m-%d').date()

    df_2022_cases = df_cases[(df_cases['ds'] > date)]

    df_deaths = combine_pred_avaible_deaths(country)
    df_deaths['ds'] = pd.to_datetime(df_deaths['ds'])
    df_deaths['ds'] = df_deaths['ds'].dt.date

    df_2022_deaths = df_deaths[(df_deaths['ds'] > date)]

    line_chart = make_subplots(specs=[[{"secondary_y": True}]])
    line_chart.add_trace(go.Scatter(
        x=df_2022_cases.ds,
        y=signal.savgol_filter(df_2022_cases.yhat, 35, 3),
        mode='lines',
        name='Cases'
    ), secondary_y=False)

    line_chart.add_trace(go.Scatter(
        x=df_2022_deaths.ds,
        y=signal.savgol_filter(df_2022_deaths.yhat, 35, 3),
        mode='lines',
        name='Deaths'
    ), secondary_y=True)

    line_chart.update_layout(yaxis={
        'type': 'linear' if axis_type == 'Linear' else 'log'
    })
    line_chart.update_layout(template="seaborn")
    # line_chart.update_layout(hovermode="x unified")
    line_chart.update_xaxes(title='Date', showgrid=False)
    line_chart.update_yaxes(title_text="Total Cases", secondary_y=False)
    line_chart.update_yaxes(title_text="Total Deaths", secondary_y=True)

    return line_chart


def cases_deaths_line_cumm(country, axis_type):
    # cumm_deaths = get_pred_line_cumm_deaths(country, axis_type)
    # cumm_cases = get_pred_line_cumm_cases(country, axis_type)

    cumm_cases = get_pred_cases_cumm(country)
    cumm_cases['ds'] = pd.to_datetime(cumm_cases['ds'])
    cumm_cases['ds'] = cumm_cases['ds'].dt.date

    date = datetime.datetime.strptime('2021-12-31', '%Y-%m-%d').date()

    df_2022_cases = cumm_cases[(cumm_cases['ds'] > date)]

    cumm_deaths = get_pred_deaths_cumm(country)
    cumm_deaths['ds'] = pd.to_datetime(cumm_deaths['ds'])
    cumm_deaths['ds'] = cumm_deaths['ds'].dt.date

    df_2022_deaths = cumm_deaths[(cumm_deaths['ds'] > date)]

    cumm_line = make_subplots(specs=[[{"secondary_y": True}]])

    # cumm_line = go.Figure()

    cumm_line.add_trace(go.Scatter(
        x=df_2022_cases.ds,
        y=df_2022_cases.yhat,
        mode='lines',
        name='Cases'
    ), secondary_y=False)

    cumm_line.add_trace(go.Scatter(
        x=df_2022_deaths.ds,
        y=df_2022_deaths.yhat,
        mode='lines',
        name='Deaths'
    ), secondary_y=True)

    cumm_line.update_layout(yaxis={
        'type': 'linear' if axis_type == 'Linear' else 'log'
    })

    cumm_line.update_layout(template="seaborn")

    cumm_line.update_layout(hovermode="x unified")

    return cumm_line


my_line = cases_deaths_line('Malaysia', 'Linear')
# my_line.show()

my_line_cumm = cases_deaths_line_cumm('Malaysia', 'Linear')
# my_line_cumm.show()

my_pie = pie_deaths_cases('Malaysia', 2022)
# my_pie.show()

my_pie2 = pie_deaths_cases('Malaysia', 2021)


# my_pie2.show()


# ---------------------------------------------------- GET TOTALS FOR PREDICTION ---------------------------------------

def get_total_cases_2022(country):
    df = combine_pred_avaible_cases(country)
    df = pred_df_total(df, country, 2022)

    df_total = round(df['yhat'], 0).astype(int)
    df_total = df_total.iloc[-1].tolist()
    df_total = str(df_total)

    # print("total cases for country in 2022:")
    # print("---------------------------------------------------------------------")
    # print(df_total)
    # print("---------------------------------------------------------------------")

    return df_total


def get_total_deaths_2022(country):
    df = combine_pred_avaible_deaths(country)
    df = pred_df_total(df, country, 2022)

    df_total = round(df['yhat'], 0).astype(int)
    df_total = df_total.iloc[-1].tolist()
    df_total = str(df_total)

    # print("total deaths for country in 2022:")
    # print("---------------------------------------------------------------------")
    # print(df_total)
    # print("---------------------------------------------------------------------")

    return df_total


# -------------------------------- BAR CHARTS FOR COMPARING PAST/PRESENT WITH FUTURE -------------------------------

# user can choose the year for the past/present

def update_bars(df, x, y, numbers, view):
    fig = px.bar(data_frame=df,
                 x=x,
                 y=y,
                 hover_data=[x],
                 height=600,
                 orientation='h',
                 labels={x: 'Total ' + numbers},
                 template='ggplot2',
                 color=x)

    fig.update_layout(template="seaborn",
                      barmode='stack',
                      xaxis={
                          'title': 'Total ' + numbers,
                          'categoryorder': 'total descending'
                      },
                      yaxis={
                          'title': view
                      },
                      title_text=numbers + " Comparison Over Time")

    fig.update_traces(marker_line_width=0)

    return fig


def get_df_year(country, cases_deaths, year):
    if cases_deaths == 'new_deaths':
        df = combine_pred_avaible_deaths(country)
    else:
        df = combine_pred_avaible_cases(country)

    df = df[['ds', 'yhat']]
    df['yhat'] = df['yhat'].astype(int)

    df['ds'] = pd.to_datetime(df['ds'])
    df['year'] = df['ds'].dt.year
    df['month'] = df['ds'].dt.month

    pd.DatetimeIndex(df.ds).to_period("M")

    per = df.ds.dt.to_period("M")
    df = df.groupby([per])[['yhat']].sum()

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    df['ds'] = df.ds.astype(str)
    # df = gd.covid_data_month
    # df = df[df['location'] == country]

    year = str(year)
    df = df[df['ds'].str.contains(year)]

    # print("df for a particular year (month-year):")
    # print("---------------------------------------------------------------------")
    # print(df)
    # print("---------------------------------------------------------------------")

    # year = str(year)
    # df = df[df['ds'].str.contains(year)]

    return df


def get_bar_current(country, year, cases_deaths):
    # cases_deaths = new_cases OR new_deaths

    df = get_df_year(country, cases_deaths, year)

    # if year == 2022:
    #     bar_chart = get_bar_future(country, cases_deaths, label)
    # else:

    if year == 2022:
        if cases_deaths == 'new_deaths':
            label = 'Predicted Deaths'
        else:
            label = 'Predicted Cases'
    else:
        if cases_deaths == 'new_deaths':
            label = 'Confirmed Deaths'
        else:
            label = 'Confirmed Cases'

    bar_chart = px.bar(df,
                       x='ds',
                       y=df.yhat,
                       hover_data=['ds', 'yhat'],
                       color='yhat',
                       labels={
                           'ds': 'Month of Year',
                           'yhat': label
                       })
    bar_chart.update_layout(template="seaborn")

    return bar_chart


my_bar = get_bar_current('Malaysia', 2021, 'new_cases')
# my_bar.show()

my_future = get_bar_current('Malaysia', 2022, 'new_cases')


# my_future.show()

# DF OF CURRWENTR MEASURES

def get_current_measures(country):
    measures_df = gd.strictness
    measures_df['date'] = pd.to_datetime(measures_df['date'], format='%Y%m%d')

    measures_df = measures_df[measures_df['location'] == country]
    measures_df_last_row = measures_df.tail(1)
    # print("last row for measures_df:")
    # print(measures_df_last_row)

    most_recent_face = measures_df_last_row['Face Covering Measures'].astype(int).iloc[-1].tolist()
    most_recent_border = measures_df_last_row['Border Control Measures'].astype(int).iloc[-1].tolist()
    most_recent_home = measures_df_last_row['Stay At Home Measures'].astype(int).iloc[-1].tolist()
    most_recent_vacc = measures_df_last_row['Vaccination Policy'].astype(int).iloc[-1].tolist()

    # Stay At Home Measures, Border Control Measures, Face Covering Measures, Vaccination Policy
    most_recent_face = str(most_recent_face)
    most_recent_border = str(most_recent_border)
    most_recent_home = str(most_recent_home)
    most_recent_vacc = str(most_recent_vacc)

    most_recent = [most_recent_face, most_recent_border, most_recent_home, most_recent_vacc]

    return most_recent


my_recent = get_current_measures('Malaysia')
jpn_recent = get_current_measures('Japan')
afg_recent = get_current_measures('Afghanistan')
aus_recent = get_current_measures('Australia')
deu_recent = get_current_measures('Germany')
grc_recent = get_current_measures('Greece')
pol_recent = get_current_measures('Poland')
saf_recent = get_current_measures('South Africa')

current = {'Country': ['Malaysia', 'Japan', ' Afghanistan', 'South Africa',
                       'Germany', 'Greece', 'Poland', 'Australia'],
           'Face Covering Measures': [my_recent[0], jpn_recent[0], afg_recent[0], aus_recent[0], deu_recent[0],
                                      grc_recent[0], pol_recent[0], saf_recent[0]],
           'Border Closure Measures': [my_recent[1], jpn_recent[1], afg_recent[1], aus_recent[1], deu_recent[1],
                                       grc_recent[1], pol_recent[1], saf_recent[1]],
           'Stay At Home Measures': [my_recent[2], jpn_recent[2], afg_recent[2], aus_recent[2], deu_recent[2],
                                     grc_recent[2], pol_recent[2], saf_recent[2]],
           'Vaccination Policy': [my_recent[3], jpn_recent[3], afg_recent[3], aus_recent[3], deu_recent[3],
                                  grc_recent[3], pol_recent[3], saf_recent[3]],
           'Boosters Being Given?': ['Yes', 'Yes', 'No', 'Yes', 'Yes',
                                     'Yes', 'Yes', 'Yes']
           }

current_measures = pd.DataFrame(current)
# current_measures.to_csv("current_measureS_test.csv")
# print(current_measures)
