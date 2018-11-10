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
from parsers import UpWardLimitStepBackMaParser

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
首次回踩ma5买入，第二天开盘卖出
'''
def trace(id,parseDay):
  N = 20  # N天内会有回踩
  # print id,parseDay

  parser = UpWardLimitStepBackMaParser.UpWardLimitStepBackMaParser(parseDay,id)
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  dayList = parser.getNextTradingDayList(parseDay,N) # 

  
  # 
  inPrice = 0
  outDay = ''
  outPrice = 0
  for i in xrange(1,N-2):
    # 预期的回测5日线跌幅
    gr5 = UpWardLimitStepBackMaParser.UpWardLimitStepBackMaParser.getReboundMa5(res,dayList[i-1])
    if gr5 <= -1:  
      return False

    # 判断是否有买入机会
    endP1 = parser.getMinPriceOfDay(res,dayList[i-1])
    minP2 = parser.getMinPriceOfDay(res,dayList[i])
    minGr = (minP2 - endP1)/endP1
    if minGr > gr5: 
      return False

    # 买入价为回踩5日线的价格
    inDay = dayList[i]
    inPrice = endP1*( 1 + gr5 )

    outDay = dayList[i+1]
    outPrice = parser.getMinPriceOfDay(res,dayList[i+1]) # 卖出价为第二天收盘价
    break


  ret = {}
  ret['id'] = id
  ret['name'] = Tools.getNameById(id)
  ret['inPrice'] = inPrice
  ret['outDay'] = outDay
  ret['outPrice'] = outPrice
  ret['holdDays'] = 1
  ret['minPrice'] = 0
  ret['maxPrice'] = 0
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

  


