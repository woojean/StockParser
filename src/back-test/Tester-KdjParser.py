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
from parsers import GeneralParser

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
1日止损
'''
def trace1(id,parseDay):
  print id,parseDay
  parser = GeneralParser.GeneralParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,20) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  if 0==inPrice:
    return False # 坏数据

  stopPrice = parser.getMinPriceOfDay(res,inDay) # 买入当天最低价做止损价
  outPrice = 0 
  dayList = dayList[1:]
  for day in dayList:
    minPrice = parser.getMinPriceOfDay(res,day)
    if minPrice == 0:
      outPrice = 0
      break
    if minPrice < stopPrice:  # 阴线
      outPrice = stopPrice
      break
    else:
      stopPrice = minPrice
      
  if outPrice == 0:
    return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outPrice'] = outPrice
  return ret




'''
2日止损
'''
def trace2(id,parseDay):
  print id,parseDay
  parser = GeneralParser.GeneralParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,50) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  if 0==inPrice:
    return False # 坏数据

  minPriceOfParseDay = parser.getMinPriceOfDay(res,parseDay)
  minPriceOfInDay = parser.getMinPriceOfDay(res,inDay)
  stopPrice = min(minPriceOfParseDay,minPriceOfInDay) # 买入当天最低价做止损价
  outPrice = 0 
  
  l = len(dayList)
  for i in xrange(1,l):
    day = dayList[i]
    minPrice = parser.getMinPriceOfDay(res,day)
    minPriceLastDay = parser.getMinPriceOfDay(res,dayList[i-1])
    if minPrice == 0:
      outPrice = 0
      break
    if minPrice < stopPrice:  # 触发止损
      outPrice = stopPrice
      break
    else:  # 未触发止损，上调止损价
      stopPrice = min(minPriceLastDay,minPrice)
      
  if outPrice == 0:
    return False


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outPrice'] = outPrice
  return ret



'''
持有10日
'''
def trace(id,parseDay):
  print id,parseDay
  parser = GeneralParser.GeneralParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,10) # 
  inDay = dayList[0]
  inPrice = parser.getStartPriceOfDay(res,inDay)  # 买入价为板后第一天的开盘价
  if 0==inPrice:
    return False # 坏数据

  outDay = dayList[-1]
  outPrice = parser.getEndPriceOfDay(res,outDay)
  if 0==outPrice:
    return False # 坏数据
  
  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outPrice'] = outPrice
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

  


