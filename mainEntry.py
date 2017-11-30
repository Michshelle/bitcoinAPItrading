import logging,time,sys
import requests
from Acc import btfAccount

import hmac
import hashlib
import json
import base64


#create the authen header part of V1 document.
def getAuthHeader(loginName, loginPasswd, rawBody):
    body64str = str(base64.b64encode(rawBody.encode('utf-8')),'utf-8')
    tmpH = hmac.new(loginPasswd.encode(),body64str.encode(), hashlib.sha384)
    secSignature = tmpH.hexdigest()
    tmpHeader = {
        "X-BFX-APIKEY": loginName,
        "X-BFX-payload": body64str,
        "X-BFX-SIGNATURE": secSignature,
        'Content-Type':'application/json',
        'Accept':'application/json'
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


tmpBaseUrl = 'https://api.bitfinex.com'
tmpSrvName = ''
tmpParas = ''

#public info test: Get Ticket
tmpSrvName = '/v1/pubticker/btcusd'
tmpParas = ''
tmpResp = requests.get(tmpBaseUrl + tmpSrvName + tmpParas)
logging.debug(tmpResp.text)
tmpObj = tmpResp.json()
logging.debug(tmpObj)

#Authenticated information test: Wallets Balances
tmpSrvName = '/v1/balances'
tmpNonce = str(int(time.time() * 10000000))
jsonBody = {
    'request': tmpSrvName,
    'nonce': tmpNonce
}
rawBody = json.dumps(jsonBody)
tmpHeader = getAuthHeader(loginName, passName, rawBody)
tmpResp = requests.post(tmpBaseUrl+tmpSrvName, headers=tmpHeader, data=rawBody, verify=True)
logging.debug(tmpResp.text)
jsonObj = tmpResp.json()

