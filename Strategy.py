from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
                        
# Import the backtrader platform
import backtrader as bt
from backtrader.trade import TradeHistory
from BasicSetup import cerebro

TradesLog = {
    'Direction':[],
    'Amount':[],
    'AssetPrice':[],
    'Return':[],
    'PortfolioValue':[]
}
# Create a Stratey
class TestStrategy(bt.Strategy):
    

    #Base Logic starts (do not mess with this) --------------------------
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close

        # To keep track of pending orders
        self.order = None

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enough cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED, %.2f' % order.executed.price)
                TradesLog['Direction'].append('Buy')
                TradesLog['AssetPrice'].append(order.executed.price)
                TradesLog['PortfolioValue'].append(cerebro.broker.getvalue())
                print(len(self))
                # print(TradesLog)

            elif order.issell():
                self.log('SELL EXECUTED, %.2f' % order.executed.price)
                TradesLog['Direction'].append('Sell')
                TradesLog['AssetPrice'].append(order.executed.price)
                TradesLog['PortfolioValue'].append(cerebro.broker.getvalue())
                print(len(self))
                # print(TradesLog)

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None
    #Base logic ends -------------------------------------------------------

    def next(self):
        # Simply log the closing price of the series from the reference
        # self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:
            #!!!! Implement Buy condition logic here as an if statement !!!!
            # Not yet ... we MIGHT BUY if ...
            # current close less than previous close
            if self.dataclose[0] < self.dataclose[-1]:

                #Execute Buy order
                # BUY (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.buy()

        else:
            #!!!! Implement Sell condition logic here as an if statement !!!!

            # Already in the market ... we might sell
            if len(self) >= (self.bar_executed + 5):

                #Execute Sell order
                # SELL (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell()
