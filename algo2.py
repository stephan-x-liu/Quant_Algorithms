import datetime
import time

atr  = ta.ATR(timeperiod = 7)
bbands = ta.BBANDS(timeperiod = 7)

def initialize(context):
	##Trade with stock spy

	context.stock=sid(8554)
	context.calc_inital_trend = True
	context.high_close_SIC = 0
	context.low_close_SIC = 999999999
	context.already_bought = False
	context.order_id = None
	context.last_5 = []
	context.last_bought = None
	context.uptrend = True
	context.sellcounter = 0
	context.buycounter = 0
	set_universe(universe.DollarVolumeUniverse(floor_percentile=98.0,ceiling_percentile=100.0)) ## sets the universe to the current mode


def handle_data(context, data):

	current_time = data[context.stock].datetime.time()
	if(current_time>datetime.time(15,55)):
		context.last_5=[]
		return
	

	context.last_5.append(data[context.stock].price)
	if(len(context.last_5)<6):
		return
	context.last_5.pop(0)

	volatility=volatility_stop(context,data)
    
	print("PRICE:",data[context.stock].price,"VSTOP:",volatility,"UPTREND",context.uptrend, "LAST 5:",context.last_5)

	if context.uptrend and not context.already_bought:
		context.order_id=order(context.stock, 50)
		context.already_bought=True 


	if context.uptrend == True:
		if data[context.stock].price< volatility:
			context.sellcounter+=1
			if context.sellcounter >= 7:
				print("SELLING STOCK","VSTOP:",volatility,"PRICE",data[context.stock].price)
				context.order_id=order_target(context.stock, 0)
				context.uptrend = False
				context.sellcounter = 0
                context.high_close_SIC = 0

	if context.uptrend == False:
		if data[context.stock].price>volatility:
			context.buycounter+=1
			if context.buycounter >= 7:
				print("BUYING STOCK","VSTOP:",volatility,"PRICE",data[context.stock].price)
				context.order_id=order_target(context.stock, 50)
				context.uptrend = True
				context.buycounter = 0
                context.low_close_SIC = 999999


def volatility_stop(context,data):  #measures volatility stop for 7 day period
	
	if len(context.last_5) < 5:
		return

	if context.calc_inital_trend:
		context.uptrend=(context.last_5[4]-context.last_5[0])>0
		context.calc_inital_trend=False

	# Below calculate the SIC 

	if context.uptrend:
		context.high_close_SIC=max(context.high_close_SIC,max(context.last_5))
	else:
		context.low_close_SIC=min(context.low_close_SIC,min(context.last_5))

	atr_data = atr(data) # initaliaze the data
	atr_value=atr_data[context.stock]
	atr_value*=2

	## returns tuple with boolean true for uptrend and the highclose or low close
	if context.uptrend:
		return context.high_close_SIC-atr_value
	return context.low_close_SIC+atr_value
