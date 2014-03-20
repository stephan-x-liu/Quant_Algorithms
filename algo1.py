# Put any initialization logic here.  The context object will be passed to
# the other methods in your algorithm.
import math
import numpy as np  

atr  = ta.ATR(timeperiod = 7)
bbands = ta.BBANDS(timeperiod = 7)


def initialize(context):
    ##Trade with stock spy
    stock_id=8554  ## SPY stock Id, used for testing 
    context.stock=stock_id
    ## change the context.values?

    set_universe(universe.DollarVolumeUniverse(floor_precentile=98.0,ceiling_percentile=100.0)) ## sets the universe to the current mode

# Will be called on every trade event for the securities you specify. 
# Test implementation for SPY stock 
# 
def handle_data(context, data):
    # Implement your algorithm logic here.
    volatility=volatility_stop(data) 


    atr_data = atr(data) # initaliaze the data
    atr_data*=3 

    bbands_data = bbands(data) # returns a tuple of (upper, line, lower)
    time_period=7


    upper_band=bbands_data[0]
    lower_band=bbands_data[2]

    # data[sid(X)] holds the trade event data for that security.
    # context.portfolio holds the current portfolio state.

    # Place orders with the order(SID, amount) method.

    # TODO: implement your own logic here.

    #this will only order if a volatility boundary is hit 
    order(sid(24), 50)


  
def volatility_stop(data):  #measures volatility stop for 7 day period
	
	calc_inital_trend=True
	if calc_inital_trend:
		uptrend=(history(1,"1d",'close_price')- history(7,"1d",'open_price'))>0
		calc_inital_trend=False


	high_close_SIC=nil 
	low_close_SIC=nil 

	# Below calculate the SIC 
	i=1
	price_history=[]
	while i<8:
		price_history=.append(history(bar_count=i, frequency="1d", field='close_price')) #tuple with closing price i days ago

	if uptrend:
		high_close_SIC=max(price_history)
	else:
		low_close_SIC=min(price_history)

	 ## returns tuple with boolean true for uptrend and the highclose or low close
	 if uptrend:
	 	return (True, high_close_SIC)
	 return (False, low_close_SIC)



