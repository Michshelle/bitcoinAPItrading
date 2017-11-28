##Bitfinex doc:https://bitfinex.readme.io/v2/docs/rest-auth

##Good way to understand REST

import requests  # pip install requests
import json
import base64
import hashlib
import hmac
import os
import time #for nonce

class BitfinexClient(object):
    BASE_URL = "https://api.bitfinex.com/"
    KEY=os.environ["BFX_KEY"]
    SECRET=os.environ["BFX_SECRET"]

    def _nonce(self):
        """
        Returns a nonce
        Used in authentication
        """
        return str(int(round(time.time() * 10000)))

    def _headers(self, path, nonce, body):
        signature = "/api/" + path + nonce + body
        h = hmac.new(self.SECRET, signature, hashlib.sha384)
        signature = h.hexdigest()
        return {
            "bfx-nonce": nonce,
            "bfx-apikey": self.KEY,
            "bfx-signature": signature,
            "content-type": "application/json"
        }

    def req(self, path, params = {}):
        nonce = self._nonce()
        body = params
        rawBody = json.dumps(body)
        headers = self._headers(path, nonce, rawBody)
        url = self.BASE_URL + path
        resp = requests.post(url, headers=headers, data=rawBody, verify=True)
        return resp
        
    def active_orders(self):
        """
        Fetch active orders
        """
        response = self.req("v2/auth/r/orders")
        if response.status_code == 200:
          return response.json()
        else:
          print response.status_code
          print response
          return ''

client = BitfinexClient()
print client.active_orders()