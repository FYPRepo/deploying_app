import datetime as dt

import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import warnings

warnings.filterwarnings("ignore")

# date to predict data for
# in ordinal form
# predictdate = 738243

# date_today = dt.datetime.today().strftime("%Y-%m-%d")
date_today = dt.datetime.today()
date_tomorrow = dt.date.today() + dt.timedelta(days=1)
date_tomorrow = date_tomorrow.strftime("%Y-%m-%d")
# predictdate = date_tomorrow.toordinal()
# date_tomorrow = date_tomorrow.strftime("%Y-%m-%d")

confirmed_link = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data' \
                 '/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv '
confirmed = pd.read_csv(confirmed_link)


def time_series(df):
    drop_columns = ['Lat',
                    'Long',
                    'Province/State']

    df.drop(columns=drop_columns, inplace=True)

    df_grouped = df.groupby(['Country/Region'], as_index=False).sum()
    df_grouped = df_grouped.set_index('Country/Region').transpose()
    df_grouped.reset_index(level=0, inplace=True)
    df_grouped.rename(columns={'index': 'Date'}, inplace=True)
    df_grouped['Date'] = pd.to_datetime(df_grouped['Date'])

    #     print(df_grouped[:5])

    return df_grouped


ts_confirmed = time_series(confirmed)
df_confirmed = ts_confirmed


def get_dataframe(country, case_type):
    # 1 = confirmed (cumulative)
    # 2 = cases per day

    # relevant features
    pivot = pd.pivot_table(df_confirmed,
                           values=country,
                           index='Date').sort_values(by='Date')

    confirmed_final = pd.DataFrame(pivot)

    confirmed_final.reset_index(inplace=True)

    Confirmed = confirmed_final[['Date', country]]
    df_c = Confirmed
    df_c['Confirmed'] = df_c[country]

    df_c['Cases_per_day'] = df_c['Confirmed'].diff()
    df_c = df_c.fillna(0)
    df_c['Cases_per_day'] = df_c['Cases_per_day'].astype(int)

    if case_type == 2:
        columns = ['Date', 'Cases_per_day']
    else:
        columns = ['Date', 'Confirmed']

    df = df_c[columns]

    df['Date'] = pd.to_datetime(df['Date'])
    df['Date'] = df['Date'].map(dt.datetime.toordinal)

    return df


def get_x_y(df, case_type):
    x = df['Date']

    if case_type == 2:
        y = df['Cases_per_day']
    else:
        y = df['Confirmed']

    return x, y


def forest_reg(country, case_type):
    df = get_dataframe(country, case_type)
    df.sum(axis=0)
    print(df.head())

    x, y = get_x_y(df, case_type)

    xtrain, xtest, ytrain, ytest = train_test_split(x, y,
                                                    test_size=0.2,
                                                    random_state=0)

    model = RandomForestRegressor()

    model.fit(np.array(xtrain).reshape(-1, 1),
              ytrain.values.ravel())

    print(df.tail())

    # dt_ = datetime.fromordinal(738243)
    # print(dt_)

    ytrain.head()

    prediction = model.predict(np.array(xtest).reshape(-1, 1))

    # result = model.predict(np.array([[predictdate]]))
    # print(result)

    fdf = pd.DataFrame(prediction)
    fdf.plot()

    # rmse = mean_squared_error(ytest, prediction)
    # score = model.score(np.array(x).reshape(-1, 1),
    #                     np.array(y).reshape(-1, 1)) * 100

    # result = model.predict(np.array([[predictdate]]))  # tomorrow
    # r = result[0].astype(int)
    # print(r)

    date = date_tomorrow
    dte = dt.datetime.strptime(date, '%Y-%m-%d').toordinal()
    prediction_cases = model.predict([[dte]])
    print("Predicted cases on {}  is : {}".format(date, prediction_cases[0]))

    # pred_15 = []
    # dates = []
    # days = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    # for i in days:
    #     date = "2022-02-22"
    #     dte = dt.datetime.strptime(date, '%Y-%m-%d').toordinal()
    #     dtes = dte + i
    #     dates.append(dtes)
    #     prediction_cases = model.predict([[dtes]])
    #     pred_15.append(prediction_cases)
    #     pred = list(map(int, pred_15))
    #     pred_df = {'date': dates, 'prediction': pred}
    #     print("Predicted cases on {}  is : {}".format(dtes, prediction_cases.astype(int)))
    #
    # print(pred_df.head())

    # df.plot.line(x='Date', y='Cases_per_day')

    df2 = pd.DataFrame({'Actual': ytest, 'Predicted': prediction})
    print(df2.head())

    # Training_Score = model.score(np.array(xtrain).reshape(-1, 1),
    #                              np.array(ytrain).reshape(-1, 1))
    # print(Training_Score)

    # forest_evaluation(ytest, prediction)

    # pyplot.scatter(xtrain, ytrain, s=10)
    # # plot predictions as red dots
    # pyplot.scatter(xtest, prediction, s=10, c='red')
    # # plt.plot(xtest, pred, color='m')
    # pyplot.show()

    return prediction_cases[0]


