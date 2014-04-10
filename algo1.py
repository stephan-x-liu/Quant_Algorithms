import datetime
import time

atr  = ta.ATR(timeperiod = 7)
bbands = ta.BBANDS(timeperiod = 7)
uptrend = True
last_bought = None
upchecker = False
downchecker = False

def initialize(context):
	##Trade with stock spy

	context.stock=sid(8554)
	context.calc_inital_trend = True
	context.high_close_SIC = 0
	context.low_close_SIC = 999999999
	context.already_bought = False
	context.order_id = None
    context.last_5 = []
	## change the context.values?
	set_universe(universe.DollarVolumeUniverse(floor_percentile=98.0,ceiling_percentile=100.0)) ## sets the universe to the current mode


	# Will be called on every trade event for the securities you specify. 
	# Test implementation for SPY stock 
	# 
def handle_data(context, data):

	global uptrend
	global last_bought
	global upchecker
	global downchecker

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
	deltatime = datetime.timedelta(days = 1)
	checker = current_time - deltatime

	current_time_time = current_time.time()

	to_buy = False
	if current_time_time > datetime.time(9,0) or current_time_time<datetime.time(9,10):
		to_buy = True
	elif current_time_time > datetime.time(15,30) and current_time_time<datetime.time(15,35):
		to_buy = True



	volatility=volatility_stop(context,data)
	record(vstops = volatility, price = data[context.stock].price)


	if uptrend and not context.already_bought:
		context.order_id=order(context.stock, 50)
		context.already_bought=True 
		last_bought = current_time - deltatime - deltatime
 

	print("BUY TIME YET?",checker>last_bought)


	if uptrend and checker>last_bought and to_buy:
		print("INSIDE UPTREND LOOP",data[context.stock].price< volatility)
		if data[context.stock].price< volatility:
			print("SELLING STOCK","VSTOP:",volatility,"PRICE",data[context.stock].price)
			context.order_id=order(context.stock, -50)
			uptrend=False
			last_bought = current_time

	if not uptrend and checker>last_bought and to_buy:
		if data[context.stock].price>volatility:
			print("BUYING STOCK","VSTOP:",volatility,"PRICE",data[context.stock].price)
			context.order_id=order(context.stock, 50)
			uptrend=True
			last_bought = current_time

		
	print("IS UPTREND?",uptrend==True)
	log.info(context.portfolio.positions[context.stock])


def volatility_stop(context,data):  #measures volatility stop for 7 day period
	if context.calc_inital_trend:
		context.uptrend=(history(1,"1d",'close_price')- history(7,"1d",'open_price'))>0
		context.calc_inital_trend=False

	# Below calculate the SIC 


	price_history = history(bar_count=8, frequency="1d", field='close_price')[context.stock] #tuple with closing price i days ago
	if uptrend:
		context.high_close_SIC=max(price_history[1:])
	else:
		context.low_close_SIC=min(price_history[1:])

	atr_data = atr(data) # initaliaze the data
	atr_value=atr_data[context.stock]
	atr_value*=3 	

	## returns tuple with boolean true for uptrend and the highclose or low close
	if uptrend:
		return context.high_close_SIC-atr_value
	return context.low_close_SIC+atr_value

