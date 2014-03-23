atr  = ta.ATR(timeperiod = 7)
bbands = ta.BBANDS(timeperiod = 7)
calc_inital_trend=True
high_close_SIC=0 
low_close_SIC=99999999
uptrend=True 

def initialize(context):
	##Trade with stock spy

	context.stock=sid(8554)
	## change the context.values?
	set_universe(universe.DollarVolumeUniverse(floor_percentile=98.0,ceiling_percentile=100.0)) ## sets the universe to the current mode


# Will be called on every trade event for the securities you specify. 
# Test implementation for SPY stock 
# 
def handle_data(context, data):

	global calc_inital_trend 
	global high_close_SIC
	global low_close_SIC
	global uptrend

	# money=context.portfolio.MONEY

	already_bought=False
	# Implement your algorithm logic here.

	##Find value of volatility stop 

	

	## calculating bbands 


	
	# data[sid(X)] holds the trade event data for that security.
	# context.portfolio holds the current portfolio state.

	# Place orders with the order(SID, amount) method.

	# TODO: implement your own logic here.

	#this will only order if a volatility boundary is hit 

	volatility=volatility_stop(context,data)

	if uptrend and not already_bought:
		order(context.stock, 50)
		already_bought=True 

	if uptrend:
		if data[context.stock].price< volatility:
			order(context.stock, -50)
			uptrend=False

   	if not uptrend:
   		if data[context.stock].price>volatility:
   			order(context.stock, 50)
   			uptrend=True


def volatility_stop(context,data):  #measures volatility stop for 7 day period
	
	global calc_inital_trend 
	global high_close_SIC
	global low_close_SIC
	global uptrend


	if calc_inital_trend:
		uptrend=(history(1,"1d",'close_price')- history(7,"1d",'open_price'))>0
		calc_inital_trend=False

	# Below calculate the SIC 
	k=(1,2,3,4,5,6,7)
	i=0


	price_history = history(bar_count=7, frequency="1d", field='close_price')[context.stock] #tuple with closing price i days ago
     
        
	if uptrend:
		high_close_SIC=max(high_close_SIC,max(price_history))
	else:
		low_close_SIC=min(low_close_SIC,min(price_history))

	atr_data = atr(data) # initaliaze the data
	atr_value=atr_data[context.stock]
	atr_value*=3 	

	 ## returns tuple with boolean true for uptrend and the highclose or low close
	if uptrend:
		return high_close_SIC-atr_value
	return low_close_SIC+atr_value


