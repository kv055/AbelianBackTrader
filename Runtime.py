import backtrader as bt
import Strategy
from BasicSetup import cerebro

# Add a strategy
cerebro.addstrategy(Strategy.TestStrategy)

#Run the Strategy
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
