#coding:utf-8
#!/usr/bin/env python
'''
woojean@2018-01-08
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
import random

reload(sys)
sys.setdefaultencoding('utf-8')

rootPath = sys.path[0][0:sys.path[0].index('StockParser')]+'/StockParser'
sys.path.append(rootPath+'/src') 
from common import Tools
from parsers import BaseParser


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
        print repr(e)
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
      #print repr(e)
      pass
  return ret


def getMinPriceOfDays(id,dayList):
  parser = BaseParser.BaseParser(dayList[-1])
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()

  minPrice = 999999
  for d in dayList:
    price = parser.getMinPriceOfDay(res,d)
    if price < minPrice: 
      minPrice = price
  return minPrice




def trace(id,day):
  parser = BaseParser.BaseParser(day)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()

  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['day'] = day
  ret['inPrice'] = parser.getEndPriceOfDay(res,day) # 买入价为当日收盘价
  ret['islp'] = parser.getMinPriceOfDay(res,day) # 初始止损价为买入当日最低价
  ret['risk'] = round(ret['islp'] - ret['inPrice'],5)
  ret['riskRate'] = round(ret['risk']/ret['inPrice'],5)
  #if ret['riskRate'] < -0.03:  
  #if ret['riskRate'] < -0.1: 
  if ret['riskRate'] < -0.04: # 初始止损不超过n%（平均持股时间才4天） <-----------------
    return  False

  dayList = parser.getNextTradingDayList(day,30)
  inDayMaxPrice = parser.getMaxPriceOfDay(res,day)
  inDayMinPrice = parser.getMinPriceOfDay(res,day)
  holdDays = 0
  inTracking = False
  #slp = round(ret['islp'],1)-0.1 # 去尾
  slp = ret['islp']
  for d in dayList: # 从第2天开始
    holdDays += 1
    endPrice = parser.getEndPriceOfDay(res,d)
    minPrice = parser.getMinPriceOfDay(res,d)

    if minPrice < slp: # 触发止损  要有大盘配合
      ret['outPrice'] = slp
      break
    
    if not inTracking: # 处于启动期
      if minPrice > inDayMaxPrice:  # 进入跟踪止损的信号<-----------------
      #if minPrice > ret['inPrice']:
      #if minPrice > inDayMinPrice:
        inTracking = True
        #slp = round(minPrice,1)-0.1 # 上调止损价
        #slp = ret['inPrice'] 
        slp = minPrice
    else: # 处于跟踪期
      dayList = parser.getPastTradingDayList(d,1)  # n日止损 <-----------------
      newIntervalMinPrice = getMinPriceOfDays(id,dayList)
      if newIntervalMinPrice > slp:
        #slp = round(newIntervalMinPrice,1)-0.1
        slp = newIntervalMinPrice


  ret['holdDays'] = holdDays
  ret['profit'] = round(ret['outPrice'] - ret['inPrice'],5)
  ret['profitRate'] =str(round(ret['profit']/ret['inPrice'],5)*100.0)+'%'
  ret['growthRate'] =round(ret['profit']/ret['inPrice'],5)
  
  return ret



if __name__ == '__main__':
  # 跟踪所有中选股
  enterListFileList = getEnterListFiles()
  #print enterListFileList

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







