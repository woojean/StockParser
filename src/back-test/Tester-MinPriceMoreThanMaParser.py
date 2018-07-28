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
from parsers import MinPriceMoreThanMaParser

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
      # print repr(e)
      pass
  return ret


def trace(id,parseDay):
  print id,parseDay
  parser = MinPriceMoreThanMaParser.MinPriceMoreThanMaParser(parseDay)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()

  (gr5,buyPrice) = parser.computeGr(res,parseDay)
  dayList = parser.getNextTradingDayList(parseDay,2)
  inDay = dayList[0]
  outDay = dayList[1]
  inDayMinPrice = parser.getMinPriceOfDay(res,inDay)

  if inDayMinPrice > buyPrice: # 未能买入
    # print "Can't Buy"
    return False

  inDayStartPrice = parser.getStartPriceOfDay(res,inDay)
  if 0==inDayStartPrice:
    return False


  inPrice = min(buyPrice,inDayStartPrice) # 买入
  outPrice = parser.getStartPriceOfDay(res,outDay)
  if 0==outPrice:
    return False

  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outPrice'] = outPrice
  ret['gr'] = gr5
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


