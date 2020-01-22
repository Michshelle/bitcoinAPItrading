import os
import sys
import asyncio
import time
sys.path.append('../')

from bfxapi import Client

API_KEY=os.getenv("BFX_KEY")
API_SECRET=os.getenv("BFX_SECRET")

bfx = Client(
  API_KEY=API_KEY,
  API_SECRET=API_SECRET,
  logLevel='DEBUG'
)

now = int(round(time.time() * 1000))
then = now - (1000 * 60 * 60 * 24 * 1) # 1 days ago



def get_two_float(f_str, n):
    f_str = str(f_str)      # f_str = '{}'.format(f_str) 也可以转换为字符串
    a, b, c = f_str.partition('.')
    c = (c+"0"*n)[:n]       # 如论传入的函数有几位小数，在字符串后面都添加n为小数0
    return ".".join([a, c])

async def log_historical_trades():
  trades = await bfx.rest.get_public_trades('fBTC', 0, then)
  #print ("Trades:")
  #[ print (t) for t in trades ]
  return trades

async def avail_balance():
   avails = await bfx.rest.avail_balance('fBTC', 1, 0,'FUNDING')
   return avails[0]

async def int_calc():
    list_int = []
    trades = await log_historical_trades()
    int_total_trades = len(trades)
    pick_trades = int_total_trades // 2
    for trade in trades:
        list_int.append(trade[3])
    list_int.sort(reverse=True)
    list_pick = list_int[:pick_trades]
    int_rate = sum(list_pick) / pick_trades
    return int_rate


async def create_funding(amo,raty):
  response = await bfx.rest.submit_funding_offer("fBTC", amo, raty, 2)
  # response is in the form of a Notification object
  # notify_info is in the form of a FundingOffer
  print ("Offer: ", response.notify_info)

async def cancel_funding():
  response = await bfx.rest.submit_cancel_funding_offer(41235958)
  # response is in the form of a Notification object
  # notify_info is in the form of a FundingOffer
  print ("Offer: ", response.notify_info)

async def run():
    k = 0.0
    avail = await avail_balance()
    if avail < 0:
        avail = avail * -1
    if avail >= 0.004:
        int_rate = await int_calc()
        #print(avail,"  ",int_rate)
        avail = float(get_two_float(avail,6))
        await create_funding(avail,int_rate)


  #await cancel_funding()

if __name__=="__main__":
    #t = asyncio.ensure_future(avail_balance())

    looping = asyncio.get_event_loop()
    fut = looping.create_task(run())
    looping.run_until_complete(fut)
    looping.close()
