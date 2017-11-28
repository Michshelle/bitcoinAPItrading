import logging,time,sys
import requests
from Acc import btfAccount

import hmac
import hashlib
import json

def getAuthHeader(loginName, loginPasswd, srvPath, rawBody):
    tmpNonce = str(int(time.time() * 10000000))
    secSignature = "/api/" + srvPath + tmpNonce + rawBody
    tmpH = hmac.new(loginPasswd.encode(), secSignature.encode(), hashlib.sha384)
    secSignature = tmpH.hexdigest()
    tmpHeader = {
        "bfx-nonce": tmpNonce,
        "bfx-apikey": loginName,
        "bfx-signature": secSignature,
        "content-type": "application/json"
    }
    return tmpHeader


#logging
log = logging.getLogger(__name__)
fh = logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG) 
sh = logging.StreamHandler(sys.stdout)  
sh.setLevel(logging.DEBUG)  
log.addHandler(sh)
log.addHandler(fh)  
logging.basicConfig(level=logging.DEBUG, handlers=[fh, sh]) 

#username and password
secStr = btfAccount()
loginName = str(secStr['APIK'])
passName = str(secStr['APIS'])


#public info test: test the interface of get BitCoin-US Dollar bid information
tmpSrvName = 'ticker/tBTCUSD'
tmpParas = ''
tmpUrl = 'https://api.bitfinex.com/v2/%s/%s' % (tmpSrvName, tmpParas)
tmpResp = requests.get(tmpUrl)
logging.debug(tmpResp.text)
jsonObj = tmpResp.json()
tmpObj = {
    'BID': jsonObj[0],
    'BID_SIZE': jsonObj[1],
    'ASK': jsonObj[2],
    'ASK_SIZE': jsonObj[3],
    'DAILY_CHANGE': jsonObj[4],
    'DAILY_CHANGE_PERC': jsonObj[5],
    'LAST_PRICE': jsonObj[6],
    'VOLUME': jsonObj[7],
    'HIGH': jsonObj[8],
    'LOW': jsonObj[9]
}
logging.debug(tmpObj)

#Authenticated information test, include: wallet, order history
#Authenticated information need authenticate headers.
tmpParas = ''
tmpBaseUrl = 'https://api.bitfinex.com/'
tmpSrvPath = 'v2/auth/r/wallets'
jsonBody = {}
rawBody = json.dumps(jsonBody)
tmpHeader = getAuthHeader(loginName, passName, tmpSrvPath, rawBody)
tmpResp = requests.post(tmpBaseUrl+tmpSrvPath+tmpParas, headers=tmpHeader, data=rawBody, verify=True)
logging.debug(tmpResp.text)
jsonObj = tmpResp.json()
tmpObj = {
    'BTC': {
        'BALANCE':jsonObj[0][2],
        'UNSETTLED_INTEREST':jsonObj[0][3],
        'BALANCE_AVAILABLE':jsonObj[0][4]
    },
    'USD': {
        'BALANCE':jsonObj[1][2],
        'UNSETTLED_INTEREST':jsonObj[1][3],
        'BALANCE_AVAILABLE':jsonObj[1][4]
    }
}



tmpParas = '?start=600000&end=1000&limit=10'
tmpBaseUrl = 'https://api.bitfinex.com/'
tmpSrvPath = 'v2/auth/r/orders/tBTCUSD/hist'
jsonBody = {}
rawBody = json.dumps(jsonBody)
tmpHeader = getAuthHeader(loginName, passName, tmpSrvPath, rawBody)
tmpResp = requests.post(tmpBaseUrl+tmpSrvPath+tmpParas, headers=tmpHeader, data=rawBody, verify=True)
logging.debug(tmpResp.text)
jsonObj = tmpResp.json()

