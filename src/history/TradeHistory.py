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

'''
[["2018-05-03","600703","三安光电",20.89,600,20.32,"2018-05-03",21.36,
  "BK","2018年五一节后开始记录每一笔交易"],
["2018-05-04","600645","中源协和",21.85,500,21.15,"2018-05-10",22.85,"BK",""],
["2018-05-09","603776","永安行",58.49,200,57.14,"2018-05-14",57.29,"BK",""],
["2018-05-10","002038","双鹭药业",46.15,300,44.85,"2018-05-11",44.85,"BK",""],
["2018-05-10","600645","中源协和",23.21,500,22.75,"2018-05-14",21.74,
  "BK","顶部上吊线进场；尾盘长上影线阴线触及止损价即反弹，未走，第二天大幅向下跳空低开"],
["2018-05-15","600718","东软集团",14.7,800,14.25,"2018-05-18",14.27,"BK",""],
["2018-05-16","002019","亿帆医药",20.54,500,20.0,"2018-05-18",19.99,"BK",""],
["2018-05-18","000505","京粮控股",7.88,1300,7.8,"2018-05-21",7.89,"BK",""],
["2018-05-18","600419","天润乳业",48.16,300,47.32,"2018-05-21",48.43,"BK",""],
["2018-05-18","000525","红太阳",20.47,500,20.12,"2018-05-21",20.4,"BK",""],
["2018-05-21","002923","润都股份",44.8,300,43.81,"",0,"DK",""],
["2018-05-21","000565","渝三峡A",6.18,1700,6.03,"2018-05-24",6.25,"DK","操作失误：买入价偏高"],
["2018-05-21","601002","晋亿实业",7.84,1300,7.65,"",0,"DK",""],
["2018-05-21","300391","康跃科技",12.77,800,12.53,"",0,"DK",""],
["2018-05-22","002172","澳洋科技",6.902,500,0,"2018-05-23",6.19,"TL",""],
["2018-05-22","002930","宏川智慧",60.79,100,0,"2018-05-23",59.5,"TL",""],
["2018-05-22","300084","海默科技",7.367,300,0,"2018-05-23",7.02,"TL",""],
["2018-05-22","300135","宝利国际",3.821,700,0,"2018-05-23",3.34,"TL",""],
["2018-05-22","300471","厚普股份",9.515,200,0,"2018-05-23",9.9,"TL",""],
["2018-05-22","300644","南京聚隆",64.95,100,0,"2018-05-23",70.5,"TL",""],
["2018-05-23","300666","江丰电子",67.13,200,64.4,"2018-05-25",64.02,"DK","前有三根大阴棒；即将到达阻力趋势线入场"],
["2018-05-23","002299","圣农发展",16.32,700,15.63,"2018-05-24",15.63,"DK","日K回撤，周K镊形顶入场；止损卖不掉，换手率太低；"],
["2018-05-24","601619","嘉泽新能",11.2,100,0,"2018-05-25",11.49,"TL",""],
["2018-05-24","000760","斯太尔",5.18,100,0,"2018-05-25",4.9,"TL",""],
["2018-05-24","002184","海得控制",15,800,14.7,"",0,"DK","即将到达阻力趋势线入场"],
["2018-05-25","000890","法尔胜",6.7,2000,6.63,"",0,"KDJ",""],
["2018-05-25","002237","恒邦股份",11.19,1000,11.84,"",0,"KDJ","操作失误：买入价偏高"],
["","","",0,0,0,"",0,"",""]
]
'''

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



def dumpReport(recordList,isHide = False):
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
  font-weight:lighter;
  color:red;
}

.lose{
  font-weight:lighter;
  color:#00CD00;
}

.hide{
  color:#aaa;
}

