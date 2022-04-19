# this page will include a list of the data to use
# along with their sources and links
# in addition, there will be some basic functions to fix the dataframes
import pathlib
import warnings

import numpy as np
import pandas as pd

warnings.filterwarnings("ignore")

# # data for basic visualisations
#
# # 1. Number of cases (JHU CSSE)
# # 2. Number of deaths (JHU CSSE)

# covid_data_link = 'https://raw.githubusercontent.com/FYPRepo/covid_data/main/covid_data_owid.csv'
# covid_data = pd.read_csv(covid_data_link)

PATH1 = pathlib.Path(__file__).parent
DATA_PATH1 = PATH1.joinpath("../COVID_DATA").resolve()
covid_data_path = DATA_PATH1.joinpath("covid_data_owid.csv")
# covid_data = pd.read_csv('../COVID_Data/covid_data_owid.csv', index_col=0)
covid_data = pd.read_csv(covid_data_path, index_col=0)


# covid_data = covid_data[['iso_code',
#                          'location',
#                          'date',
#                          'new_cases',
#                          'new_cases_smoothed',
#                          'new_deaths',
#                          'new_deaths_smoothed',
#                          'population']]

# print("covid_data dataframe: (covid data from OWID) ")
# print("--------------------------------------------------------------------------- ")
# print(covid_data.head())
# print("--------------------------------------------------------------------------- ")
# covid_data.to_csv('covid_data')

# print("covid_data dataframe columns: (covid data from OWID) ")
# print("--------------------------------------------------------------------------- ")
# print(list(covid_data.columns))
# print("--------------------------------------------------------------------------- ")

# extracting the year and month from the dates
covid_data['date'] = pd.to_datetime(covid_data['date'])
covid_data['year'] = covid_data['date'].dt.year
covid_data['month'] = covid_data['date'].dt.month


def get_df_owid_year(df):
    # grouping data by country and year, shows the total number of cases for each country by year
    df = df.groupby(['location', 'year'])[['new_cases', 'new_deaths']].sum()
    df.reset_index(inplace=True)
    df.reset_index(drop=True)
    # print(df[:5])

    return df


def get_df_owid_month(df):
    pd.DatetimeIndex(df.date).to_period("M")

    per = df.date.dt.to_period("M")
    df = df.groupby(['location', per])[['new_cases', 'new_deaths']].sum()

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    df['date'] = df.date.astype(str)

    # print(df[:5])

    return df


def get_df_owid_total(df):
    df = df.groupby(['location'])[['new_cases', 'new_deaths']].sum()
    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    # print(df[:5])

    return df


covid_data_total = get_df_owid_total(covid_data)
# print("covid_data_total: (covid data total for each country)")
# print("--------------------------------------------------------------------------- ")
# print(covid_data_total.head())
# print("--------------------------------------------------------------------------- ")

covid_data_year = get_df_owid_year(covid_data)
# print("covid_data_year: (covid data total of each year for each country)")
# print("--------------------------------------------------------------------------- ")
# print(covid_data_year.head())
# print("--------------------------------------------------------------------------- ")

covid_data_month = get_df_owid_month(covid_data)
# print("covid_data_month: (covid data by month for each country)")
# print("--------------------------------------------------------------------------- ")
# print(covid_data_month.head())
# print("--------------------------------------------------------------------------- ")

# strictness_link = 'https://raw.githubusercontent.com/FYPRepo/covid_data/main/strictest_measures.csv'
# strictness = pd.read_csv(strictness_link)

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../COVID_DATA").resolve()
strictness_path = DATA_PATH.joinpath("strictest_measures.csv")
strictness = pd.read_csv(strictness_path, index_col=0)

strictness[strictness['Stay At Home Measures'] == ""] = np.NaN
strictness[strictness['Border Control Measures'] == ""] = np.NaN
strictness[strictness['Face Covering Measures'] == ""] = np.NaN
strictness[strictness['Vaccination Policy'] == ""] = np.NaN
strictness[strictness['Total Strictness'] == ""] = np.NaN
strictness.fillna(method='ffill', inplace=True)
# strictness.to_csv("strictness_test.csv")

# print("strictest_measures dataframe: (measures taken by each country)")
# print("--------------------------------------------------------------------------- ")
# print(strictness.head())
# print("--------------------------------------------------------------------------- ")


strictness['Date'] = pd.to_datetime(strictness['Date'], format='%Y%m%d')
# strictness['Date'] = pd.to_datetime(strictness['Date'])
strictness['year'] = strictness['Date'].dt.year
strictness['month'] = strictness['Date'].dt.month

# first we rename the columns in the vacc policy from entity to location, code to iso_code, day to date
# same for strictness

# vaccination_policies.rename(columns={'Entity': 'location', 'Code': 'iso_code', 'Day': 'date'}, inplace=True)
strictness.rename(columns={'CountryName': 'location', 'CountryCode': 'iso_code', 'Date': 'date'}, inplace=True)
# print("strictest_measures dataframe with renamed columns:")
# print("--------------------------------------------------------------------------- ")
# print(strictness.head())
# print("--------------------------------------------------------------------------- ")
#
# strictness_avg = (strictness.groupby(['location'])
#                   .agg({'Total Strictness': 'mean'})
#                   .rename(columns={'Total Strictness': 'Average Strictness'}))
# print("strictness_avg dataframe: (average strictness per country)")
# print("--------------------------------------------------------------------------- ")
# print(strictness_avg)
# print("--------------------------------------------------------------------------- ")
# strictness_avg.to_csv('/COVID_Data/average_strictness.csv')

