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
      try:
        path = root + '/' + f
        enterListFileList.append(path)
      except Exception, e:
        pass
        print repr(e)
  return enterListFileList


def traceEnterList(f):
  ret = {}
  parser = f.split('/')[-1][11:-4]
  parseDay = f.split('/')[-1][:10]
  idList = open(f,'r').read().split(',')
  ret['parser'] = parser
  ret['parseDay'] = parseDay
  ret['idList'] = []
  for id in idList:
    try:
      r = trace(id,parseDay)
      ret['idList'].append(r)
    except Exception, e:
      pass
  return ret


def trace(id,day):
  parser = BaseParser.BaseParser(day)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()

  ret = {}
  ret['id'] = id
  ret['day'] = day
  ret['inPrice'] = parser.getEndPriceOfDay(res,day) # 买入价为当日收盘价
  ret['islp'] = parser.getMinPriceOfDay(res,day) # 初始止损价为买入当日最低价
  ret['risk'] = round(ret['inPrice'] - ret['islp'],3)
  ret['riskRate'] = round(ret['risk']/ret['inPrice'],3)

  dayList = parser.getNextTradingDayList(day,30)
  holdDays = 0
  slp = ret['islp']
  for d in dayList: # 从第2天开始
    holdDays += 1
    endPrice = parser.getEndPriceOfDay(res,d)
    minPrice = parser.getMinPriceOfDay(res,d)
    if minPrice < slp: # 触发止损
      ret['outPrice'] = slp
      break
    elif minPrice > ret['inPrice']: # 当日最低价已经超过成本价
      slp = minPrice # 上调止损价

  ret['holdDays'] = holdDays
  ret['profit'] = round(ret['outPrice'] - ret['inPrice'],3)
  ret['profitRate'] =str(round(ret['profit']/ret['inPrice'],3)*100.0)+'%'
  ret['growthRate'] =round(ret['profit']/ret['inPrice'],3)
  ret['PR'] = round(ret['profit']/ret['risk'],3)
  
  return ret



if __name__ == '__main__':
  # 跟踪所有中选股
  enterListFileList = getEnterListFiles()
  #print enterListFileList

  ret = []
  

  for f in enterListFileList:
    r = traceEnterList(f)
    ret.append(r)
  
  print ret
  path = Tools.getTracerDirPath()+'/trace_report.data'
  open(path,'w').write(str(ret))







