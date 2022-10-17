from collections import OrderedDict
import json
import math
import pandas as pd
import re
import yfinance as yf

regex_list = ['2010-01', '2010-02', '2010-03', '2010-04', '2010-05', '2010-06', '2010-07', '2010-08', '2010-09',
              '2010-10', '2010-11', '2010-12',
              '2011-01', '2011-02', '2011-03', '2011-04', '2011-05', '2011-06', '2011-07', '2011-08', '2011-09',
              '2011-10', '2011-11', '2011-12',
              '2012-01', '2012-02', '2012-03', '2012-04', '2012-05', '2012-06', '2012-07', '2012-08', '2012-09',
              '2012-10', '2012-11', '2012-12',
              '2013-01', '2013-02', '2013-03', '2013-04', '2013-05', '2013-06', '2013-07', '2013-08', '2013-09',
              '2013-10', '2013-11', '2013-12',
              '2014-01', '2014-02', '2014-03', '2014-04', '2014-05', '2014-06', '2014-07', '2014-08', '2014-09',
              '2014-10', '2014-11', '2014-12',
              '2015-01', '2015-02', '2015-03', '2015-04', '2015-05', '2015-06', '2015-07', '2015-08', '2015-09',
              '2015-10', '2015-11', '2015-12',
              '2016-01', '2016-02', '2016-03', '2016-04', '2016-05', '2016-06', '2016-07', '2016-08', '2016-09',
              '2016-10', '2016-11', '2016-12',
              '2017-01', '2017-02', '2017-03', '2017-04', '2017-05', '2017-06', '2017-07', '2017-08', '2017-09',
              '2017-10', '2017-11', '2017-12',
              '2018-01', '2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07', '2018-08', '2018-09',
              '2018-10', '2018-11', '2018-12',
              '2019-01', '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07', '2019-08', '2019-09',
              '2019-10', '2019-11', '2019-12',
              '2020-01', '2020-02', '2020-03', '2020-04', '2020-05', '2020-06', '2020-07', '2020-08', '2020-09',
              '2020-10', '2020-11', '2020-12',
              '2021-01', '2021-02', '2021-03', '2021-04', '2021-05', '2021-06', '2021-07', '2021-08', '2021-09',
              '2021-10', '2021-11', '2021-12',
              '2022-01']


# ----------------------------------------------------------------------------------------------------------------------

def get_change(current, previous):
    if current == previous:
        return 0
    try:
        return ((current - previous) / previous) * 100.0
    except ZeroDivisionError:
        return 0


def get_first_date_of_month_with_data(stocks_data):
    dates = []
    for index, row in stocks_data.iterrows():
        dates.append(str(index)[0:10])
    dates.sort()
    result = []
    for regex in regex_list:
        r = re.compile(regex + ".*")
        matched_dates = list(filter(r.match, dates))
        if len(matched_dates) > 0:
            matched_dates.sort()
            result.append(matched_dates[0])
    return result


# ----------------------------------------------------------------------------------------------------------------------

ticker_list = pd.read_csv('ticker.csv')

sector = "Consumer Cyclical"
tickers = []

for index, row in ticker_list.iterrows():
    if row['Sector'] == sector and row['Industry'] != "Shell Companies":
        tickers.append(row['Ticker'])

print(tickers)
stock_monthly_price_change_data = {}



for ticker in tickers:
    if pd.isna(ticker):
        continue

    try:
        data = yf.download(ticker, '2010-01-01', '2022-01-31')
    except:
        print("Exception occurred while downloading data.")
        continue

    dates = []
    dates = get_first_date_of_month_with_data(data)

    first = True
    prev = 0
    for date in dates:
        for index, row in data.iterrows():
            date_str = str(index)[0:10]
            if date_str == date:
                if first:
                    prev = row['Adj Close']
                    first = False
                    continue
                change = get_change(row['Adj Close'], prev)
                prev = row['Adj Close']

                #Not to insert infinity
                if math.isinf(change):
                    continue

                if change > 1000:
                    continue

                if date_str in stock_monthly_price_change_data:
                    stock_monthly_price_change_data[date_str].append(change)
                else:
                    stock_monthly_price_change_data[date_str] = []
                    stock_monthly_price_change_data[date_str].append(change)

    # Clearing the dataframe
    data = data.iloc[0:0]
    print("Done calculation for ticker : " + ticker)

stock_price_change_avg = {}
for key in stock_monthly_price_change_data:
    avg = sum(stock_monthly_price_change_data[key]) / len(stock_monthly_price_change_data[key])
    stock_price_change_avg[key] = avg

stock_price_change_avg_ordered = OrderedDict(sorted(stock_price_change_avg.items()))
print(stock_price_change_avg_ordered)
with open("../data/orig/" + sector + ".json", "w") as outfile:
    json.dump(stock_price_change_avg_ordered, outfile)
