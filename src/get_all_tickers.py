from finviz.screener import Screener

#Get all tickers list
ticker_list = Screener(filters=[])
print(ticker_list)

ticker_list.to_csv('ticker.csv')