def forest_evaluation(ytest, prediction):
    print('Mean Absolute Error:', metrics.mean_absolute_error(ytest, prediction))
    print('Mean Squared Error:', metrics.mean_squared_error(ytest, prediction))
    print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(ytest, prediction)))
    print('R-2:', metrics.r2_score(ytest, prediction))


# 1 = confirmed (cumulative)
# 2 = cases per day
# 3 = dead (cumulative)
# 4 = deaths per day

# next_day_my_case_day = forest_reg('Malaysia', 2)
# next_day_my_cases_cumm = forest_reg('Malaysia', 1)

# print("====== next day cases per day ====")
# print(next_day_my_case_day)
# print("===================================\n")
#
# print("====== next day cases cumm ====")
# print(next_day_my_cases_cumm)
# print("===================================\n")

# # cumulative cases
#
# df2 = get_dataframe('Malaysia', 1)
# print(df2.head())
#
# x2, y2 = get_x_y(df2, 1)
#
# xtrain2, xtest2, ytrain2, ytest2 = train_test_split(x2, y2, test_size=0.2, random_state=0)
#
# model2 = RandomForestRegressor()
#
# model2.fit(np.array(xtrain2).reshape(-1, 1), ytrain2.values.ravel())
#
# print(df2.tail())
# print(ytrain2.head())
#
# prediction2 = model2.predict(np.array(xtest2).reshape(-1, 1))
#
# fdf2 = pd.DataFrame(prediction2)
# fdf2.plot()
#
# result2 = model2.predict(np.array([[737932]]))
# rmse2 = mean_squared_error(ytest2, prediction2)
# score2 = model2.score(np.array(x2).reshape(-1, 1), np.array(y2).reshape(-1, 1)) * 100
#
# result2 = model2.predict(np.array([[predictdate]]))
# r2 = result2[0].astype(int)
# print(r2)
#
# date2 = "2022-04-29"
# dte2 = dt.datetime.strptime(date2, '%Y-%m-%d').toordinal()
# print(dte2)
# prediction_cases2 = model2.predict(np.array([[dte2]]))
# print("Predicted cases on {}  is : {}".format(date2, prediction_cases2[0]))
#
# pred_152 = []
# dates2 = []
# days2 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# for i in days2:
#     date2 = "2022-3-29"
#     dte2 = dt.datetime.strptime(date2, '%Y-%m-%d').toordinal()
#     dtes2 = dte2 + i
#     dates2.append(dtes2)
#     prediction_cases2 = model2.predict([[dtes2]])
#     pred_152.append(prediction_cases2)
#     pred2 = list(map(int, pred_152))
#     pred_df2 = {'date': dates2, 'prediction': pred2}
#     print("Predicted cases on {}  is : {}".format(dtes2, prediction_cases2.astype(int)))
#
# print(pred_df2)
#
# df2.plot.scatter(x='Date', y='Confirmed')
#
# df2 = pd.DataFrame({'Actual': ytest2, 'Predicted': prediction2})
# print(df2.head)
#
# Training_Score2 = model2.score(np.array(xtrain2).reshape(-1, 1),
#                                np.array(ytrain2).reshape(-1, 1))
# print(Training_Score2)
#
# print('Mean Absolute Error:', metrics.mean_absolute_error(ytest2, prediction2))
# print('Mean Squared Error:', metrics.mean_squared_error(ytest2, prediction2))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(ytest2, prediction2)))
# print('R-2:', metrics.r2_score(ytest2, prediction2))
#
# pyplot.scatter(xtrain2, ytrain2, s=10)
# # plot predictions as red dots
# pyplot.scatter(xtest2, prediction2, s=10, c='red')
# # plt.plot(xtest, pred, color='m')
# pyplot.show()