.summaryAll{
  font-weight:bolder;
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
  s += '<td>策略</td>'
  s += '<td>备注</td>'
  s += '</tr>'

  i = len(recordList)
  tradeNum = 0 # 成交记录数
  winNum = 0
  totalEarn = 0.0 # 盈亏总额
  totalHoldDay = 0
  totalProfitAndLoss = 0.0
  for record in recordList:
    if len(record[0]) <1:
      continue
    tr = '<tr>'
    tr += '<td>'+str(i) +'</td>'
    i -= 1
    tr += '<td>'+ str(record[0]) +'</td>'
    tr += '<td>'+ str(record[1]) +'</td>'
    tr += '<td>'+ str(record[2]) +'</td>'
    tr += '<td>'+ str(record[3]) +'</td>'

    if isHide:
      tr += '<td class="hide">隐藏</td>'
    else:
      tr += '<td>'+ str(record[4]) +'</td>'

    tr += '<td>'+ str(record[5]) +'</td>'

    endDate = str(record[6])
    if len(endDate) < 1:
      tr += '<td>持仓中</td>'
    else:
      tr += '<td>'+ str(record[6]) +'</td>'
    tr += '<td>'+ str(record[7]) +'</td>'
    
    # 买入金额
    buyAmount = record[3] * record[4]
    if isHide:
      tr += '<td class="hide">隐藏</td>'
    else:
      tr += '<td>'+ str(buyAmount) +'</td>'
    winAmount = 0
    if 0 != record[7]:  # 判断是否已卖出
      tradeNum += 1
      sellAmount = record[4] * record[7]
      holdDays = getHoldDays(record[0],record[6])
      totalHoldDay += holdDays
      profitAndLoss = round((sellAmount - buyAmount)/buyAmount,5)*100.0
      totalProfitAndLoss += profitAndLoss
      totalEarn += (sellAmount - buyAmount)
      winAmount = sellAmount - buyAmount
    else:
      sellAmount = 0
      holdDays = 0
      profitAndLoss = 0

    # 卖出金额
    if isHide:
      tr += '<td class="hide">隐藏</td>'
    else:
      tr += '<td>'+ str(sellAmount) +'</td>'

    # 持股天数
    tr += '<td>'+ str(holdDays) +'</td>'

    # 盈亏金额
    if isHide:
      tr += '<td class="hide">隐藏</td>'
    elif winAmount>0:
      tr += '<td class="win">'+ str(winAmount) +'</td>'
    else:
      tr += '<td class="lose">'+ str(winAmount) +'</td>'

    # 盈亏比
    if profitAndLoss>0:
      winNum +=1
      tr += '<td class="win">'+ str(profitAndLoss) +'%</td>'
    else:
      tr += '<td class="lose">'+ str(profitAndLoss) +'%</td>'

    # 策略
    tr += '<td><font color="orange">'+ str(record[8]) +'</font></td>'

    # 备注
    tr += '<td><font color="orange">'+ str(record[9]) +'</font></td>'
    s += tr
  s += '</table>'



  # 汇总统计
  sumStr = '<table width="100%" cellspacing="0" cellpadding="0">'
  sumStr += '<tr class="table_header_counted">'
  sumStr += '<td>策略</td>'
  sumStr += '<td>开始日期</td>'
  sumStr += '<td>结束日期</td>'
  sumStr += '<td>总交易数</td>'
  sumStr += '<td>盈利交易数</td>'
  sumStr += '<td>亏损交易数</td>'
  sumStr += '<td>胜率</td>'
  sumStr += '<td>平均持股天数</td>'
  sumStr += '<td>单笔交易平均盈亏</td>'
  sumStr += '<td>盈亏总金额</td>'
  sumStr += '</tr>'

  summaryData = getSummaryData(recordList)
  for strategies,data in summaryData.items():
    if not data:
      continue
    if 'ALL' == strategies:
      sumStr += '<tr class = "summaryAll">'
    else:
      sumStr += '<tr>'
    sumStr += '<td>'+strategies+'</td>'
    sumStr += '<td>'+str(data['startDate'])+'</td>'
    sumStr += '<td>'+str(data['endDate'])+'</td>'
    sumStr += '<td>'+str(data['tradeNum'])+'</td>'
    sumStr += '<td>'+str(data['winNum'])+'</td>'
    sumStr += '<td>'+str(data['loseNum'])+'</td>'

    # 胜率
    winRate = data['winRate']
    if winRate > 50:
      sumStr += '<td class="win">'+str(winRate)+'%</td>'
    else:
      sumStr += '<td class="lose">'+str(winRate)+'%</td>'

    sumStr += '<td>'+str(data['avgHoldDay'])+'</td>'

    # 单笔交易平均盈利
    avgProfitAndLoss = data['avgProfitAndLoss']
    if avgProfitAndLoss > 0:
      sumStr += '<td class="win">'+str(avgProfitAndLoss)+'%</td>'
    else:
      sumStr += '<td class="lose">'+str(avgProfitAndLoss)+'%</td>'

    # 总盈亏
    totalEarn = data['totalEarn']
    if isHide:
      sumStr += '<td class="hide">隐藏</td>'
    elif totalEarn > 0:
      sumStr += '<td class="win">'+str(totalEarn)+'</td>'
    else:
      sumStr += '<td class="lose">'+str(totalEarn)+'</td>'

    sumStr += '</tr>'
  sumStr += '</table>'
  sumStr += '</br></br>'

  s = s.replace('SUM_UP',sumStr)

  today = time.strftime('%Y-%m-%d',time.localtime(time.time()))
  path = Tools.getRootPath()+'/db/db-trade-history/Trade-History-'+today+'.html'
  open(path,'w').write(s)
  os.system('open '+path)


def filterRecordsByStrategies(recordList,strategies):
  if not strategies:
    return recordList

  filteredList = []
  for record in recordList:
    if strategies == record[8]:
      filteredList.append(record)
  return filteredList


def getAllTradeRecords(strategies = False):
  recordList = []
  for root,dirs,files in os.walk(TRADE_RECORD_PATH):
    for f in files:
      try:
          if '.DS_Store' == f:
            continue
          path = root + '/' + f
          s = open(path,'r').read()
          s = s.replace(' ','')
          records = eval(s)
          records = filterRecordsByStrategies(records,strategies)
          recordList = recordList + records
      except Exception, e:
        pass
        print repr(e)

  # 删除非法元素
  for record in recordList:
    if len(record[0]) <1:
      recordList.remove(record)

  recordList.reverse()
  return recordList


def getSummaryDataOfStrategies(strategies):
  ret = {}
  tradeNum = 0 # 成交记录数
  winNum = 0
  totalEarn = 0.0 # 盈亏总额
  totalHoldDay = 0
  totalProfitAndLoss = 0.0
  for record in recordList:
    if len(record[0]) <1:
      continue

    if (strategies != record[8]) and ('ALL' != strategies):
      continue

    # 买入金额
    buyAmount = record[3] * record[4]
    winAmount = 0
    if 0 != record[7]:  # 判断是否已卖出
      tradeNum += 1
      sellAmount = record[4] * record[7]
      holdDays = getHoldDays(record[0],record[6])
      totalHoldDay += holdDays
      profitAndLoss = round((sellAmount - buyAmount)/buyAmount,5)*100.0
      totalProfitAndLoss += profitAndLoss
      totalEarn += (sellAmount - buyAmount)
      winAmount = sellAmount - buyAmount
    else:
      sellAmount = 0
      holdDays = 0
      profitAndLoss = 0

    if profitAndLoss>0:
      winNum +=1
  
  if 0 == tradeNum:  # 尚无已完成的交易
    return ret

  ret['startDate'] = recordList[-1][0]
  ret['endDate'] = recordList[0][0]
  ret['tradeNum'] = tradeNum
  ret['winNum'] = winNum
  ret['loseNum'] = tradeNum - winNum
  ret['winRate'] = 100.0*round(winNum*1.0/tradeNum,5)
  ret['avgHoldDay'] = round(totalHoldDay*1.0/tradeNum,3)
  ret['avgProfitAndLoss'] = round(totalProfitAndLoss/tradeNum,3)
  ret['totalEarn'] = totalEarn
  
  return ret
  



def getSummaryData(recordList):
  ret = {
    'ALL':{}
  }

  # 统计有哪些strategies
  for record in recordList:
    if len(record[0]) <1:
      continue
    strategies = str(record[8])
    if not ret.has_key(strategies):
      ret[strategies] = {}
  
  # 统计各个strategies的数据
  for k,v in ret.items():
    ret[k] = getSummaryDataOfStrategies(k)
  return ret


# ============================================================================================

TRADE_RECORD_PATH = '/Users/wujian/woojean/ThinkingInTrade/Trading-Records'

if __name__ == '__main__':
  isHide = False if (len(sys.argv) <= 1) else ('hide' == sys.argv[1])
  strategies = False if (len(sys.argv) <= 2) else (sys.argv[2])

  recordList = getAllTradeRecords(strategies)
  dumpReport(recordList,isHide)
  
  #ret =  getSummaryData(recordList)
  #print ret








