import logging,time,sys  
from btfxwss import BtfxWss
from Acc import btfAccount  
      
log = logging.getLogger(__name__)  
  
fh = logging.FileHandler('test.log')  
fh.setLevel(logging.DEBUG)  
sh = logging.StreamHandler(sys.stdout)  
sh.setLevel(logging.DEBUG)  
  
log.addHandler(sh)  
log.addHandler(fh)  
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh]) 

secStr = btfAccount()

loginName = str(secStr['APIK'])
passName = str(secStr['APIS'])
  
wss = BtfxWss(key=loginName,secret=passName)  
wss.start()  
while not wss.conn.connected.is_set():  
    time.sleep(1)  
wss.authenticate()  #Success
###########################################################
myAcc = wss.wallets.get()  

BTCw = myAcc[0][1][0][2]
USDw = myAcc[0][1][1][2]
print("Bitcoin bal is" ,BTCw)
print("USD bal is" ,USDw)  
##################################################################
# Subscribe to some channels
wss.subscribe_to_ticker('BTCUSD')
wss.subscribe_to_order_book('BTCUSD')

time.sleep(10)
#Accessing data stored in BtfxWss:
ticker_q=wss.tickers('BTCUSD')
while not ticker_q.empty():
    print(ticker_q.get())

#######################################
Morder = {           
"type": "EXCHANGE LIMIT",
"symbol": "tBTCUSD",
"amount": "0.01",
"price": "531",
"hidden": 0
}
wss.new_order(**Morder)
time.sleep(10)
print(wss.orders_new.get())
#######################################
# Unsubscribing from channels:
wss.unsubscribe_from_ticker('BTCUSD')
wss.unsubscribe_from_order_book('BTCUSD')



wss.stop()


