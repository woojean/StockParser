#coding:utf-8
#!/usr/bin/env python
import os
import re
import requests,time
import shutil
import sys
import threading
import time
import datetime

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser
from parsers import RelativeParser

def getEnterListFiles():
  enterListDirPath = Tools.getEnterListDirPath()
  enterListFileList = []
  for root,dirs,files in os.walk(enterListDirPath):
    for f in files:
      if f =='.DS_Store':
        continue
      try:
        path = root + '/' + f
        enterListFileList.append(path)
      except Exception, e:
        pass
        # print repr(e)
  return enterListFileList


def printProcess(current,total):
  lastRate = round((current-1)*100.0/total,0)
  currentRate = round(current*100.0/total,0)
  if lastRate != currentRate:
    rate = str(int(currentRate)) 
    rate = rate.rjust(3,' ')
    s = ''
    s = s.rjust(int(currentRate),'.')
    s += ' -> '
    s = s.ljust(104,' ')
    s += rate + ' %'
    print s


def traceEnterList(f):
  ret = {}
  parser = f.split('/')[-1][11:-4]
  parseDay = f.split('/')[-1][:10]
  idList = open(f,'r').read().split(',')
  #idList = idList[:2]
  #if len(idList) > 2:
  #  idList = random.sample(idList, 2)
  ret['parser'] = parser
  ret['parseDay'] = parseDay
  ret['idList'] = []

  for id in idList:
    try:
      r = trace(id,parseDay)
      if False == r:
        continue
      ret['idList'].append(r)
    except Exception, e:
      print repr(e)
      pass
  return ret


'''
1日最低价跟踪止损，收盘价卖出
'''
def trace11(id,parseDay):
  print '1日最低价跟踪止损，收盘价卖出'
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,20) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  # inPrice = parser.getMinPriceOfDay(res,inDay)  # 
  if 0==inPrice:
    return False # 坏数据

  # 确定止损价
  sp1 = parser.getMinPriceOfDay(res,parseDay) 
  sp2 = parser.getMinPriceOfDay(res,inDay) 
  stopPrice = min(sp1,sp2) # 初始止损价为信号日、买入日两天的最低价
  
  outPrice = 0 
  dayList = dayList[1:]  # 从买入后第2天开始遍历
  holdDays = 1
  for day in dayList:
    holdDays +=1
    minPrice = parser.getMinPriceOfDay(res,day)
    endPrice = parser.getEndPriceOfDay(res,day)
    if endPrice == 0:
      return False
    if endPrice < stopPrice:  # 收盘价跌破止损价，收盘价卖出
      outPrice = endPrice
      outDay = day
      break
    else:
      stopPrice = minPrice  # 上调止损价
      
  if outPrice == 0: # 数据错误
    outPrice = parser.getEndPriceOfDay(res,dayList[-1])  # 默认按到期后的收盘价为卖出价
    outDay = dayList[-1]
    if outPrice == 0:
      return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
  return ret




'''
1日最低价跟踪止损，止损价卖出
'''
def trace1(id,parseDay):
  print '1日最低价跟踪止损，止损价卖出'
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,20) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  # inPrice = parser.getMinPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  if 0==inPrice:
    return False # 坏数据

  # 确定止损价
  sp1 = parser.getMinPriceOfDay(res,parseDay) 
  sp2 = parser.getMinPriceOfDay(res,inDay) 
  stopPrice = min(sp1,sp2)
  
  outPrice = 0 
  dayList = dayList[1:]
  holdDays = 1
  for day in dayList:
    holdDays +=1
    minPrice = parser.getMinPriceOfDay(res,day)
    if minPrice == 0:
      return False
    if minPrice < stopPrice:  # 最低价低于止损价
      outPrice = stopPrice
      outDay = day
      break
    else:
      stopPrice = minPrice
      
  if outPrice == 0:
    return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
  return ret



'''
最大持股20日，n%止盈，止损
'''
def traceZY(id,parseDay):
  print '最大持股20日，n%止盈，止损'

  maxDays = 20 # 最长持股时间
  rate = 0.01 # 止盈利润比例

  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,maxDays) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为信号日后一天的开盘价
  # inPrice = parser.getMinPriceOfDay(res,inDay) 
  if 0==inPrice:
    return False # 坏数据

  # 确定止损价
  sp1 = parser.getMinPriceOfDay(res,parseDay) 
  sp2 = parser.getMinPriceOfDay(res,inDay) 
  stopPrice = min(sp1,sp2)

  # 确定止盈价
  targetPrice = inPrice*(1+rate)

  outPrice = 0 
  dayList = dayList[1:]
  holdDays = 1
  outDay = ''
  for day in dayList:
    holdDays +=1
    maxPrice = parser.getMaxPriceOfDay(res,day)
    if maxPrice == 0: # 坏数据
      return False
      break

    # 止盈
    if maxPrice >= targetPrice:
      outPrice = targetPrice
      outDay = day
      break
    
    # 止损
    # sp = parser.getMinPriceOfDay(res,day) 
    # if sp < stopPrice:
    #   outPrice = stopPrice
    #   outDay = day
    #   break
      
  if outPrice == 0:
    outPrice = parser.getEndPriceOfDay(res,dayList[-1])  # 默认按到期后的收盘价为卖出价
    outDay = dayList[-1]
    if outPrice == 0:
      return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
  return ret



