from finviz.screener import Screener

#Get all tickers list
ticker_list = Screener(filters=[])


ticker_list.to_csv('ticker.csv')