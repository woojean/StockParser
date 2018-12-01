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
from spiders import BaseSpider
from parsers import BaseParser


'''
市场仪表盘
'''

# ------------------------------------------------------------------------

def dumpReport(ret):
  pass

def getParams():
  parseDay = time.strftime('%Y-%m-%d',time.localtime(time.time())) 

  for item in sys.argv:
    if 10 == len(item):
      parseDay = item

  return (parseDay)


def getRes(id):
  priceFile = Tools.getPriceDirPath()+'/'+str(id)
  res = open(priceFile,'r').read()
  return res

def isUpwardLimit(res,parseDay):
  dayList = BaseParser.BaseParser.getPastTradingDayList(parseDay,2)
  endPrice1 = parser.getEndPriceOfDay(res,dayList[-2])
  endPrice2 = parser.getEndPriceOfDay(res,dayList[-1])
  if endPrice1 == 0 or  endPrice2 == 0:
    return False
  r = (endPrice2 - endPrice1)/endPrice1
  if r < 0.095:
    return False
  return True


def getUpwardLimitNum(res,parseDay):
  days = 20
  dayList = BaseParser.BaseParser.getPastTradingDayList(parseDay,days)
  num = 0
  for i in xrange(1,days-1):
    if isUpwardLimit(res,dayList[-i]):
      num += 1
    else:
      break
  return num

'''
[
  [000001,3],
  ...
]
'''
def getContinuousUpwardLimitData(idList):
  ret = []

  for id in idList:
    print id
    try:
      res = getRes(id)
      if not isUpwardLimit(res,parseDay):
        continue
      upwardLimitNum = getUpwardLimitNum(res,parseDay)
      ret.append((id,upwardLimitNum))
    except Exception, e:
      pass
      # print repr(e)

  return ret




parser = None

if __name__ == '__main__':
  data = {}
  print 'Dashboard'

  (parseDay) = getParams()
  print 'parseDay:'+parseDay

  parser = BaseParser.BaseParser(parseDay)

  idList = BaseSpider.BaseSpider.getIdList() 

  ret = getContinuousUpwardLimitData(idList)
  data['upwardLimitNUm'] = ret

  print data

  



