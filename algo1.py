import datetime

atr  = ta.ATR(timeperiod = 7)
bbands = ta.BBANDS(timeperiod = 7)


def initialize(context):
	##Trade with stock spy

	context.stock=sid(8554)
	context.calc_inital_trend = True
	context.high_close_SIC = 0
	context.low_close_SIC = 999999999
	context.uptrend = True
	context.already_bought = False
	context.last_bought = datetime.datetime(10,10,10,10)
	## change the context.values?
	set_universe(universe.DollarVolumeUniverse(floor_percentile=98.0,ceiling_percentile=100.0)) ## sets the universe to the current mode


	# Will be called on every trade event for the securities you specify. 
	# Test implementation for SPY stock 
	# 
def handle_data(context, data):


	# money=context.portfolio.MONEY
	# Implement your algorithm logic here.

	##Find value of volatility stop 



	## calculating bbands 



	# data[sid(X)] holds the trade event data for that security.
	# context.portfolio holds the current portfolio state.

	# Place orders with the order(SID, amount) method.

	# TODO: implement your own logic here.

	#this will only order if a volatility boundary is hit 
	
	current_time = data[context.stock].datetime
	deltatime = datetime.timedelta(minutes=5)
	checker = current_time - deltatime

	volatility=volatility_stop(context,data)
	record(vstops = volatility, price = data[context.stock].price)


	if context.uptrend and not context.already_bought:
		order(context.stock, 50)
		context.already_bought=True 
		context.last_bought = current_time

	if checker>current_time:
		if context.uptrend:
			if data[context.stock].price< volatility:
				order(context.stock, -50)
				context.uptrend=False

		if not context.uptrend:
			if data[context.stock].price>volatility:
				order(context.stock, 50)
				context.uptrend=True
		context.last_bought = current_time


def volatility_stop(context,data):  #measures volatility stop for 7 day period
	if context.calc_inital_trend:
		context.uptrend=(history(1,"1d",'close_price')- history(7,"1d",'open_price'))>0
		context.calc_inital_trend=False

	# Below calculate the SIC 


	price_history = history(bar_count=7, frequency="1d", field='close_price')[context.stock] #tuple with closing price i days ago
	if context.uptrend:
		context.high_close_SIC=max(context.high_close_SIC,max(price_history))
	else:
		context.low_close_SIC=min(context.low_close_SIC,min(price_history))

	atr_data = atr(data) # initaliaze the data
	atr_value=atr_data[context.stock]
	atr_value*=3 	

	## returns tuple with boolean true for uptrend and the highclose or low close
	if context.uptrend:
		return context.high_close_SIC-atr_value
	return context.low_close_SIC+atr_value

