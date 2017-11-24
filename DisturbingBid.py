import logging,time,sys  
from btfxwss import BtfxWss
from Acc import btfAccount  
      
def replace_value_with_definition(current_dict,key_to_find, definition):
    for key in current_dict.keys():
        if key == key_to_find:
            current_dict[key] = definition
            break
    return current_dict

secStr = btfAccount()

loginName = str(secStr['APIK'])
passName = str(secStr['APIS'])
  
wss = BtfxWss(key=loginName,secret=passName)  
wss.start()  
    
while not wss.conn.connected.is_set():  
    time.sleep(1)  
wss.authenticate()  #Success
##############################################################################
# Subscribe to some channels
wss.subscribe_to_ticker('BTCUSD')
wss.subscribe_to_order_book('BTCUSD')
wss.subscribe_to_trades('BTCUSD')

time.sleep(5)
#Accessing data stored in BtfxWss:
ticker_q=wss.tickers('BTCUSD')
while not ticker_q.empty():
    print(ticker_q.get()[0][0][0])
    break

##################################################################################

curOrder = wss.orders.get()
nbOrders = len(curOrder[0][1]) #number of orders

pricy ="8399"  #Must be string

if nbOrders != 0: #Cancel all orders
	for item in curOrder[0][1]:
		wss.cancel_order(id=item[0])
#######################################################################
Morder = {        
    "type": "EXCHANGE LIMIT",
    "symbol": "tBTCUSD",
    "amount": "-0.007",
    "price": "",
    "hidden": 0
}

Zorder=replace_value_with_definition(Morder,'price', pricy)

time.sleep(5) #First make sure to cancel

wss.new_order(**Zorder)	
print(wss.orders_new.get())
########################################################################
# Unsubscribing from channels:
wss.unsubscribe_from_ticker('BTCUSD')
wss.unsubscribe_from_order_book('BTCUSD')
wss.unsubscribe_from_trades('BTCUSD')

wss.stop()