'''
限制时间，止损、开盘价止盈
'''
def tracekp(id,parseDay):
  print '限制时间，止损、开盘价止盈'

  maxDays = 20 # 最长持股时间
  rate = 0.01 # 止盈利润比例

  # 取参数
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  dayList = parser.getNextTradingDayList(parseDay,maxDays) # 

  # 确定入场日
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为信号日后一天的开盘价
  if 0==inPrice:
    return False # 坏数据

  # 确定初始止损价
  sp1 = parser.getMinPriceOfDay(res,parseDay) 
  sp2 = parser.getMinPriceOfDay(res,inDay) 
  stopPrice = min(sp1,sp2)

  # 确定止盈价
  targetPrice = inPrice*(1+rate)

  outPrice = 0 
  dayList = dayList[1:] # 从买入后一天开始
  holdDays = 1
  outDay = ''
  for day in dayList:
    holdDays +=1
    startPrice = parser.getStartPriceOfDay(res,day)
    if startPrice == 0: # 坏数据
      return False

    # 止盈
    if startPrice >= targetPrice:  # 开盘价超过止盈价
      outPrice = startPrice  # 开盘价大于止盈价格，则卖出
      outDay = day
      break
    
    # 止损
    # sp = parser.getMinPriceOfDay(res,day) 
    # if sp < stopPrice:
    #   outPrice = stopPrice
    #   outDay = day
    #   break
      
  if outPrice == 0:
    outPrice = parser.getEndPriceOfDay(res,dayList[-1])  # 默认按到期后的收盘价为卖出价
    outDay = dayList[-1]
    if outPrice == 0:
      return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
  return ret


'''
限制时间，按比例止损、止盈
'''
def traceBI(id,parseDay):
  print '限制时间，按比例止损、止盈'

  maxDays = 20 # 最长持股时间

  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  minPrice = parser.getMinPriceOfDay(res,parseDay)

  dayList = parser.getNextTradingDayList(parseDay,maxDays) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为信号日后一天的开盘价
  if 0==inPrice:
    return False # 坏数据



  # 确定止损价
  sp1 = parser.getMinPriceOfDay(res,parseDay) 
  sp2 = parser.getMinPriceOfDay(res,inDay) 
  stopPrice = min(sp1,sp2)

  # 止盈利润比例
  rate = (inPrice - stopPrice)/stopPrice 
  rate = 5* rate  # 止盈是止损的N倍

  # 确定止盈价
  targetPrice = inPrice*(1+rate)

  outPrice = 0 
  dayList = dayList[1:]
  holdDays = 1
  outDay = ''
  for day in dayList:
    holdDays +=1
    maxPrice = parser.getMaxPriceOfDay(res,day)
    if maxPrice == 0: # 坏数据
      return False

    # 止盈
    if maxPrice >= targetPrice:
      outPrice = targetPrice
      outDay = day
      break
    
    # 止损
    sp = parser.getMinPriceOfDay(res,day) 
    if sp < stopPrice:
      outPrice = stopPrice
      outDay = day
      break
      
  if outPrice == 0:
    outPrice = parser.getEndPriceOfDay(res,dayList[-1])  # 默认按到期后的收盘价为卖出价
    outDay = dayList[-1]
    if outPrice == 0:
      return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
  return ret



'''
持有N日
'''
def trace(id,parseDay):
  print '持有N日'
  N = 2 # 持股天数
  # N = 20 # 持股天数
  print id,parseDay
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,N) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 开盘价买入
  # inPrice = parser.getMinPriceOfDay(res,inDay)  # 最低价买入
  if 0==inPrice:
    return False # 坏数据

  outDay = dayList[-1]
  outPrice = parser.getEndPriceOfDay(res,outDay)  # 收盘价卖出
  # outPrice = parser.getMaxPriceOfDay(res,outDay) # 最高价卖出
  if 0==outPrice:
    return False # 坏数据

  minPrice = 999999
  maxPrice = 0  
  dayList = dayList[1:]  # 从买入后第2天开始统计最高价、最低价
  for day in dayList:
    maxP = parser.getMaxPriceOfDay(res,day)
    minP = parser.getMinPriceOfDay(res,day)
    if maxP > maxPrice:
      maxPrice = maxP
    if minP < minPrice:
      minPrice = minP

  # 无2%的盈利机会
  # r = maxPrice/inPrice
  # if r >1.02:
  #   return False

  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = N
  ret['minPrice'] = minPrice
  ret['maxPrice'] = maxPrice
  return ret






if __name__ == '__main__':
  # 跟踪所有中选股
  enterListFileList = getEnterListFiles()
  ret = []
  
  parsedNum = 0
  total = len(enterListFileList)
  for f in enterListFileList:
    printProcess(parsedNum,total)
    r = traceEnterList(f)
    ret.append(r)
    parsedNum += 1
  
  path = Tools.getTracerDirPath()+'/trace_report.data'
  open(path,'w').write(str(ret))
  
  cmd = 'python '+ rootPath + '/src/back-test/Reporter-RelativeParser.py'
  print cmd
  os.system(cmd)
  


