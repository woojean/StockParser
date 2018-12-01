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
收盘价1日止损
'''
def trace1(id,parseDay):
  print id,parseDay
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
  stopPrice = min(sp1,sp2)
  
  outPrice = 0 
  dayList = dayList[1:]
  holdDays = 0
  for day in dayList:
    holdDays +=1
    minPrice = parser.getMinPriceOfDay(res,day)
    endPrice = parser.getEndPriceOfDay(res,day)
    if endPrice == 0:
      outPrice = 0
      break
    if endPrice < stopPrice:
      outPrice = endPrice
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
持有N日
'''
def trace(id,parseDay):
  # N = 5 # 持股天数
  N = 20 # 持股天数
  print id,parseDay
  parser = RelativeParser.RelativeParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  
  dayList = parser.getNextTradingDayList(parseDay,N) # 
  inDay = dayList[0]
  # inPrice = parser.getStartPriceOfDay(res,inDay)  # 开盘价买入
  inPrice = parser.getMinPriceOfDay(res,inDay)  # 最低价买入
  if 0==inPrice:
    return False # 坏数据

  outDay = dayList[-1]
  outPrice = parser.getEndPriceOfDay(res,outDay)
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
  