# print(vaccination_policies.head())
# print(strictness.head())

# then we merge with covid_data
# merge vaccination policies first

# then merge those with strictness measures

all_data = pd.merge(covid_data, strictness,
                    on=['location', 'date', 'iso_code'], how="left")
# print("list of columns in all_data:")
# print("--------------------------------------------------------------------------- ")
# print(list(all_data.columns))
# print("--------------------------------------------------------------------------- ")


# print("list of countries:")
# print("--------------------------------------------------------------------------- ")
countries = list(all_data['location'].unique())
# print(countries)
# print("--------------------------------------------------------------------------- ")

# all_data = pd.read_csv('../COVID_Data/strictest_measures.csv')
# print(all_data)


# print("all_data dataframe:")
# print("--------------------------------------------------------------------------- ")
# print(all_data)
# print("--------------------------------------------------------------------------- ")


# all_data_month = get_df_owid_month_cases(all_data)
# print(all_data_month)

def get_df_measures_month(df, measure):
    pd.DatetimeIndex(df.date).to_period("M")

    per = df.date.dt.to_period("M")
    # df = df.groupby(['Entity', per])[[measure]].max()

    df = (df.groupby(['location', per])
          .agg({'new_cases': 'sum',
                'new_deaths': 'sum',
                measure: 'max'})
          .rename(columns={'new_cases': 'Total Cases',
                           'new_deaths': 'Total Deaths',
                           measure: measure}))

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    df['date'] = df.date.astype(str)

    # print(df[:5])

    return df


measures = ['Total Strictness', 'Vaccination Policy',
            'Face Covering Measures', 'Border Control Measures',
            'Stay At Home Measures']


# for stacked barchart to find measures per month
def get_df_all_measures_month(df):
    pd.DatetimeIndex(df.date).to_period("M")

    per = df.date.dt.to_period("M")
    # df = df.groupby(['Entity', per])[[measure]].max()

    df = (df.groupby(['location', per])
          .agg({'new_cases': 'sum',
                'new_deaths': 'sum',
                'Total Strictness': 'max',
                'Vaccination Policy': 'max',
                'Face Covering Measures': 'max',
                'Border Control Measures': 'max',
                'Stay At Home Measures': 'max'})
          .rename(columns={'new_cases': 'Total Cases',
                           'new_deaths': 'Total Deaths'}))

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    df['date'] = df.date.astype(str)

    # print(df[:5])

    return df


# to find correlation for scatter plot
def get_df_measures_cases(df, measure):
    # df = df.groupby(['Entity', per])[[measure]].max()

    df = (df.groupby(['location', measure])
          .agg({'new_cases': 'sum',
                'new_deaths': 'sum'})
          .rename(columns={'new_cases': 'Total Cases',
                           'new_deaths': 'Total Deaths'}))

    df.reset_index(inplace=True)
    df.reset_index(drop=True)

    # print(df[:5])

    return df


measures_cases = get_df_measures_cases(all_data, 'Total Strictness')
# print("measures_cases df: (a single measure with cases and deaths per day)")
# print("--------------------------------------------------------------------------- ")
# print(measures_cases)
# print("--------------------------------------------------------------------------- ")

all_data_monthly = get_df_measures_month(all_data, 'Total Strictness')
# print("all_data_monthly df: (a single measure with cases and deaths in a month)")
# print("--------------------------------------------------------------------------- ")
# print(all_data_monthly)
# print("--------------------------------------------------------------------------- ")

all_data_month = get_df_owid_month(all_data)
# print("all_data_month df: (cases and deaths per month)")
# print("--------------------------------------------------------------------------- ")
# print(all_data_month)
# print("--------------------------------------------------------------------------- ")

# print("names of columns in the all_data_month df: (cases and deaths per month)")
# print("--------------------------------------------------------------------------- ")
# print(list(all_data_month.columns))
# print("--------------------------------------------------------------------------- ")

# all_data_month_deaths = get_df_owid_month_cases(all_data)
# print("all_data_month_deaths df: (cases and deaths per month)")
# print("--------------------------------------------------------------------------- ")
# print(all_data_month)
# print("--------------------------------------------------------------------------- ")

all_measures_monthly = get_df_all_measures_month(all_data)
# print("all_measures_monthly dataframe: (all measures with cases and deaths per month)")
# print("--------------------------------------------------------------------------- ")
# print(all_measures_monthly)
# print("--------------------------------------------------------------------------- ")
# print("column names of all_measures_monthly dataframe:")
# print("--------------------------------------------------------------------------- ")
# print(list(all_measures_monthly.columns))
# print("--------------------------------------------------------------------------- ")

# 6. GeoJSON Maps

world_map = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'

# print(px.colors.sequential.Sunset)
