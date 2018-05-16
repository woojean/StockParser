#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-05-04
'''

import os
import re
import copy
import requests,time
import shutil
import sys
import threading
import time
import new
from operator import itemgetter 

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools



def getAllTradeDayList(new= False):
  path = Tools.getRootPath()+'/data/price/000001'
  
  if new or not os.path.exists(path):
   url = 'http://pdfm2.eastmoney.com/EM_UBG_PDTI_Fast/api/js?id=0000012&TYPE=k&js=fsDataTeacma((x))&rtntype=5&isCR=false&fsDataTeacma=fsDataTeacma'
   data = requests.get(url,verify=False).text
   open(path,'w').write(data)
  
  s = open(path,'r').read()
  idx = s.index('"data":[')
  s = s[idx:]
  allDayList = re.findall(r"(\d{4}-\d{1,2}-\d{1,2})", s)
  return allDayList


def getHoldDays(beginDay,endDay):
  allDayList = getAllTradeDayList()
  if not endDay in allDayList:
    allDayList = getAllTradeDayList(True)
  endIndex = allDayList.index(endDay)
  beginIndex = allDayList.index(beginDay)
  return endIndex - beginIndex



def dumpReport(recordList):
  s = '<html><head><meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
  s += '''
<style>
font-size:0.8em;

table {
  width:100%;
}

tr:hover{
  background-color:yellow;
  cursor:hand;
}

td{
  font-size:0.8em;
  text-align:center;
  padding:5px;
  border-bottom: thin dashed #ccc;
}

.table_header{
  font-weight:bold;
}

.table_header_counted{
  font-weight:bold;
  color:#009ACD;
}

.win{
  color:red;
}

.lose{
  color:#3CB371;
}

