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
import random

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser
from parsers import RelativeParser

def getEnterListFiles():
  enterListDirPath = Tools.getEnterListDirPath()
  enterListDirPath = '/Users/wujian/woojean/StockParser/config/db/向上跳空缺口-2017'
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
n日跟踪止损
'''
def trace(id,parseDay):
  print id,parseDay
  traceDays = 5  # n日跟踪止损
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,30) # 
  inDay = dayList[0]
  startPrice = parser.getStartPriceOfDay(res,inDay)
  endPrice = parser.getEndPriceOfDay(res,inDay)
  minPrice = parser.getMinPriceOfDay(res,inDay)
  maxPrice = parser.getMaxPriceOfDay(res,inDay)
  if 0==startPrice:
    return False # 坏数据

  # 剔除买入日一字板
  if parser.isOneLineUpwardLimit(res,inDay):
    print '剔除买入日一字板'
    return False
  
  inPrice = startPrice # 开盘价买

  # 剔除买入日阴线
  # if endPrice < startPrice:
  #   return False

  # inPrice = (maxPrice+minPrice)/2 # 阳线中间买入
  


  # 确定止损价
  pastDayList = parser.getPastTradingDayList(parseDay,traceDays)
  stopPrice = parser.getMinPriceOfDays(res,pastDayList)
  
  outPrice = 0 

  l = len(dayList)
  holdDays = 0
  for i in xrange(1,l):
    day = dayList[i]
    minPrice = parser.getMinPriceOfDay(res,day)
    holdDays +=1
    if minPrice == 0:
      outPrice = 0
      break
    if minPrice < stopPrice:  # 触发止损
      outDay = day
      outPrice = stopPrice
      break
    else:  # 未触发止损，上调止损价
      pastDayList = parser.getPastTradingDayList(day,traceDays)
      minPriceOfPastDays = parser.getMinPriceOfDays(res,pastDayList)
      stopPrice = minPriceOfPastDays
      
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
最大持股20日，止损，收盘价高于成本价止盈 ☆
'''
def traceWW(id,parseDay):
  print '最大持股20日，止损，收盘价高于成本价止盈'

  maxDays = 20 # 最长持股时间

  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,maxDays) # 
  inDay = dayList[0]
  print inDay
  maxPrice = parser.getMaxPriceOfDay(res,inDay)
  minPrice = parser.getMinPriceOfDay(res,inDay)
  startPrice = parser.getStartPriceOfDay(res,inDay)
  endPrice = parser.getEndPriceOfDay(res,inDay)
  # inPrice = parser.getMinPriceOfDay(res,inDay)  # 最低价买入
  if 0==startPrice:
    return False # 坏数据

  # 剔除买入日阴线
  # if endPrice < startPrice:
  #   return False

  # 剔除买入日阳线
  # if endPrice > startPrice:
  #   return False

  # 开盘价不等于最低价
  # if startPrice == minPrice:
  #   return False

  # 开盘价和最低价中间买
  # inPrice = (startPrice + minPrice)/2
  
  # 昨日收盘价买
  # dayList2 = parser.getPastTradingDayList(parseDay,2)
  # lastDay = dayList2[0]
  # endPriceOfLastDay = parser.getEndPriceOfDay(res,lastDay)
  # if minPrice > endPriceOfLastDay:  # 今日最低价在昨日收盘价之上，买不进
  #   return False
  # inPrice = endPriceOfLastDay

    
  # 买入价为K线中间
  # inPrice = (maxPrice+minPrice)/2

  # 开盘价买
  inPrice = startPrice

  # 最低价买
  # inPrice = minPrice

  # 收盘价买
  # inPrice = endPrice

  # 收盘价和上引线中间买
  # inPrice = (maxPrice+endPrice)/2

  # 确定止损价
  # sp1 = parser.getMinPriceOfDay(res,parseDay) 
  # sp2 = parser.getMinPriceOfDay(res,inDay) 
  # stopPrice = min(sp1,sp2)  # 信号日和买入日的最低价为止损价

  # 固定比例止损
  stopPrice = inPrice*0.9

  outPrice = 0 
  dayList = dayList[1:] # 从买入后第2天开始统计最高价、最低价
  holdDays = 1
  outDay = ''
  minP = 9999999
  maxP = 0
  for day in dayList:
    holdDays +=1
    maxPrice = parser.getMaxPriceOfDay(res,day)
    minPrice = parser.getMinPriceOfDay(res,day)
    startPrice = parser.getStartPriceOfDay(res,day)
    endPrice = parser.getEndPriceOfDay(res,day)
    
    if maxPrice == 0: # 坏数据
      return False
      break
    
    if minPrice < minP:
      minP = minPrice
    if maxPrice > maxP:
      maxP = maxPrice

    # 收盘价大于成本价止盈
    if endPrice >= inPrice:
      outPrice = endPrice # 收盘价卖
      outDay = day
      break
    
    # 开盘价大于成本价止盈
    # if startPrice >= inPrice:
    #   outPrice = startPrice # 收盘价卖
    #   outDay = day
    #   break
    
    # 止损：触价止损
    sp = parser.getMinPriceOfDay(res,day) 
    if sp < stopPrice:
      outPrice = stopPrice
      outDay = day
      break

  # 不考虑无结果的
  if outPrice == 0:
    return False

  # 以最后一天收盘价卖出
  # if outPrice == 0:
  #   outPrice = parser.getEndPriceOfDay(res,dayList[-1])  # 默认按到期后的收盘价为卖出价
  #   outDay = dayList[-1]
  #   if outPrice == 0:
  #     return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = holdDays
  ret['minPrice'] = minP
  ret['maxPrice'] = maxP
  return ret






'''
持有N日
'''
def traceN(id,parseDay):
  print '持有N日'
  N = 2 # 持股天数
  print id,parseDay
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  

  dayList = parser.getNextTradingDayList(parseDay,N) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 开盘价买入
  # inPrice = parser.getMinPriceOfDay(res,inDay)  # 最低价买入
  startPrice = parser.getStartPriceOfDay(res,inDay)
  endPrice = parser.getEndPriceOfDay(res,inDay)

  if 0==inPrice:
    return False # 坏数据

  # 剔除买入日阴线
  if endPrice < startPrice:
    return False

  outDay = dayList[-1]
  outPrice = parser.getEndPriceOfDay(res,outDay)  # 收盘价卖出
  # outPrice = parser.getMaxPriceOfDay(res,outDay) # 最高价卖出
  # outPrice = parser.getStartPriceOfDay(res,outDay) # 开盘价卖出
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
  


