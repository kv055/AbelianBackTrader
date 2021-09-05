import backtrader as bt
import datetime
#in this file we configure the cerebro class and add OHLC data to it
#Basic Setup for Cerebro
cerebro = bt.Cerebro()

#Add Cash
cerebro.broker.setcash(100000.0)

#Add OHLC Data
data = bt.feeds.YahooFinanceCSVData(
    #file or filepath
    dataname='BTC-USD.csv',
    # Do not pass values before this date
    fromdate=datetime.datetime(2020, 9, 5),
    # Do not pass values after this date
    todate=datetime.datetime(2021, 9, 4),
    reverse=False)

# Add the Data Feed to Cerebro
cerebro.adddata(data)