</style>
  '''
  s += '</head><body>'
  
  # 总体统计
  s += 'SUM_UP'
  


  # 流水
  s += '<table width="100%" cellspacing="0" cellpadding="0">'
  s += '<tr class="table_header">'
  s += '<td>序号</td>'
  s += '<td>买入日期</td>'
  s += '<td>代码</td>'
  s += '<td>名称</td>'
  s += '<td>买入价</td>'
  s += '<td>买入数量</td>'
  s += '<td>初始止损价</td>'
  s += '<td>卖出日期</td>'
  s += '<td>卖出价</td>'

  s += '<td class="table_header_counted">买入金额</td>'
  s += '<td class="table_header_counted">卖出金额</td>'
  s += '<td class="table_header_counted">持股天数</td>'
  s += '<td class="table_header_counted">盈亏金额</td>'
  s += '<td class="table_header_counted">盈亏比</td>'

  s += '<td>备注</td>'
  s += '</tr>'

  i = 1
  tradeNum = 0 # 成交记录数
  winNum = 0
  totalWin = 0.0 # 盈亏总额
  totalHoldDay = 0
  totalProfitAndLoss = 0.0
  for record in recordList:
    if len(record[0]) <1:
      continue
    tr = '<tr>'
    tr += '<td>'+str(i) +'</td>'
    i += 1
    tr += '<td>'+ str(record[0]) +'</td>'
    tr += '<td>'+ str(record[1]) +'</td>'
    tr += '<td>'+ str(record[2]) +'</td>'
    tr += '<td>'+ str(record[3]) +'</td>'
    tr += '<td>'+ str(record[4]) +'</td>'
    tr += '<td>'+ str(record[5]) +'</td>'
    tr += '<td>'+ str(record[6]) +'</td>'
    tr += '<td>'+ str(record[7]) +'</td>'
    
    # 买入金额
    buyAmount = record[3] * record[4]
    tr += '<td>'+ str(buyAmount) +'</td>'
    winAmount = 0
    if 0 != record[7]:  # 判断是否已卖出
      tradeNum += 1
      sellAmount = record[4] * record[7]
      holdDays = getHoldDays(record[0],record[6])
      totalHoldDay += holdDays
      profitAndLoss = round((sellAmount - buyAmount)/buyAmount,5)*100.0
      totalProfitAndLoss += profitAndLoss
      totalWin += (sellAmount - buyAmount)
      winAmount = sellAmount - buyAmount
    else:
      sellAmount = 0
      holdDays = 0
      profitAndLoss = 0

    # 卖出金额
    tr += '<td>'+ str(sellAmount) +'</td>'

    # 持股天数
    tr += '<td>'+ str(holdDays) +'</td>'

    # 盈亏金额
    if winAmount>0:
      tr += '<td class="win">'+ str(winAmount) +'</td>'
    else:
      tr += '<td class="lose">'+ str(winAmount) +'</td>'

    # 盈亏比
    if profitAndLoss>0:
      winNum +=1
      tr += '<td class="win">'+ str(profitAndLoss) +'%</td>'
    else:
      tr += '<td class="lose">'+ str(profitAndLoss) +'%</td>'

    tr += '<td>'+ str(record[8]) +'</td>'
    s += tr
  s += '</table>'

  today = time.strftime('%Y-%m-%d',time.localtime(time.time()))

  sumStr = '<table width="100%" cellspacing="0" cellpadding="0">'
  sumStr += '<tr class="table_header_counted">'
  sumStr += '<td>开始日期</td>'
  sumStr += '<td>结束日期</td>'
  sumStr += '<td>成交数</td>'
  sumStr += '<td>盈利数</td>'
  sumStr += '<td>亏损数</td>'
  sumStr += '<td>平均持股天数</td>'
  sumStr += '<td>胜率</td>'
  sumStr += '<td>盈亏总额</td>'
  sumStr += '<td>平均盈亏比例</td>'
  sumStr += '</tr>'

  sumStr += '<tr>'
  sumStr += '<td>'+recordList[0][0]+'</td>'
  sumStr += '<td>'+today+'</td>'
  sumStr += '<td>'+str(tradeNum)+'</td>'
  sumStr += '<td>'+str(winNum)+'</td>'
  sumStr += '<td>'+str(tradeNum - winNum)+'</td>'
  sumStr += '<td>'+str(round(totalHoldDay/tradeNum,3))+'</td>'

  winRate = 100.0*round(winNum*1.0/tradeNum,5)
  if winRate > 0:
    sumStr += '<td class="win">'+str(winRate)+'%</td>'
  else:
    sumStr += '<td class="lose">'+str(winRate)+'%</td>'

  if totalWin > 0:
    sumStr += '<td class="win">'+str(totalWin)+'</td>'
  else:
    sumStr += '<td class="lose">'+str(totalWin)+'</td>'

  avgProfitAndLoss = round(totalProfitAndLoss/tradeNum,3)
  if avgProfitAndLoss > 0:
    sumStr += '<td class="win">'+str(avgProfitAndLoss)+'%</td>'
  else:
    sumStr += '<td class="lose">'+str(avgProfitAndLoss)+'%</td>'

  
  sumStr += '</tr>'
  sumStr += '</table>'
  sumStr += '</br></br>'

  s = s.replace('SUM_UP',sumStr)

  path = Tools.getRootPath()+'/db/db-trade-history/Trade-History-'+today+'.html'
  open(path,'w').write(s)
  os.system('open '+path)



def getAllTradeRecords():
  recordList = []
  for root,dirs,files in os.walk(TRADE_RECORD_PATH):
    for f in files:
      try:
         path = root + '/' + f
         s = open(path,'r').read()
         s = s.replace(' ','')
         records = eval(s)
         recordList = recordList + records
      except Exception, e:
        pass
        #print repr(e)
  return recordList


# ============================================================================================

TRADE_RECORD_PATH = '/Users/wujian/woojean/ThinkingInTrade/Data/Trades'

if __name__ == '__main__':
  recordList = getAllTradeRecords()
  dumpReport(recordList)


